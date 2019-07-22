from .. import util
from fnmatch import fnmatch
import re
import pymel.core as pm
import maya.cmds as cmds
import os
import sys

# Export selected nodes for substance Painter.
# Creates two FBX files, one hi-poly and one lo-poly.
# Smooths any meshes that have subdivisions enabled in Arnold or Redshift.
# TODO:
# - Catch error and delete temp nodes
def exportForPainter(nodesOrSet, lo=True, hi=True):
  if isinstance(nodesOrSet, pm.nodetypes.ObjectSet):
    nodes = nodesOrSet.members()
  else:
    nodes = nodesOrSet

  sys.stdout.write("%i nodes selected" % len(nodes))

  exportName = _getExportName()
  if not exportName:
    sys.stdout.write("Aborting due to empty exportName.")
    return False

  directory = _promptForDirectory()
  if not directory:
    sys.stdout.write("Aborting due to empty directory.")
    return False

  if lo:
    _exportLoPoly(nodes, exportName, directory)
  if hi:
    _exportHiPoly(nodes, exportName, directory)

def _exportLoPoly(nodes, exportName, directory):
  loExportPath = os.path.join(directory, exportName + "_lo.fbx")
  loPolyNodes = dupAndSmoothNodes(nodes,
                                  suffix="_lo",
                                  divisions=2)
  _exportFbx(loPolyNodes, loExportPath)
  sys.stdout.write("Exported lo poly group to: %s" % loExportPath)
  pm.delete(loPolyNodes)

def _exportHiPoly(nodes, exportName, directory):
  hiExportPath = os.path.join(directory, exportName + "_hi.fbx")
  hiPolyNodes = dupAndSmoothNodes(nodes,
                                  suffix="_hi",
                                  divisions=4)
  _exportFbx(hiPolyNodes, hiExportPath)
  sys.stdout.write("Exported hi poly group to: %s" % hiExportPath)
  pm.delete(hiPolyNodes)

def dupAndSmoothNodes(nodes,
                      suffix="",
                      groupName="smoothed_group_1",
                      divisions=1):
  smoothNodes = []
  for node in nodes:
    if _isPolyMeshTransform(node):
      newName = _toBasename(node) + suffix
      dup = pm.duplicate(node,
                         name=newName,
                         returnRootsOnly=True,
                         upstreamNodes=True)[0]
      if _isSmoothed(node):
        pm.polySmooth(dup, divisions=divisions)
      smoothNodes.append(dup)

  return smoothNodes

def _isSmoothed(mesh):
  shape = mesh.getShape()
  if util.attr.exists(shape, "rsEnableSubdivision"):
    return shape.rsEnableSubdivision.get() != 0
  elif util.attr.exists(shape, "aiSubdivType"):
    return shape.aiSubdivType.get() != 0

def _matchPatterns(node, pattern):
  if fnmatch(str(node), pattern):
    return True
  return False

def _toBasename(node):
  matches = re.match(r"(.+?)_(?:hi|lo)", str(node))
  if matches:
    return matches.group(1)
  return str(node)

def _toHiPolyName(loPoly):
  return _toBasename(loPoly) + "_hi"

def _isPolyMeshTransform(node):
  return _isTransform(node) and _isMesh(node.getShape())

def _isTransform(node):
  return node and node.nodeType() == "transform"

def _isMesh(node):
  return node and node.nodeType() == "mesh"

def _isInstance(node):
  pm.PyNode(node).isInstanced()

def _getTransform(shape):
  if shape.nodeType() == "mesh":
    parents = pm.listRelatives(shape, parent=True, type="transform")
    return parents[0]
  else:
    return None

def _exportFbx(nodes, path):
  pm.select(nodes)
  return pm.exportSelected(
    path,
    force=True,
    typ="FBX export",
    options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"
  )

def _promptForDirectory(caption="Select a directory"):
  selection = pm.fileDialog2(
    okCaption="Select",
    fileMode=3, # Directory mode
    dialogStyle=2, # Maya-style dialog
    caption=caption,
  )
  return selection[0]

def _groupBasename(group):
  matches = re.match(r"(.+)(?:_Grp?|_lo?).*", str(group))
  if matches:
    return matches.group(1)
  else:
    return str(group)

def _getExportName():
  result = cmds.promptDialog(
    title="Export Name",
    text=util.sceneName(),
    message="Enter name:",
    button=["OK", "Cancel"],
    defaultButton="OK",
    cancelButton="Cancel",
    dismissString="Cancel"
  )

  if result == "OK":
    return pm.promptDialog(query=True, text=True)
  else:
    return "export"

# TODO
# - Add way to specify export file names
