from PIL import Image
import os

def prompt_file(caption="Select file"):
  dialog = pm.fileDialog2(
    okCaption = "Select",
    fileMode = 1, # Single file mode
    dialogStyle = 2, # Maya-style dialog
    caption = caption
  )
  return dialog[0]

class PlaneImage(object):
  """docstring for PlaneImage"""
  def __init__(self, image_path):
    self.image_path = image_path
    self.image = Image.open(image_path)

  def create(self):
    plane = self.create_plane()
    material = self.create_material()
    self.assign_material(plane, material)

  def create_plane(self):
    width, height = self.image.size
    return pm.polyPlane(
      height=height/100,
      width=width/100,
      createUVs=1,
    )

  def create_material(self):
    # name = self.generate_shader_name()
    shader = pm.shadingNode(
      "aiStandardSurface",
      asShader=True,
      # name=name,
    )
    file_node = pm.shadingNode(
      "file",
      name=os.path.basename(self.image_path),
      asTexture=True,
      isColorManaged=True,
    )
    file_node.fileTextureName.set(self.image_path)
    pm.connectAttr(file_node.outColor, shader.baseColor, force=True)
    return shader

  def assign_material(self, mesh):
    pm.select(mesh)
    pm.hyperShade(assign=shader)

  def generate_shader_name(self):
    n = 1
    name = "plane_image_" + n + "_Mat"
    exists = len(pm.ls(name)) > 1
    while exists:
      n += 1
      name = "plane_image_" + n + "_Mat"
      exists = len(pm.ls(name)) > 1

image_path = prompt_file
PlaneImage(image_path)
