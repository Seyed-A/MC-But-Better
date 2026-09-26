import os
import zipfile
import json

def create_mrpack(instance_path, output_filename="modpack.mrpack", pack_name="My Custom Pack", pack_version="1.0.0", game_version="1.20.1", loader="fabric"):
    """
    Packages a Minecraft instance folder into a .mrpack file.
    """
    if not os.path.exists(instance_path):
        print(f"Error: Path '{instance_path}' does not exist.")
        return

    # 1. Define the basic Modrinth index structure
    index_data = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": pack_version,
        "name": pack_name,
        "summary": "Exported from local instance.",
        "files": [], # Empty because we are embedding everything in overrides
        "dependencies": {
            "minecraft": game_version,
            loader: "latest" # You can specify an exact loader version if known
        }
    }

    # Folders and files we want to include from the instance
    include_targets = ['config', 'mods', 'resourcepacks', 'shaderpacks', 'options.txt']

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as mrpack:
        # Write the index.json
        mrpack.writestr('modrinth.index.json', json.dumps(index_data, indent=2))
        
        # Walk through the instance folder and add to overrides
        for root, dirs, files in os.walk(instance_path):
            # Get relative path from the instance root
            rel_path = os.path.relpath(root, instance_path)
            
            # Check if this folder or its parent is in our allowed targets
            root_dir = rel_path.split(os.sep)[0]
            if root_dir not in include_targets and rel_path != '.':
                continue
                
            for file in files:
                # Skip system files
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                arc_path = os.path.join('overrides', rel_path, file) if rel_path != '.' else os.path.join('overrides', file)
                
                print(f"Adding: {arc_path}")
                mrpack.write(file_path, arc_path)

    print(f"\n🎉 Successfully created {output_filename}!")

# --- CONFIGURATION ---
# Replace this with the path to your instance folder (the folder containing /mods, /config, etc.)
INSTANCE_FOLDER = "./" 
OUTPUT_NAME = "pack.mrpack"
MC_VERSION = "26.2"
MOD_LOADER = "fabric" # Options: fabric, forge, neoforge, quilt

create_mrpack(INSTANCE_FOLDER, OUTPUT_NAME, pack_name="26.2 But Better", game_version=MC_VERSION, loader=MOD_LOADER)

