##################################################
# Instance and replace
##################################################
# Instance source object for each target object, and replace targets
# with instances.
#
# Select source object, then one or more target objects.

import pymel.core as pm

def instanceAndReplace():
  sel = pm.ls(sl=True)
  source = sel[0]
  for target in sel[1:len(sel)]:
    dup = pm.instance(source)
    pm.matchTransform(dup, target)
    parent = firstOrNone(pm.listRelatives(target, parent=True))
    safeParent(dup, parent)
    pm.delete(target)

def firstOrNone(list):
  try:
    return list[0]
  except IndexError:
    return None

def safeParent(child, prent):
  if prent:
    pm.parent(child, prent)
  else:
    pm.parent(child, world=True)

instanceAndReplace()
