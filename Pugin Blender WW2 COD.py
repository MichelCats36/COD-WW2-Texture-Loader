bl_info = {
    "name": "Texture Loader Add-on",
    "blender": (3, 3, 20),
    "category": "Object",
}

import bpy
import os
import json
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator, Panel

class MATERIAL_OT_get_names_from_json(Operator, ImportHelper):
    bl_idname = "material.get_names_from_json"
    bl_label = "Get Material Names from JSON"
    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'})

    def execute(self, context):
        file_path = self.filepath
        if not os.path.exists(file_path):
            self.report({'ERROR'}, "JSON file not found.")
            return {'CANCELLED'}

        with open(file_path, 'r') as file:
            data = json.load(file)

        names = [item.get('Name', 'Unnamed') for item in data.values()]
        names_text = ', '.join(names)

        text_block = bpy.data.texts.new(name="Material_Names")
        text_block.clear()
        text_block.write(names_text)

        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces.active.text = text_block
                break

        self.report({'INFO'}, "Material names loaded into the scripting tab.")
        return {'FINISHED'}

class MATERIAL_OT_rename_files(Operator, ImportHelper):
    bl_idname = "material.rename_files"
    bl_label = "Rename TXT and MTL Files"
    use_filter_folder = True

    def execute(self, context):
        root_dir = self.filepath
        old_suffix = '_images'
        new_suffix = ''

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith((old_suffix + '.txt', old_suffix + '.mtl')):
                    old_file_path = os.path.join(root, file)
                    new_file_name = file.replace(old_suffix, new_suffix)
                    new_file_path = os.path.join(root, new_file_name)

                    self.report({'INFO'}, f"Renaming {old_file_path} to {new_file_path}")
                    os.rename(old_file_path, new_file_path)

        self.report({'INFO'}, "Renaming complete.")
        return {'FINISHED'}

class MATERIAL_OT_rename_special_characters(Operator, ImportHelper):
    bl_idname = "material.rename_special_characters"
    bl_label = "Rename Special Characters in TXT and MTL Files"
    use_filter_folder = True

    def execute(self, context):
        directory_path = self.filepath

        def replace_chars(text):
            for char in ['~', '&', '$']:
                text = text.replace(char, '_')
            return text

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.txt', '.mtl')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = replace_chars(content)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    self.report({'INFO'}, f"Processed: {file_path}")

        self.report({'INFO'}, "Renaming special characters complete.")
        return {'FINISHED'}

class MATERIAL_OT_rename_textures_files(Operator, ImportHelper):
    bl_idname = "material.rename_textures_files"
    bl_label = "Rename Textures Files Special Characters"
    use_filter_folder = True

    def execute(self, context):
        directory_path = self.filepath

        def replace_chars(filename):
            for char in ['~', '&', '$']:
                filename = filename.replace(char, '_')
            return filename

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.png', '.dds', '.tga', '.tiff', '.tif', '.jpg', '.jpeg', '.bmp')):
                    old_path = os.path.join(root, file)
                    new_filename = replace_chars(file)
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
                    self.report({'INFO'}, f"Renamed: {file} to {new_filename}")

        self.report({'INFO'}, "Renaming of textures complete.")
        return {'FINISHED'}

class MATERIAL_OT_cleanup_and_replace(Operator):
    bl_idname = "material.cleanup_and_replace"
    bl_label = "Cleanup and Replace Materials and Textures"

    def cleanup_names(self, data, name_attr):
        cleaned_names = {}

        for item in data:
            name = getattr(item, name_attr)
            if "." in name:
                base_name, suffix = name.rsplit(".", 1)
                if suffix.isdigit():
                    if data.get(base_name):
                        cleaned_names[name] = base_name
                    else:
                        setattr(item, name_attr, base_name)
                        cleaned_names[name] = base_name

        return cleaned_names

    def replace_materials_in_meshes(self, cleaned_materials):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                if obj.data.materials:
                    for i in range(len(obj.data.materials)):
                        mat = obj.data.materials[i]
                        if mat and mat.name in cleaned_materials:
                            new_mat_name = cleaned_materials[mat.name]
                            new_mat = bpy.data.materials.get(new_mat_name)
                            if new_mat:
                                obj.data.materials[i] = new_mat

    def replace_textures_in_materials(self, cleaned_textures):
        for mat in bpy.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        tex = node.image
                        if tex and tex.name in cleaned_textures:
                            new_tex_name = cleaned_textures[tex.name]
                            new_tex = bpy.data.images.get(new_tex_name)
                            if new_tex:
                                node.image = new_tex

    def remove_unused_materials(self):
        for mat in bpy.data.materials:
            if not mat.users:
                bpy.data.materials.remove(mat)

    def remove_unused_textures(self):
        for tex in bpy.data.images:
            if not tex.users:
                bpy.data.images.remove(tex)

    def execute(self, context):
        cleaned_materials = self.cleanup_names(bpy.data.materials, 'name')
        self.replace_materials_in_meshes(cleaned_materials)

        cleaned_textures = self.cleanup_names(bpy.data.images, 'name')
        self.replace_textures_in_materials(cleaned_textures)

        self.remove_unused_materials()
        self.remove_unused_textures()

        self.report({'INFO'}, "Material and texture names cleaned up and replaced in meshes and materials. Unused materials and textures removed.")
        return {'FINISHED'}

class MATERIAL_OT_mapping(Operator):
    bl_idname = "material.mapping"
    bl_label = "Material Texture Mesh Mapping"

    def execute(self, context):
        material_texture_map = {}

        for material in bpy.data.materials:
            if material.use_nodes:
                texture_nodes = [node for node in material.node_tree.nodes if node.type == 'TEX_IMAGE']
                texture_paths = [node.image.name if node.image else 'No texture' for node in texture_nodes]
                material_texture_map[material.name] = {
                    'textures': texture_paths,
                    'meshes': []
                }
            else:
                material_texture_map[material.name] = {
                    'textures': ['No nodes'],
                    'meshes': []
                }

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material and slot.material.name in material_texture_map:
                        material_texture_map[slot.material.name]['meshes'].append(obj.name)

        clipboard_text = "Material to Texture and Mesh Mapping:\n\n"
        for material, data in material_texture_map.items():
            textures = data['textures']
            meshes = data['meshes']
            clipboard_text += f"{material} has textures: {', '.join(textures)} and is applied to meshes: {', '.join(meshes)}\n"

        text_block = bpy.data.texts.new(name="Material_Texture_Mesh_Mapping")
        text_block.clear()
        text_block.write(clipboard_text)

        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                area.spaces.active.text = text_block
                break

        self.report({'INFO'}, "Material to Texture and Mesh Mapping created.")
        return {'FINISHED'}

class TEXTURE_OT_select_texture_info_directory(Operator, ImportHelper):
    bl_idname = "texture.select_texture_info_directory"
    bl_label = "Select Texture Info Directory"
    use_filter_folder = True

    def execute(self, context):
        context.scene.texture_info_directory = self.filepath
        self.report({'INFO'}, f"Selected texture info directory: {self.filepath}")
        return {'FINISHED'}


class TEXTURE_OT_select_texture_directory(Operator, ImportHelper):
    bl_idname = "texture.select_texture_directory"
    bl_label = "Select Texture Directory"
    use_filter_folder = True

    def execute(self, context):
        context.scene.texture_directory = self.filepath
        self.report({'INFO'}, f"Selected texture directory: {self.filepath}")
        return {'FINISHED'}


class TEXTURE_OT_load_textures(Operator):
    bl_idname = "texture.load_textures"
    bl_label = "Load Textures"

    def add_file_extension(self, filename):
        if not os.path.splitext(filename)[1]:
            return filename + ".png"
        return filename

    def find_files(self, directory, extensions):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in extensions):
                    matches.append(os.path.join(root, filename))
        return matches

    def assign_material_to_mesh(self, material_name):
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and (obj.name == material_name or obj.name.replace("::", "_") == material_name):
                if material_name in bpy.data.materials:
                    obj.data.materials.clear()
                    obj.data.materials.append(bpy.data.materials[material_name])
                    self.report({'INFO'}, f"Assigned material '{material_name}' to mesh '{obj.name}'")
                else:
                    self.report({'WARNING'}, f"Material '{material_name}' not found for mesh '{obj.name}'")

    def execute(self, context):
        texture_info_directory = context.scene.texture_info_directory
        texture_directory = context.scene.texture_directory

        if not texture_info_directory or not texture_directory:
            self.report({'ERROR'}, "Please select both the texture info directory and the texture directory")
            return {'CANCELLED'}

        texture_info_files = self.find_files(texture_info_directory, ['.txt', '.mtl'])
        if not texture_info_files:
            self.report({'ERROR'}, "No texture info files found in the selected directory")
            return {'CANCELLED'}

        texture_files = self.find_files(texture_directory, ['.png', '.jpg', '.jpeg', '.tga'])
        texture_files_map = {os.path.basename(f): f for f in texture_files}

        for texture_info_file in texture_info_files:
            with open(texture_info_file, 'r') as f:
                lines = f.readlines()

            texture_info = {}
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue
                texture_info[parts[0]] = parts[1]

            material_name = os.path.splitext(os.path.basename(texture_info_file))[0]
            material = bpy.data.materials.get(material_name)
            if material is None:
                material = bpy.data.materials.new(name=material_name)
            else:
                material.node_tree.nodes.clear()

            material.use_nodes = True
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            output_node.location = (300, 0)

            shader_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            shader_node.location = (0, 0)

            links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface'])

            def create_texture_node(image_name, node_location):
                texture_node = nodes.new(type='ShaderNodeTexImage')
                image_name_with_ext = self.add_file_extension(image_name)
                texture_path = texture_files_map.get(image_name_with_ext)
                if texture_path:
                    if image_name_with_ext in bpy.data.images:
                        texture_node.image = bpy.data.images[image_name_with_ext]
                        self.report({'INFO'}, f"Texture '{image_name_with_ext}' already loaded. Using existing.")
                    else:
                        print(f"Attempting to load texture: {texture_path}")
                        texture_node.image = bpy.data.images.load(texture_path)
                        self.report({'INFO'}, f"Loaded texture: {texture_path}")
                    texture_node.location = node_location
                    return texture_node
                else:
                    self.report({'WARNING'}, f"Texture file {image_name_with_ext} not found in the directory")
                    return None

            def link_texture(texture_type, input_name, node_location):
                if texture_type in texture_info:
                    texture_node = create_texture_node(texture_info[texture_type], node_location)
                    if texture_node:
                        if input_name == 'Normal':
                            normal_map_node = nodes.new(type='ShaderNodeNormalMap')
                            normal_map_node.location = (-300, -600)
                            links.new(texture_node.outputs['Color'], normal_map_node.inputs['Color'])
                            links.new(normal_map_node.outputs['Normal'], shader_node.inputs['Normal'])
                        elif input_name in shader_node.inputs:
                            links.new(texture_node.outputs['Color'], shader_node.inputs[input_name])
                        else:
                            self.report({'WARNING'}, f"Input {input_name} not found in Principled BSDF shader")

            priorities = [
                ('colorMap', 'Base Color', (-600, 600)),
                ('specularMap', 'Specular', (-600, 0)),
                ('normalMap', 'Normal', (-600, -600))
            ]

            for texture_type, input_name, location in priorities:
                link_texture(texture_type, input_name, location)

            additional_textures = {
                'unk_semantic_0xB60D1850': ('Metallic', (-500, 300)),
                'unk_semantic_0xCFE18444': ('Roughness', (-500, -300))
            }

            for semantic, (input_name, location) in additional_textures.items():
                if semantic in texture_info:
                    texture_node = create_texture_node(texture_info[semantic], location)
                    if texture_node:
                        if input_name == 'Normal':
                            normal_map_node = nodes.new(type='ShaderNodeNormalMap')
                            normal_map_node.location = (-300, -600)
                            links.new(texture_node.outputs['Color'], normal_map_node.inputs['Color'])
                            links.new(normal_map_node.outputs['Normal'], shader_node.inputs['Normal'])
                        elif input_name in shader_node.inputs:
                            links.new(texture_node.outputs['Color'], shader_node.inputs[input_name])
                        else:
                            self.report({'WARNING'}, f"Input {input_name} not found in Principled BSDF shader")

            self.report({'INFO'}, f"Material '{material_name}' created with textures")
            self.assign_material_to_mesh(material_name)

        # Assign base materials to duplicated objects after textures are loaded
        assign_base_material_to_duplicates()

        return {'FINISHED'}

# Helper functions to handle base material assignment for duplicated objects

def collect_base_materials():
    base_materials = {}
    for mat in bpy.data.materials:
        base_name = mat.name.rsplit(".", 1)[0]
        if base_name not in base_materials:
            base_materials[base_name] = mat
            print(f"Collected base material: {base_name} -> {mat.name}")
    return base_materials

def assign_materials_to_objects(base_materials):
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for i, mat in enumerate(obj.data.materials):
                if mat:
                    base_name = mat.name.rsplit(".", 1)[0]
                    if base_name in base_materials:
                        base_mat = base_materials[base_name]
                        if base_mat and mat != base_mat:
                            print(f"Object '{obj.name}': Assigning '{base_mat.name}' to replace '{mat.name}' in material slot {i}")
                            obj.data.materials[i] = base_mat
                            if len(obj.material_slots) > i:
                                obj.material_slots[i].material = base_mat

def assign_missing_materials(base_materials):
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and not obj.data.materials:
            base_name = obj.name.rsplit(".", 1)[0]
            if base_name in base_materials:
                base_mat = base_materials[base_name]
                obj.data.materials.append(base_mat)
                print(f"Assigned base material '{base_mat.name}' to object '{obj.name}' which had no material.")

def assign_base_material_to_duplicates():
    base_materials = collect_base_materials()
    assign_materials_to_objects(base_materials)
    assign_missing_materials(base_materials)

class TEXTURE_PT_panel(Panel):
    bl_label = "Texture Loader"
    bl_idname = "TEXTURE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Texture Loader'

    def draw(self, context):
        layout = self.layout
        layout.operator(MATERIAL_OT_get_names_from_json.bl_idname)
        layout.operator(MATERIAL_OT_rename_files.bl_idname)
        layout.operator(MATERIAL_OT_rename_textures_files.bl_idname)
        layout.operator(MATERIAL_OT_rename_special_characters.bl_idname)
        layout.operator(TEXTURE_OT_select_texture_info_directory.bl_idname)
        layout.operator(TEXTURE_OT_select_texture_directory.bl_idname)
        layout.operator(TEXTURE_OT_load_textures.bl_idname)
        layout.operator(MATERIAL_OT_cleanup_and_replace.bl_idname)
        layout.operator(MATERIAL_OT_mapping.bl_idname)

def menu_func(self, context):
    self.layout.operator(TEXTURE_OT_select_texture_info_directory.bl_idname)
    self.layout.operator(TEXTURE_OT_select_texture_directory.bl_idname)
    self.layout.operator(TEXTURE_OT_load_textures.bl_idname)

def register():
    bpy.utils.register_class(MATERIAL_OT_get_names_from_json)
    bpy.utils.register_class(MATERIAL_OT_rename_files)
    bpy.utils.register_class(MATERIAL_OT_rename_textures_files)
    bpy.utils.register_class(MATERIAL_OT_rename_special_characters)
    bpy.utils.register_class(TEXTURE_OT_select_texture_info_directory)
    bpy.utils.register_class(TEXTURE_OT_select_texture_directory)
    bpy.utils.register_class(TEXTURE_OT_load_textures)
    bpy.utils.register_class(MATERIAL_OT_cleanup_and_replace)
    bpy.utils.register_class(MATERIAL_OT_mapping)
    bpy.utils.register_class(TEXTURE_PT_panel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)
    bpy.types.Scene.texture_info_directory = StringProperty(name="Texture Info Directory", default="")
    bpy.types.Scene.texture_directory = StringProperty(name="Texture Directory", default="")

def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_get_names_from_json)
    bpy.utils.unregister_class(MATERIAL_OT_rename_files)
    bpy.utils.unregister_class(MATERIAL_OT_rename_textures_files)
    bpy.utils.unregister_class(MATERIAL_OT_rename_special_characters)
    bpy.utils.unregister_class(TEXTURE_OT_select_texture_info_directory)
    bpy.utils.unregister_class(TEXTURE_OT_select_texture_directory)
    bpy.utils.unregister_class(TEXTURE_OT_load_textures)
    bpy.utils.unregister_class(MATERIAL_OT_cleanup_and_replace)
    bpy.utils.unregister_class(MATERIAL_OT_mapping)
    bpy.utils.unregister_class(TEXTURE_PT_panel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
    del bpy.types.Scene.texture_info_directory
    del bpy.types.Scene.texture_directory

if __name__ == "__main__":
    register()
