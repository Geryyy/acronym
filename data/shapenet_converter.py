import os
import shutil
from tqdm import tqdm

# Define the paths
grasp_path = os.path.expanduser('~/datasets/acronym/grasps')
mesh_path = os.path.expanduser('~/datasets/acronym/meshes')
obj_path = os.path.expanduser('~/datasets/models-OBJ/models/')

# Get the list of files to iterate through
files_to_iterate = [f for f in os.listdir(grasp_path) if f.endswith('.h5')]

if not os.path.exists(mesh_path):
            os.mkdir(mesh_path)

# Iterate through all the files in grasp_path with a progress bar
for filename in tqdm(files_to_iterate, desc="Processing files"):
    # Extract the samnetID from the filename
    category = filename.split('_')[0]
    samnetID = filename.split('_')[1]

    # Construct the path to the .obj file
    obj_file_path = os.path.join(obj_path, samnetID + '.obj')

    # Check if the .obj file exists
    if os.path.exists(obj_file_path):
        # Construct the destination path
        dest_dir = os.path.join(mesh_path, category)
        dest_path = os.path.join(dest_dir, samnetID + '.obj')

        # Copy the .obj file to the mesh_path
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        shutil.copy(obj_file_path, dest_path)
    else:
        print(f"OBJ file for {samnetID} not found")