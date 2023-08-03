import bpy
import mathutils
import random
from math import radians

class Scene:

    def __init__(self, object_path, support_path, texture_image, object_position, object_orientation, camera_position):
        self.object_path = object_path
        self.support_path = support_path
        self.texture_image = texture_image
        self.object_position = object_position
        self.object_orientation = object_orientation
        self.camera_position = camera_position

        # Load object and support
        self.obj = self.load_obj(self.object_path)
        self.support = self.load_obj(self.support_path)

        # Create scene
        self.create_scene()

    def load_obj(self, path):
        bpy.ops.import_scene.obj(filepath=path)
        return bpy.context.selected_objects[0]  # Return the last imported object
    
    def import_dae_object(file_path):
        bpy.ops.wm.collada_import(filepath=file_path)
        obj = bpy.context.selected_objects[0]
        return obj

    def setup_scene(self, config):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # # Enable GPU rendering
        # bpy.context.scene.cycles.device = 'GPU'
        # bpy.context.scene.render.resolution_x = config['resolution_x']
        # bpy.context.scene.render.resolution_y = config['resolution_y']
        # bpy.context.scene.render.image_settings.file_format = 'PNG'

        self.set_random_lighting(config)
        self.set_random_camera_pose(config)

    def set_random_camera_pose(self, config):
        # Set up the camera
        camera_config = config['camera']
        min_location = camera_config['location_min']
        max_location = camera_config['location_max']
        min_rotation = camera_config['rotation_min']
        max_rotation = camera_config['rotation_max']
        
        random_location = [
            random.uniform(min_location[0], max_location[0]),
            random.uniform(min_location[1], max_location[1]),
            random.uniform(min_location[2], max_location[2])
        ]
        
        random_rotation = [
            random.uniform(min_rotation[0], max_rotation[0]),
            random.uniform(min_rotation[1], max_rotation[1]),
            random.uniform(min_rotation[2], max_rotation[2])
        ]

        bpy.ops.object.camera_add(location=random_location)
        cam = bpy.context.active_object
        cam.rotation_euler = tuple(random_rotation)
        cam.data.type = 'PERSP'
        bpy.context.scene.camera = cam


    def set_random_lighting(self, config):
        # Set up the lighting
        lighting_config = config['lighting']
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select all light objects in the current scene
        for obj in bpy.context.scene.objects:
            if obj.type == 'LIGHT':
                obj.select_set(True)

        # Delete selected light objects
        bpy.ops.object.delete()

        for _ in range(lighting_config['num_lights']):
            bpy.ops.object.light_add(type=lighting_config['light_type'], align='WORLD', location=(0, 0, lighting_config['light_distance']))
            light = bpy.context.active_object
            light.data.color = lighting_config['light_color']

            if lighting_config['light_type'] == "AREA":
                light.data.size = lighting_config['light_size']

            if lighting_config['type'] == 'random':
                light.data.energy = random.uniform(lighting_config['light_energy_min'], lighting_config['light_energy_max'])
            else:
                light.data.energy = lighting_config['light_energy_min']

    def get_object_pose(self):
        return self.obj.matrix_world

    def get_camera_pose(self):
        return bpy.context.scene.camera.matrix_world

    def render(self, output_path='render.png', resolution_x=1920, resolution_y=1080, samples=128):
        bpy.context.scene.render.resolution_x = resolution_x
        bpy.context.scene.render.resolution_y = resolution_y
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.filepath = output_path

        # Render settings for cycles
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = samples
        bpy.context.scene.cycles.device = 'GPU'  # or 'CPU' depending on your preferences

        # Trigger render
        bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    object_path = "../data/examples/meshes/Mug/10f6e09036350e92b3f21f1137c3c347.obj"
    support_path = "../data/examples/meshes/Table/99cf659ae2fe4b87b72437fd995483b.obj"
    texture_image = "/home/geraldebmer/Pictures/dtd-r1.0.1/dtd/images/porous/porous_0045.jpg"
    object_position = (0, 0, 0)
    object_orientation = (0, 0, 0)
    camera_position = (2, 0, 1)
    bpy.context.view_layer.objects.clear() 
    scene = Scene(object_path, support_path, texture_image, object_position, object_orientation, camera_position)
    print("object pose: ", scene.get_object_pose())
    print("camera pose: ", scene.get_camera_pose())

    scene.render()
