import fnmatch
import os
import re
import sys

import pymel.core as pm
from .. import util

class RedshiftPlugSubstance:
  """
  RedshiftPlugSubstance automatically connects a RedshiftMaterial shader
  to textures exported from Substance Painter. Expects files for one
  material to be contained in their own directory.
  """

  VALID_EXTENSIONS = [
    ".png",
    ".tif",
    ".tiff",
    ".exr",
    ".hdr",
    ".tga",
  ]

  def __init__(self, material):
    try:
      self.shader = material
      self.directory = None
      self.filenames = {}
      if self.launchFileBrowser():
        self.connectDirectory()

  def launchFileBrowser(self):
    directory = pm.fileDialog2(
      okCaption = "Select",
      fileMode = 3, # Directory mode
      dialogStyle = 2, # Maya-style dialog
      caption = "Select texture directory for %s" % self.shader,
    )
    success = directory and len(directory)
    if success:
      self.directory = directory[0]
    return success

  def connectDirectory(self):
    for root, _, filenames in os.walk(self.directory):
      for filename in filenames:
        name, extension = os.path.splitext(filename)
        mapType, udim = self.parseFileName(name)
        if mapType and extension in self.VALID_EXTENSIONS:
          fullPath = os.path.join(root, filename)
          self.connectTexture(fullPath, mapType)
        else:
          util.log("Skipping invalid file %s" % filename)

  def parseFileName(self, filename):
    name = filename.split(".")[0]
    udim = filename.split(".")[1]
    matches = re.match(r"(?:.+)_(.+)", name)
    mapType = matches.group(1) if matches else None
    return [mapType, udim]

  def connectTexture(self, path, mapType):
    try:
      connector = getattr(self, "connect%s" % mapType)
      fileNode = self.createFileNode(path)
      connector(fileNode)
    except AttributeError:
      util.log("Connector %s not found for %s" % (mapType, path))

  def connect(self, attr_1, attr_2):
    pm.connectAttr(attr_1, attr_2, force=True)

  def connectAlpha(self, attr, fileNode):
    fileNode.alphaIsLuminance.set(1)
    self.connect(fileNode.outAlpha, self.shader.attr(attr))

  def connectColor(self, attr, fileNode):
    self.connect(fileNode.outColor, self.shader.attr(attr))

  def createFileNode(self, path):
    fileNode = pm.shadingNode(
                  "file",
                  name=os.path.basename(path),
                  asTexture=True,
                  isColorManaged=True,
                )
    fileNode.fileTextureName.set(path)
    return fileNode

  def connectNormal(self, fileNode):
    bumpNode = pm.shadingNode("RedshiftBumpMap", asUtility=True)
    bumpNode.inputType.set(1) # Tangent Space Normals
    bumpNode.flipY.set(1) # Flip Normal Y
    self.connect(fileNode.outColor, bumpNode.input)
    self.connect(bumpNode.out, self.shader.bump_input)

  def connectDiffuse(self, fileNode):
    self.connectColor("diffuse_color", fileNode)

  def connectBaseColor(self, fileNode):
    self.connectDiffuse(fileNode)

  def connectRoughness(self, fileNode):
    self.connectAlpha("refl_roughness", fileNode)

  def connectReflection(self, fileNode):
    self.connectAlpha("refl_weight", fileNode)
    self.connectColor("refl_color", fileNode)

  def connectEmission(self, fileNode):
    self.connectAlpha("emission_weight", fileNode)
    self.connectColor("emission_color", fileNode)

  def connectOpacity(self, fileNode):
    self.connectColor("opacity_color", fileNode)

  def connectMetalness(self, fileNode):
    self.shader.refl_fresnel_mode.set(2) # Metalness fresnel type
    self.connectAlpha("refl_metalness", fileNode)

  def connectHeight(self, fileNode):
    displacementShader = pm.shadingNode("displacementShader", asShader=True)
    displacementShader.scale.set(0)
    surfaceShader = self.shader.listConnections(type="shadingEngine")[0]
    self.connect(
      fileNode.outAlpha,
      displacementShader.attr("displacement"),
    )
    self.connect(
      displacementShader.attr("displacement"),
      surfaceShader.attr("displacementShader"),
    )
    fileNode.alphaIsLuminance.set(1)
