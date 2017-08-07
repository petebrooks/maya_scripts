import pymel.core as pm

def groupToHiPoly():
  loPolyGroup = pm.ls(sl=True, transforms=True)[0]
  hiPolyGroupName = toHiPolyName(loPolyGroup)

  if len(pm.ls(hiPolyGroupName)):
    pm.delete(hiPolyGroupName)
  hiPolyGroup = pm.group(name=hiPolyGroupName, world=True, empty=True)

  for shape in pm.listRelatives(loPolyGroup, children=True):
    dup = pm.duplicate(shape,
                       name = toHiPolyName(shape),
                       returnRootsOnly=True,
                       upstreamNodes=True)
    pm.parent(dup, hiPolyGroup)
    pm.polySmooth(dup, divisions=3)

def toHiPolyName(loPoly):
  baseName = str(loPoly).replace("_lo", "")
  return baseName + "_hi"

groupToHiPoly()
