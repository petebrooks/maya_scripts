import pymel.core as pm
from ..util import general

def children(objects=None):
  objects = objects or pm.selected()
  children = []
  for obj in objects:
    children.append(pm.listRelatives(obj, children=True))
  pm.select(children)

def materials(objects=None):
  objects = objects or pm.selected()
  materials = []
  for object in objects:
    for material in general.listMaterials(object):
      if not str(material).startswith("displacementShader"):
        materials.append(material)
  pm.select(list(set(materials)))
  return materials

def objectsWithMaterial(material):
  pm.hyperShade(objects = material)
  return pm.selected()