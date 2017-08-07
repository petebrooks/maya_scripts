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

  def connect_texture(self, attr, file):
    file_node = pm.shadingNode("file", name=os.path.basename(file), asTexture=True)

    if attr == "baseColor":
      file_attr_name = "%s.outColor" % str(file_node)
      ai_attr_name = "%s.%s" % (self.ai_material, attr)
      pm.connectAttr(file_attr_name, ai_attr_name, force=True)
    elif attr == "normal":
      file_attr_name = "%s.outAlpha" % str(file_node)
      ai_attr_name = "%s.normalCamera" % self.ai_material
      bump_node = pm.shadingNode("bump2d", asUtility=True)
      bump_node.bumpInterp.set(1) # Tangent Space Normals
      pm.connectAttr(file_attr_name, str(bump_node) + ".bumpValue", force=True)
      pm.connectAttr(str(bump_node) + ".outNormal", ai_attr_name, force=True)
    elif attr == "roughness":
      file_attr_name = "%s.outAlpha" % str(file_node)
      ai_attr_name = "%s.specularRoughness" % self.ai_material
      file_node.alphaIsLuminance.set(1)
      pm.connectAttr(file_attr_name, ai_attr_name, force=True)
    elif attr == "metalness":
      file_attr_name = "%s.outAlpha" % str(file_node)
      ai_attr_name = "%s.metalness" % self.ai_material
      file_node.alphaIsLuminance.set(1)
      pm.connectAttr(file_attr_name, ai_attr_name, force=True)
    elif attr == "emission":
      file_attr_name = "%s.outAlpha" % str(file_node)
      ai_attr_name = "%s.emission" % self.ai_material
      file_node.alphaIsLuminance.set(1)
      pm.connectAttr(file_attr_name, ai_attr_name, force=True)
    # elif attr == "height":
      # TODO

AiPlugSubstance()
