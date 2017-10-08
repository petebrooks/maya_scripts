from fnmatch import fnmatch

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

      print str(node)
      print str(node).endswith("_s_lo")
      if str(node).endswith("_s_lo"):
        pm.polySmooth(dup, divisions=divisions)
    elif isTransform(node):
      pm.parent(groupToHiPoly(node), hiPolyGroup)

  return hiPolyGroup

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

def getTransform(shape):
  if shape.nodeType() == "mesh":
    parents = pm.listRelatives(shape, parent=True, type="transform")
    return parents[0]
  else:
    return None

import os

def export_for_painter(lo_poly_group):
  directory = prompt_for_directory()
  base_name = group_basename(lo_poly_group)
  base_path = os.path.join(directory, base_name)

  hi_poly_group = groupToHiPoly(lo_poly_group)

  lo_poly_name = base_path + "_lo.fbx"
  export_fbx(lo_poly_group, lo_poly_name)
  print "Exported lo poly group to %s" % lo_poly_name

  hi_poly_name = base_path + "_hi.fbx"
  export_fbx(hi_poly_group, hi_poly_name)
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


export_for_painter(pm.selected()[0])
