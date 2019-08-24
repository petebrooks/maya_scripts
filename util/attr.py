import maya.cmds as cmds

def exists(node, attr):
  return cmds.attributeQuery(attr, node=str(node), exists=True)