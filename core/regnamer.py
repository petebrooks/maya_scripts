# REGNAMER
# (The g is silent.)

import re

def rename_from_parent(mesh, suffix):
  parent = mesh.listRelatives(parent=True)[0]
  name = mesh_basename(parent) + suffix
  pm.rename(mesh, name)

def mesh_basename(mesh):
  return re.match(r"(.+)_(?:Geo|(?:s_)?lo).*", str(mesh)).group(1)

for mesh in pm.selected():
  rename_from_parent(mesh, "_Cap")
