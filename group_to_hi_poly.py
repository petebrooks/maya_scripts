import pymel.core as pm

def groupToHiPoly(loPolyGroup, renameGroup=True):
  hiPolyGroupName = toHiPolyName(loPolyGroup)

  if len(pm.ls(hiPolyGroupName)):
    pm.delete(hiPolyGroupName)

  hiPolyGroup = pm.group(name=hiPolyGroupName, world=True, empty=True)

  for node in pm.listRelatives(loPolyGroup, children=True):
    if isPolyMeshTransform(node):
      dup = pm.duplicate(node,
                         name=toHiPolyName(node),
                         returnRootsOnly=True,
                         upstreamNodes=True)
      pm.parent(dup, hiPolyGroup)
      pm.polySmooth(dup, divisions=3)
    elif isTransform(node):
      pm.parent(groupToHiPoly(node), hiPolyGroup)

  return hiPolyGroup

def toHiPolyName(loPoly):
  baseName = str(loPoly).replace("_lo", "")
  return baseName + "_hi"

def isPolyMeshTransform(node):
  return isTransform(node) and isMesh(node.getShape())

def isTransform(node):
  return node and node.nodeType() == "transform"

def isMesh(node):
  return node and node.nodeType() == "mesh"

def getTransform(shape):
  if shape.nodeType() == "mesh":
    parents = pm.listRelatives(shape, parent=True, type="transform")
    return parents[0]
  else:
    return None

loPolyGroup = pm.ls(sl=True, transforms=True)[0]
print "Working..."
groupToHiPoly(loPolyGroup)
