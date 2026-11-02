import os

with open("project/findings/rtti_classes_raw.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

subsystems = {
    'Archive/Resource': ['Archive', 'Resource', 'File', 'Package', 'Stream'],
    'Memory/Alloc': ['Alloc', 'Heap', 'Pool', 'Buffer'],
    'Script/Lua': ['Lua', 'Script', 'Function', 'Symbol'],
    'Property/Meta': ['Property', 'Meta', 'Value', 'Flags', 'Enum'],
    'Scene/Game': ['Scene', 'Actor', 'Agent', 'Game', 'World', 'Entity', 'Component'],
    'Render/Graphics': ['Render', 'Shader', 'Mesh', 'Texture', 'Material', 'Light', 'Camera', 'D3D', 'DX11', 'Enlighten', 'Skeleton'],
    'Audio': ['Audio', 'Sound', 'FMOD', 'Music', 'Voice', 'Emitter'],
    'Input': ['Input', 'Controller', 'Keyboard', 'Mouse', 'Joy']
}

for sub, kws in subsystems.items():
    matched = [c for c in lines if any(kw.lower() in c.lower() for kw in kws)]
    print(f"=== {sub} ({len(matched)}) ===")
    for c in matched[:12]:
        print(" ", c)
