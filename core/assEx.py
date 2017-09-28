import maya.mel as mel

# scene_dir = directory or os.path.dirname(pm.sceneName()) # Extract to util

def prompt_directory(caption="Select directory"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 3, # Directory mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog[0]

def prompt_file(caption="Select file"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 1, # Single file mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog[0]

def prompt_files(caption="Select one or more files"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 4, # Multiple file mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog

def export_selected():
  export_dir = prompt_directory("Select export directory")

  for obj in pm.selected():
    export(obj, export_dir)

def export(obj, export_dir=""):
  base_name = str(obj).replace("_Geo", "")

  ass_export_path = os.path.join(export_dir, base_name + ".ass")
  fbx_export_path = os.path.join(export_dir, base_name + ".fbx")

  export_ass(obj, ass_export_path)
  export_fbx(obj, fbx_export_path)

def export_ass(obj, path):
  pm.select(obj)
  command = "arnoldExportAss -f \"%s\" -s -shadowLinks 1 -mask 2303 -lightLinks 1 -boundingBox -cam perspShape" % path
  mel.eval(command)

def export_fbx(obj, path):
  pm.select(obj)
  pm.exportSelected(
    path,
    force=True,
    typ="FBX export",
    options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1"
  )

def create_procedural(path_to_ass):
  base_name = os.path.splitext(os.path.basename(path_to_ass))[0]
  dirname = os.path.dirname(path_to_ass)
  path_to_fbx = os.path.join(dirname, base_name + ".fbx")

  if os.path.exists(path_to_fbx):
    geo_node = pm.importFile(
      path_to_fbx,
      namespace="standin",
      returnNewNodes=True,
    )[-1]
    print geo_node
    pm.rename(geo_node, base_name)
    geo_node.aiTranslator.set("procedural")
    geo_node.dso.set(path_to_ass)
  else:
    print "'%s' does not exist" % path_to_fbx

def import_procedurals():
  files = prompt_files("Select ASS files to import")
  for file in files:
    print "Importing " + file
    create_procedural(file)

# export_selected()
# import_procedurals()
