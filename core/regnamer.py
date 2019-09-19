# REGNAMER
# (The g is silent.)

import re
import pymel.core as pm

def rename_from_parent(mesh, suffix):
  parent = mesh.listRelatives(parent=True)[0]
  name = mesh_basename(parent) + suffix
  pm.rename(mesh, name)

def mesh_basename(mesh):
  return re.match(r"(.+)_(?:Geo|(?:s_)?lo).*", str(mesh)).group(1)

def fixFBXNames(meshes=None):
  meshes = meshes or pm.selected()
  for mesh in meshes:
    newName = str(mesh).replace("FBXASC032", "_")
    print "Renaming %s to %s" % (mesh, newName)
    pm.rename(mesh, newName)
