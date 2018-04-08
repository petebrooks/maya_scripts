import pymel.core as pm
import maya.cmds as cmds
import sys
import numpy

def create(relativeToObj=None,
           points=8,
           name=None,
           color=None,
           limitX=None,
           limitY=None,
           limitZ=None):
  """Creates a pointy control curve"""

  sections = points * 2
  curve = pm.circle(sections=sections, nr=(0, 1, 0))[0]

  # Select every other CV
  selection = []
  for cv in range(0, sections, 2):
    selection.append(str(curve) + ".cv[%i]" % cv)
  cmds.select(selection, r=True)

  pm.mel.eval("scale -r -p 0cm 0cm 0cm 0.192404 0.192404 0.192404")

  if relativeToObj:
    _transformRelativeToObj(curve, relativeToObj)

  if color:
    _overrideColor(curve, color)

  if name:
    pm.rename(curve, name)

  _limitTransforms(curve, limitX=limitX, limitY=limitY, limitZ=limitZ)

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

def _limitTransforms(obj, limitX=None, limitY=None, limitZ=None):
  if limitX:
    pm.transformLimits(obj, etx=(True, True), tx=limitX)
  if limitY:
    pm.transformLimits(obj, ety=(True, True), ty=limitY)
  if limitZ:
    pm.transformLimits(obj, etz=(True, True), tz=limitZ)

def _transformRelativeToObj(curve, relativeToObj):
  # Move curve above object
  objY = pm.xform(relativeToObj, query=True, boundingBox=True)[4]
  pm.xform(curve, translation=(0, objY, 0))

  # Scale to match object size
  # TODO: Does this work well at any scale? With oblong footprints?
  boundingBox = pm.xform(relativeToObj, query=True, boundingBox=True)
  scaleValue = numpy.mean([
    abs(boundingBox[0]),
    abs(boundingBox[2]),
    abs(boundingBox[3]),
    abs(boundingBox[5]),
  ]) / 2
  pm.scale(curve, scaleValue, scaleValue, scaleValue)

