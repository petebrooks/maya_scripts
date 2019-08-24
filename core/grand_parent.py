import pymel.core as pm

def grandparent(mesh):
  parent = _findParent(mesh)
  grandparent = _findParent(parent)

  if grandparent:
    pm.parent(mesh, grandparent)
  else:
    pm.parent(mesh, world=True)

  if _isGroup(parent) and _isEmpty(parent):
    pm.delete(parent)

def _findParent(node):
  return node and node.listRelatives(parent=True)[0]

def _isGroup(node):
  return _isTransform(node) and not node.getShape()

def _isTransform(node):
  return node and node.nodeType() == "transform"

def _isEmpty(node):
  return not len(node.listRelatives(children=True))
