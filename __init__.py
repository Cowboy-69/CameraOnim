# for reload
if "bpy" in locals():
    import importlib

    if "import_onim" in locals():
        importlib.reload(import_onim)

    if "export_onim" in locals():
        importlib.reload(export_onim)

import os
import time

import bpy
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper

from . import import_onim
from . import export_onim

bl_info = {
    "name": "CameraOnim",
    "author": "Cowboy69",
    "blender": (2, 80, 0),
    "version": (0, 8),
    "description": "Camera ONIM file importer & Exporter",
    "location": "File > Import-Export",
    "category": "Import-Export"
}


class Import_ONIM(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.onim"
    bl_description = 'Import file in ONIM format'
    bl_label = "Camera ONIM (.onim)"

    filter_glob : bpy.props.StringProperty(
        default = "*.onim",
        options = {'HIDDEN'}
    )
    
    directory : bpy.props.StringProperty(
        maxlen = 1024,
        default = "",
        subtype = 'FILE_PATH',
        options = {'HIDDEN'}
    )
    
    files : bpy.props.CollectionProperty(
        type = bpy.types.OperatorFileListElement,
        options = {'HIDDEN'}
    )

    filepath : bpy.props.StringProperty(
         name = "File path",
         description = "ONIM file path",
         maxlen = 1024,
         default = "",
         options = {'HIDDEN'}
     )

    def draw(self, context):
        layout = self.layout
        
    def execute(self, context):
        for file in [os.path.join(self.directory, file.name) for file in self.files] if self.files else [self.filepath]:
            import_onim.start_import(
                                    {
                                     'filePath' : file,
                                    }
                                    )
                
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def import_onim_link(self, context):
    self.layout.operator(Import_ONIM.bl_idname, text="Camera ONIM (.onim)")


class Export_ONIM(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.onim"
    bl_description = 'Export the selected camera to ONIM format'
    bl_label = "Camera ONIM (.onim)"
    filename_ext = ".onim"

    filter_glob : bpy.props.StringProperty(
        default = "*.onim",
        options = {'HIDDEN'}
    )
    
    directory : bpy.props.StringProperty(
        maxlen = 1024,
        default = "",
        subtype = 'FILE_PATH',
        options = {'HIDDEN'}
    )
    
    files : bpy.props.CollectionProperty(
        type = bpy.types.OperatorFileListElement,
        options = {'HIDDEN'}
    )

    filepath : bpy.props.StringProperty(
         name = "File path",
         description = "ONIM file path",
         maxlen = 1024,
         default = "",
         options = {'HIDDEN'}
     )

    def draw(self, context):
        layout = self.layout
        
    def execute(self, context):
        export_onim.start_export(
                                {
                                    'filePath' : self.filepath,
                                }
                                )
                
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def export_onim_link(self, context):
    self.layout.operator(Export_ONIM.bl_idname, text="Camera ONIM (.onim)")


def register():
    register_class(Import_ONIM)
    register_class(Export_ONIM)

    bpy.types.TOPBAR_MT_file_import.append(import_onim_link)
    bpy.types.TOPBAR_MT_file_export.append(export_onim_link)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(import_onim_link)
    bpy.types.TOPBAR_MT_file_export.remove(export_onim_link)

    unregister_class(Import_ONIM)
    unregister_class(Export_ONIM)
