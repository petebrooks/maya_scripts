import pymel.core as pm

def grandparent(mesh):
  parent = find_parent(mesh)
  grandparent = find_parent(parent)

  if grandparent:
    pm.parent(mesh, grandparent)
  else:
    pm.parent(mesh, world=True)

  if is_group(parent) and is_empty(parent):
    pm.delete(parent)

def find_parent(node):
  return node and node.listRelatives(parent=True)[0]

def is_group(node):
  return is_transform(node) and not node.getShape()

def is_transform(node):
  return node and node.nodeType() == "transform"

def is_empty(node):
  return not len(node.listRelatives(children=True))
