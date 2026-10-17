# GIMI Model Dumps (Genshin / Wuwa / NTE)

Custom 3DMigoto / XXMI frame-analysis and GIMI-ready model dumps prepared for **Blender import** (`.txt` topology dumps, `.vb`/`.ib`/`.buf` buffers, `.dds` textures, and `hash.json` metadata) across:

- **[`Genshin/`](./Genshin)** — Genshin Impact (GIMI / XXMI) custom character, NPC, weapon, and asset dumps
- **[`Wuwa/`](./Wuwa)** — Wuthering Waves (WWMI / XXMI) custom character, weapon, and asset dumps
- **[`NTE/`](./NTE)** — Neverness to Everness (NTE / XXMI) custom character, vehicle, and asset dumps

---

## Repository Structure

```text
GIMI-Model-Dumps/
├── Genshin/
│   └── <AssetName>/
│       ├── hash.json
│       ├── *vb0*.txt / *ib*.txt      # Blender 3DMigoto raw text topology dumps
│       ├── *.vb / *.ib / *.buf       # Binary vertex/index/blend buffers (if exported)
│       └── *.dds / *.png             # Diffuse, LightMap, NormalMap, ShadowRamp textures
├── Wuwa/
│   └── <AssetName>/
│       ├── hash.json / metadata.json
│       ├── *.txt / *.vb / *.ib / *.buf
│       └── *.dds / *.png
├── NTE/
│   └── <AssetName>/
│       ├── hash.json / metadata.json
│       ├── *.txt / *.vb / *.ib / *.buf
│       └── *.dds / *.png
├── tools/
│   └── sync_dumps.py                 # Validator, manifest generator & GitHub sync helper
├── Upload_Dumps_To_GitHub.bat        # 1-click local validation, commit & push launcher
└── manifest.json                     # Auto-generated index of all dumps in this repository
```

---

## How to Add & Upload New Dumps Locally

1. Place your extracted GIMI / WWMI / NTE dump folder inside the corresponding game folder:
   - `D:\Genshin all in one\GIMI-Model-Dumps\Genshin\<CharacterOrItemName>\`
   - `D:\Genshin all in one\GIMI-Model-Dumps\Wuwa\<CharacterOrItemName>\`
   - `D:\Genshin all in one\GIMI-Model-Dumps\NTE\<CharacterOrItemName>\`
2. Double-click **`Upload_Dumps_To_GitHub.bat`** (or run `python tools/sync_dumps.py --push`).
3. The script will:
   - Scan `Genshin/`, `Wuwa/`, and `NTE/` and verify which dumps are **Blender-import ready** (`.txt` / `.vb` / `.ib` / `hash.json` / `.dds`).
   - Check file sizes to prevent GitHub's 100 MB per-file push rejection.
   - Update `manifest.json` and commit + push to `https://github.com/abdulrehmankhan5466-ui/GIMI-Model-Dumps`.

---

## Importing Into Blender

1. Install the **3DMigoto / XXMI Blender Add-on** matching your target game (GIMI / WWMI / XXMI Tools).
2. Download the desired folder from **`Genshin/`**, **`Wuwa/`**, or **`NTE/`** (or download directly via the **GitHub Assets** tab in **Genshin Modder Pro** / **WuWa Modder Pro** / **NTE Modder Pro**).
3. In Blender:
   - For **Frame Analysis `.txt` dumps**: Use *File → Import → 3DMigoto Raw Buffers (`.txt`)* and select the matched `*vb0*.txt` + `*ib*.txt` pair.
   - For **Extracted `.vb`/`.ib`/`.buf` dumps**: Use the XXMI/GIMI import panel with `hash.json`.

---

## Notice & Attribution

Game assets, meshes, and textures dumped from Genshin Impact, Wuthering Waves, and Neverness to Everness remain the intellectual property of their respective developers/publishers (HoYoverse / Cognosphere, Kuro Games, Hotta Studio / Perfect World). These dumps are shared solely for non-commercial fan modding, study, and Blender reference in compliance with community modding guidelines.
