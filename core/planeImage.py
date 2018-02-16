import os
import pymel.core as pm

def createPlaneImage(alpha=False, imageSequence=False):
  dialog = pm.fileDialog2(okCaption = "Select",
                          fileMode = 1, # Single file mode
                          dialogStyle = 2, # Maya-style dialog
                          caption = "Select an image")
  imagePath = dialog[0]
  imageName = os.path.basename(imagePath)

  fileNode = pm.shadingNode("file",
                            name=imageName,
                            asTexture=True,
                            isColorManaged=True)
  fileNode.fileTextureName.set(imagePath)

  if imageSequence:
    fileNode.useFrameExtension.set(1) # Enable "Use image sequence"
    numFrames = len(os.listdir(os.path.dirname(imagePath)))
    pm.expression(object=fileNode,
                  string="frameExtension = frame %% %i" % numFrames)

  # Create shader
  shader = pm.shadingNode("aiStandardSurface",
                          asShader=True)
  shader.base.set(1)

  # Connect fileNode to shader
  pm.connectAttr(fileNode.outColor, shader.baseColor, force=True)

  # Create plane
  height = fileNode.outSizeY.get()
  width = fileNode.outSizeX.get()
  planeName = imageName.split(".")[0]
  plane = pm.polyPlane(name=planeName,
                       width=width/100,
                       height=height/100,
                       sw=1,
                       sh=1,
                       cuv=1)[0]

  if alpha:
    pm.connectAttr(fileNode.outAlpha, shader.opacityR, force=True)
    pm.connectAttr(fileNode.outAlpha, shader.opacityG, force=True)
    pm.connectAttr(fileNode.outAlpha, shader.opacityB, force=True)
    plane.aiOpaque.set(0)

  _assignShader(plane, shader)

def _assignShader(mesh, shader):
  pm.select(mesh.getShape())
  pm.hyperShade(assign=shader)
