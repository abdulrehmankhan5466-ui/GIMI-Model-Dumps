# Genshin Impact — Custom GIMI / Blender Dumps

Place each Genshin Impact dump inside its own subfolder:

```text
Genshin/
└── <Character_NPC_or_Weapon_Name>/
    ├── hash.json
    ├── <Component>-vb0=<hash>.txt
    ├── <Component>-ib=<hash>.txt
    ├── *.dds
    └── README.md (optional notes)
```

### Supported Blender Import Formats
- **GIMI Frame Analysis `.txt` Dumps**: Pair of `*vb0*.txt` and `*ib*.txt` files + `.dds` textures (`Diffuse`, `LightMap`, `NormalMap`, `ShadowRamp`).
- **GIMI Extracted Buffer Dumps**: `hash.json` + `.vb` / `.ib` / `.buf` + `.dds` textures.
