import pymel.core as pm

def groupToHiPoly():
  loPolyGroup = pm.ls(sl=True, transforms=True)[0]
  hiPolyGroupName = toHiPolyName(loPolyGroup)

  if len(pm.ls(hiPolyGroupName)):
    pm.delete(hiPolyGroupName)
  hiPolyGroup = pm.group(name=hiPolyGroupName, world=True, empty=True)

  for node in pm.listRelatives(loPolyGroup, allDescendents=True, shapes=True):
    transform = getTransform(node)
    if transform:
      dup = pm.duplicate(transform,
                         name=toHiPolyName(transform),
                         returnRootsOnly=True,
                         upstreamNodes=True)
      pm.parent(dup, hiPolyGroup)
      pm.polySmooth(dup, divisions=3)

def toHiPolyName(loPoly):
  baseName = str(loPoly).replace("_lo", "")
  return baseName + "_hi"

# def isPolyMeshTransform(node):
#   node.getShape() and node.getShape().nodeType() == "mesh"

def getTransform(shape):
  if shape.nodeType() == "mesh":
    parents = pm.listRelatives(shape, parent=True, type="transform")
    return parents[0]
  else:
    return None

groupToHiPoly()
