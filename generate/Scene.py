import bpy
import mathutils
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

    def create_scene(self):
        # Clear all mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        # Remove all objects from the default scene collection
        for obj in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)

        # Add ground and background plane
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD')
        ground = bpy.context.active_object
        ground.scale = (10, 10, 10)  # Scale up the ground plane

        # Add texture to ground
        img = bpy.data.images.load(self.texture_image)
        tex = bpy.data.textures.new('ColorTex', type='IMAGE')
        tex.image = img
        mat = bpy.data.materials.new('TexMat')
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_node.image = img
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
        ground.data.materials.append(mat)

        # Position the object and support
        self.obj.location = self.object_position
        self.obj.rotation_euler = [radians(a) for a in self.object_orientation]  # Convert to radians
        self.support.location = (self.object_position[0], self.object_position[1], self.object_position[2]-1)  # Assuming the support is just below the object

        # Position the camera
        cam_data = bpy.data.cameras.new('camera')
        cam = bpy.data.objects.new('camera', cam_data)
        bpy.context.scene.collection.objects.link(cam)
        bpy.context.scene.camera = cam
        cam.location = self.camera_position
        cam.rotation_euler = self.obj.rotation_euler  # Make the camera face the object

        # Add a light source
        light_data = bpy.data.lights.new(name="light", type='POINT')
        light = bpy.data.objects.new(name="light", object_data=light_data)
        bpy.context.scene.collection.objects.link(light)
        light.location = (5, -5, 5)  # Change as required

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
