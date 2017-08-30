##################################################
# Instance and replace
##################################################
# Instance source object for each target object, and replace targets
# with instances.
#
# Select source object, then one or more target objects.

import pymel.core as pm

def cloneAndReplace(keepNames=True, instance=False):
  sel = pm.selected()
  source = sel.pop(0)
  for target in sel:
    print instance
    if instance:
      clone = pm.instance(source)[0]
    else:
      clone = pm.duplicate(source)[0]
    pm.matchTransform(clone, target)
    parent = firstOrNone(pm.listRelatives(target, parent=True))
    safeParent(clone, parent)
    pm.delete(target)
    if keepNames:
      pm.rename(clone, target)

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

cloneAndReplace()
