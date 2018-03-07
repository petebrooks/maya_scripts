import maya.mel as mel
import pymel.core as pm
import os

def create_procedural(path_to_ass):
  base_name = os.path.splitext(os.path.basename(path_to_ass))[0]
  dirname = os.path.dirname(path_to_ass)
  fbx_path = os.path.join(dirname, base_name + ".fbx")
  obj_path = os.path.join(dirname, base_name + ".obj")

  geo_node = _import_if_exists(fbx_path) or _import_if_exists(obj_path)

  if geo_node:
    pm.rename(geo_node, base_name)
    geo_node.aiTranslator.set("procedural")
    geo_node.dso.set(path_to_ass)
  else:
    print "No proxy found for %s" % base_name

def import_procedurals():
  files = _prompt_files("Select ASS files to import")
  for file in files:
    print "Importing " + file
    create_procedural(file)

# def createStandIns():
#   files = _prompt_files("Select ASS files to import")
#   for file in files:
#     print "Creating stand-in " + file

def export_selected():
  export_dir = _prompt_directory("Select export directory")

  for mesh in pm.selected():
    export(mesh, export_dir)

def export(mesh, export_dir=""):
  base_name = str(mesh).replace("_Geo", "")

  ass_export_path = os.path.join(export_dir, base_name + ".ass")
  fbx_export_path = os.path.join(export_dir, base_name + ".fbx")

  _export_ass(mesh, ass_export_path)
  print "Exported %s to %s" % (mesh, ass_export_path)
  _export_fbx(mesh, fbx_export_path)
  print "Exported %s to %s" % (mesh, fbx_export_path)

def _export_ass(mesh, path):
  pm.select(mesh)
  command = "arnoldExportAss -f \"%s\" -s -shadowLinks 1 -mask 2303 -lightLinks 1 -boundingBox -cam perspShape" % path
  mel.eval(command)

def _export_fbx(mesh, path):
  pm.select(mesh)
  pm.exportSelected(
    path,
    force=True,
    typ="FBX export",
    options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"
  )

def _export_obj(mesh, path):
  pm.select(mesh)
  pm.exportSelected(
    path,
    force=True,
    typ="OBJexport",
    options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"
  )

def _import_if_exists(path):
  if not os.path.exists(path):
    print "'%s' does not exist" % path
    return False

  return pm.importFile(
    path,
    returnNewNodes=True,
  )[-1]

def _prompt_directory(caption="Select directory"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 3, # Directory mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog[0]

def _prompt_files(caption="Select one or more files"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 4, # Multiple file mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog
