##################################################
# clone and replace
##################################################
# Clone source object for each target object, and replace targets
# with instances.
#
# Select source object, then one or more target objects.

import pymel.core as pm

def andReplace(keepNames=True, instance=False, position=True, rotation=True, scale=True):
  selected = pm.selected()
  source = selected.pop(0)
  for target in selected:
    if instance:
      clone = pm.instance(source)[0]
    else:
      clone = pm.duplicate(source, renameChildren=True)[0]
    pm.matchTransform(
      clone,
      target,
      position=position,
      rotation=rotation,
      scale=scale,
    )
    parent = _firstOrNone(pm.listRelatives(target, parent=True))
    _safeParent(clone, parent)
    pm.delete(target)
    if keepNames:
      pm.rename(clone, target)

def andMatch(keepNames=True, instance=False, position=True, rotation=True, scale=True):
  selected = pm.selected()
  source = selected.pop(0)
  for target in selected:
    if instance:
      clone = pm.instance(source)[0]
    else:
      clone = pm.duplicate(source, renameChildren=True)[0]
    pm.matchTransform(
      clone,
      target,
      position=position,
      rotation=rotation,
      scale=scale,
    )
    parent = _firstOrNone(pm.listRelatives(target, parent=True))
    _safeParent(clone, parent)

def _firstOrNone(list):
  if len(list):
    return list[0]
  else:
    return None

def _safeParent(child, prent):
  if prent:
    pm.parent(child, prent)
  else:
    pm.parent(child, world=True)
