import pymel.core as pm
import maya.cmds as cmds
import sys
import numpy

def create(relativeToObj=None, points=8, color=None):
  sections = points * 2
  curve = pm.circle(sections=sections, nr=(0, 1, 0))[0]

  # Select every other CV
  selection = []
  for cv in range(0, sections, 2):
    selection.append(str(curve) + ".cv[%i]" % cv)
  cmds.select(selection, r=True)

  pm.mel.eval("scale -r -p 0cm 0cm 0cm 0.192404 0.192404 0.192404")

  if relativeToObj:
    # Move curve above object
    objY = pm.xform(relativeToObj, query=True, boundingBox=True)[4]
    pm.xform(curve, translation=(0, objY, 0))
    # Scale to match object size
    boundingBox = pm.xform(relativeToObj, query=True, boundingBox=True)
    scaleValue = numpy.mean([
      abs(boundingBox[0]),
      abs(boundingBox[2]),
      abs(boundingBox[3]),
      abs(boundingBox[5]),
    ]) / 2
    pm.scale(curve, scaleValue, scaleValue, scaleValue)

  if color:
    _overrideColor(curve, color)

  return curve

def _overrideColor(obj, color):
  obj.overrideEnabled.set(True)
  colorNameToIndex = {
    "yellow": 17,
    "blue": 6,
    "red": 13,
  }
  if isinstance(color, int):
    index = color
  else:
    index = colorNameToIndex[color]

  if not index:
    sys.stdout.log("`color` must be an integer or color name. Valid color names are: %s" % " ".join(colorNameToIndex.keys()))
    return

  obj.overrideColor.set(index)
