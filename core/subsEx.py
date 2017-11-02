from fnmatch import fnmatch
import re
import pymel.core as pm

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
  baseName = str(loPoly).replace("_lo", "")
  return baseName + "_hi"

def isPolyMeshTransform(node):
  return isTransform(node) and isMesh(node.getShape())

def isTransform(node):
  return node and node.nodeType() == "transform"

def isMesh(node):
  return node and node.nodeType() == "mesh"

def isInstance(node):
  pm.PyNode(node).isInstanced()

def getTransform(shape):
  if shape.nodeType() == "mesh":
    parents = pm.listRelatives(shape, parent=True, type="transform")
    return parents[0]
  else:
    return None

import os

def export_for_painter(group, old_workflow=False):
  if old_workflow:
    return export_old_workflow(group)

  directory = prompt_for_directory()
  export_path = os.path.join(directory, str(group) + ".fbx")

  hi_poly_group = groupToHiPoly(group)
  export_fbx(hi_poly_group, export_path)
  print "Exported group to: %s" % export_path
  pm.delete(hi_poly_group)

def export_old_workflow(lo_poly_group):
  directory = prompt_for_directory()
  base_name = group_basename(lo_poly_group)
  base_path = os.path.join(directory, base_name)

  lo_poly_name = base_path + "_lo.fbx"
  export_fbx(lo_poly_group, lo_poly_name)
  print "Exported lo poly group to %s" % lo_poly_name

  hi_poly_group = groupToHiPoly(lo_poly_group)
  hi_poly_name = base_path + "_hi.fbx"
  export_fbx(hi_poly_group, hi_poly_name)
  pm.delete(hi_poly_group)
  print "Exported hi poly group to %s" % hi_poly_name


def export_fbx(mesh, path):
  pm.select(mesh)
  return pm.exportSelected(
    path,
    force=True,
    typ="FBX export",
    options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"
  )

def prompt_for_directory(caption="Select a directory"):
  selection = pm.fileDialog2(
    okCaption="Select",
    fileMode=3, # Directory mode
    dialogStyle=2, # Maya-style dialog
    caption=caption,
  )
  return selection[0]

def group_basename(group):
  matches = re.match(r"(.+)(?:_Grp?|_lo?).*", str(group))
  if matches:
    return matches.group(1)
  else:
    return str(group)


# export_for_painter(pm.selected()[0], old_workflow=True)


# TODO
# - Add way to specify export file names
