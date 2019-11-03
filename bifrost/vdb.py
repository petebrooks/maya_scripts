import pymel.core as pm

def exportFoam(foamProperties = None):
  bifrostFileNode = pm.createNode("BE_BifrostFileToArray")
  vdbParticlesNode = pm.createNode("BE_VDBFromParticles")
  vdbWriteNode = pm.createNode("BE_VDBWrite")
  foamProperties = foamProperties or pm.selected()

  vdbParticlesNode.ExportDistanceVDB.set(False)
  vdbParticlesNode.ExportVelocityVDB.set(True)
  vdbParticlesNode.VelocityGridName.set("velocity")
  bifrostFileNode.useFrameExtension.set(True)

  pm.connectAttr(bifrostFileNode.outPosition, vdbParticlesNode.PointInput, force=True)
  pm.connectAttr(bifrostFileNode.AttributesOut[3], vdbParticlesNode.VelocityInput, force=True)
  pm.connectAttr(vdbParticlesNode.VdbOutput, vdbWriteNode.VdbInput, force=True)

  # TODO:
  # - Prompt for input file
  # - Prompt for output file
  # - Actually play scene
