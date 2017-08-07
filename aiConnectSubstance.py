import pymel.core as pm
import sys
import fnmatch
import os

class AiPlugSubstance:
  """TODO: docstring for AiPlugSubstance"""
  def __init__(self):
    try:
      self.ai_material = pm.ls(sl=True, materials=True)[0]
      self.directory = None
      self.filenames = {}
      self.launch_file_browser()
    except IndexError:
      sys.stdout.write("Select a material")


  def launch_file_browser(self):
    pm.fileBrowserDialog(mode=4, # directories mode
                         fileCommand=self.plug,
                         fileType="image")

  def plug(self, directory, _type):
    self.directory = directory
    self.filenames = {
      "baseColor": self.filename_for_map("BaseColor"),
      "roughness": self.filename_for_map("Roughness"),
      "normal": self.filename_for_map("Normal"),
      "metalness": self.filename_for_map("Metalness"),
      "metalness": self.filename_for_map("Metallic"),
      "emissive": self.filename_for_map("Emissive"),
      "height": self.filename_for_map("Height"),
    }

    for attr, file in self.filenames.items():
      if file:
        self.connect_texture(attr, file)

  def filename_for_map(self, map_type):
    matches = self.search_directory(map_type)
    if len(matches):
      return matches[0]
    else:
      return None

  def search_directory(self, map_type):
    matches = []
    for root, dirnames, filenames in os.walk(self.directory):
        search_string = "*%s*.png" % map_type
        for filename in fnmatch.filter(filenames, search_string):
            matches.append(os.path.join(root, filename))
    return matches

  def connect(self, attr_1, attr_2):
    pm.connectAttr(attr_1, attr_2, force=True)

  def connect_alpha(self, attr, file_node):
    file_node.alphaIsLuminance.set(1)
    self.connect(file_node.outAlpha, self.ai_material.attr(attr))

  def connect_color(self, attr, file_node):
    self.connect(file_node.outColor, self.ai_material.attr(attr))

  def connect_normal(self, file_node):
    bump_node = pm.shadingNode("bump2d", asUtility=True)
    bump_node.bumpInterp.set(1) # Tangent Space Normals
    self.connect(file_node.outAlpha, bump_node.bumpValue)
    self.connect(bump_node.outNormal, self.ai_material.normalCamera)

  def connect_texture(self, attr, file):
    file_node = pm.shadingNode(
                  "file",
                  name=os.path.basename(file),
                  asTexture=True
                )

    if attr == "baseColor":
      self.connect_color("baseColor", file_node)
    elif attr == "normal":
      self.connect_normal(file_node)
    elif attr == "roughness":
      self.connect_alpha("specularRoughness", file_node)
    elif attr == "metalness":
      self.connect_alpha("metalness", file_node)
    elif attr == "emission":
      self.connect_alpha("emission", file_node)
    # elif attr == "height":
      # TODO

AiPlugSubstance()
