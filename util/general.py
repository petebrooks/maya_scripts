import os
import subprocess
import pymel.core as pm

def safeParent(child_node, parent_node):
  if parent_node:
    return pm.parent(child_node, parent_node)
  else:
    return pm.parent(child_node, world=True)

def safeGetShape(transformOrShape):
  if transformOrShape.nodeType() == "mesh":
    return transformOrShape
  else:
    return transformOrShape.getShape()

def listMaterials(transformOrShape):
  shape = safeGetShape(transformOrShape)
  shading_engines = pm.listConnections(shape)
  return pm.ls(pm.listConnections(shading_engines), materials=True)

def sceneName():
  scenePath = pm.sceneName()
  sceneFile = os.path.basename(scenePath)
  return os.path.splitext(sceneFile)[0]

def sceneDir():
  return os.path.dirname(pm.sceneName())

def openSceneDir():
  subprocess.call([
    "open",
    sceneDir(),
  ])

def selectMaterials(objects):
  materials = []
  for object in objects:
    for material in listMaterials(object):
      if not str(material).startswith("displacementShader"):
        materials.append(material)
  pm.select(list(set(materials)))
  return materials

def switchPosition(object1, object2):
  pass # TODO
