from fnmatch import fnmatch

import pymel.core as pm
import re

# Usage:
# loPolyGroup = pm.ls(sl=True, transforms=True)[0]
# groupToHiPoly(loPolyGroup)
#
# toHiPolyGroup(pm.selected())
# groupToHiPoly(pm.selected()[0])


def groupToHiPoly(loPolyGroup,
                  divisions=1,
                  exclude=None):
  hiPolyGroupName = toHiPolyName(loPolyGroup)

  if len(pm.ls(hiPolyGroupName)):
    pm.delete(hiPolyGroupName)

  geoNodes = pm.listRelatives(loPolyGroup, children=True)
  return toHiPolyGroup(geoNodes,
                       name=hiPolyGroupName,
                       divisions=divisions,
                       exclude=exclude)

def toHiPolyGroup(nodes,
                  name="hiPoly_Grp_1",
                  divisions=1,
                  exclude=None):
  hiPolyGroup = pm.group(name=name, world=True, empty=True)

  for node in nodes:
    if isPolyMeshTransform(node):
      dup = pm.duplicate(node,
                         name=toHiPolyName(node),
                         returnRootsOnly=True,
                         upstreamNodes=True)[0]
      pm.parent(dup, hiPolyGroup)

      if isSmoothed(node):
        pm.polySmooth(dup, divisions=divisions)
    elif isTransform(node):
      pm.parent(groupToHiPoly(node), hiPolyGroup)

  return hiPolyGroup

def isSmoothed(mesh):
  return not not mesh.aiSubdivType.get()

def matchPatterns(node, pattern):
  if fnmatch(str(node), pattern):
    return True
  return False

def toHiPolyName(loPoly):
  return mesh_basename(loPoly) + "_hi"

def mesh_basename(mesh):
  return re.match(r"(?:.*\|)?(.+)_(?:Geo|lo).*", str(mesh)).group(1)

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

groupToHiPoly(pm.selected()[0])

# for mesh in pm.selected():
#   print mesh
#   print "\t" + toHiPolyName(mesh)
#   print "\t" + str(isSmoothed(mesh))

# file -force -options "v=0;" -typ "FBX export" -pr -es "/Volumes/Promise Pegasus/maya/projects/realest_estate/scenes/club_moss/substance/clubFloor_hi.fbx";

# TODO:
# - Auto export
