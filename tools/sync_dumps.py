"""
sync_dumps.py
Scans Genshin/, Wuwa/, and NTE/ folders in the GIMI-Model-Dumps repository,
validates GIMI / WWMI / NTE Blender-import readiness, checks for oversized files
(>95 MB GitHub limit), generates manifest.json, and optionally commits + pushes
changes to GitHub.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_FOLDERS = ("Genshin", "Wuwa", "NTE")
MAX_GITHUB_FILE_BYTES = 95 * 1024 * 1024  # 95 MB safe threshold under GitHub's 100 MB limit


def inspect_asset_folder(game: str, asset_dir: Path) -> dict:
    files = [p for p in asset_dir.rglob("*") if p.is_file() and not p.name.startswith(".")]
    total_bytes = sum(p.stat().st_size for p in files)

    txt_vb = [p for p in files if p.suffix.lower() == ".txt" and "vb" in p.name.lower()]
    txt_ib = [p for p in files if p.suffix.lower() == ".txt" and "ib" in p.name.lower()]
    bin_buffers = [p for p in files if p.suffix.lower() in {".vb", ".ib", ".buf"}]
    textures = [p for p in files if p.suffix.lower() in {".dds", ".png", ".tga", ".jpg"}]
    meshes_3d = [p for p in files if p.suffix.lower() in {".blend", ".fbx", ".obj", ".glb", ".gltf"}]
    has_hash_json = any(p.name.lower() in {"hash.json", "metadata.json"} for p in files)
    has_ini = any(p.suffix.lower() == ".ini" for p in files)
    oversized = [
        {
            "path": p.relative_to(REPO_ROOT).as_posix(),
            "size_mb": round(p.stat().st_size / (1024 * 1024), 2),
        }
        for p in files
        if p.stat().st_size > MAX_GITHUB_FILE_BYTES
    ]

    blender_import_ready = bool((txt_vb and txt_ib) or bin_buffers or meshes_3d)
    if txt_vb and txt_ib:
        dump_format = "3dmigoto_txt_dump"
    elif bin_buffers:
        dump_format = "gimi_binary_buffers"
    elif meshes_3d:
        dump_format = "3d_mesh_project"
    else:
        dump_format = "textures_or_partial"

    return {
        "game": game,
        "name": asset_dir.name,
        "path": asset_dir.relative_to(REPO_ROOT).as_posix(),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "total_mb": round(total_bytes / (1024 * 1024), 2),
        "dump_format": dump_format,
        "blender_import_ready": blender_import_ready,
        "has_hash_json": has_hash_json,
        "has_ini": has_ini,
        "txt_vb_count": len(txt_vb),
        "txt_ib_count": len(txt_ib),
        "binary_buffer_count": len(bin_buffers),
        "texture_count": len(textures),
        "mesh_3d_count": len(meshes_3d),
        "oversized_files": oversized,
    }


def scan_repository() -> dict:
    summary = {
        "schema_version": 1,
        "repository": "abdulrehmankhan5466-ui/GIMI-Model-Dumps",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "games": {},
        "total_dumps": 0,
        "oversized_warnings": [],
    }

    for game in GAME_FOLDERS:
        game_dir = REPO_ROOT / game
        game_dir.mkdir(parents=True, exist_ok=True)
        entries = []
        for child in sorted(game_dir.iterdir(), key=lambda p: p.name.lower()):
            if child.is_dir() and not child.name.startswith("."):
                info = inspect_asset_folder(game, child)
                entries.append(info)
                if info["oversized_files"]:
                    summary["oversized_warnings"].extend(info["oversized_files"])
        summary["games"][game] = {
            "folder": game,
            "dump_count": len(entries),
            "dumps": entries,
        }
        summary["total_dumps"] += len(entries)

    return summary


def write_manifest(summary: dict) -> Path:
    manifest_path = REPO_ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return manifest_path


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=check,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and sync GIMI/WuWa/NTE model dumps to GitHub.")
    parser.add_argument("--push", action="store_true", help="Stage, commit, and push all changes to origin/main.")
    parser.add_argument("--message", default="", help="Optional custom commit message.")
    args = parser.parse_args()

    print("=" * 64)
    print(" GIMI-Model-Dumps - Validator & GitHub Upload Tool")
    print("=" * 64)

    summary = scan_repository()
    manifest_path = write_manifest(summary)

    for game in GAME_FOLDERS:
        game_info = summary["games"][game]
        print(f"\n[{game}] {game_info['dump_count']} dump folder(s):")
        if not game_info["dumps"]:
            print(f"  - (Empty - drop your {game} dumps into {REPO_ROOT / game})")
        for d in game_info["dumps"]:
            ready_tag = "READY FOR BLENDER" if d["blender_import_ready"] else "PARTIAL/TEXTURES"
            print(
                f"  - {d['name']} [{ready_tag}] ({d['dump_format']}, "
                f"{d['file_count']} files, {d['total_mb']} MB)"
            )

    if summary["oversized_warnings"]:
        print("\n[!] ERROR: The following file(s) exceed GitHub's 95 MB safe limit:")
        for item in summary["oversized_warnings"]:
            print(f"    - {item['path']} ({item['size_mb']} MB)")
        print("    Please compress or split oversized files (or enable Git LFS) before pushing.")
        return 1

    print(f"\n[+] Updated {manifest_path.relative_to(REPO_ROOT)}")

    if not args.push:
        print("\nScan complete (dry run). Pass --push or use Upload_Dumps_To_GitHub.bat to push to GitHub.")
        return 0

    print("\n[+] Staging files with git...")
    run_git(["add", "-A"])

    status = run_git(["status", "--porcelain"]).stdout.strip()
    if not status:
        print("[+] Working tree is clean — nothing new to commit. Pushing any unpushed commits...")
    else:
        commit_msg = args.message.strip() or (
            f"Update model dumps ({summary['total_dumps']} total across Genshin/Wuwa/NTE)"
        )
        print(f"[+] Committing: {commit_msg}")
        commit_proc = run_git(["commit", "-m", commit_msg], check=False)
        if commit_proc.returncode != 0:
            print(commit_proc.stdout)
            print(commit_proc.stderr)
            return commit_proc.returncode

    print("[+] Pushing to GitHub (origin main)...")
    push_proc = run_git(["push", "-u", "origin", "main"], check=False)
    if push_proc.returncode != 0:
        print(push_proc.stdout)
        print(push_proc.stderr)
        return push_proc.returncode

    print("\n" + "=" * 64)
    print(" SUCCESS! Your dumps are live on GitHub:")
    print(" https://github.com/abdulrehmankhan5466-ui/GIMI-Model-Dumps")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
