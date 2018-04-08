import pymel.core as pm
from mine import curve

def create(geo, color="yellow", boundary=10, useTranslate=False):
  """Creates a rig that squashes geo in Y and bends geo in X and Z"""

  squashDeformer, squashDeformerTransform = _squashDeformer(geo)
  bendDeformerX, bendDeformerXTransform = _bendDeformer(geo, "x")
  bendDeformerZ, bendDeformerZTransform = _bendDeformer(geo, "z")

  controlCurve = curve.pointy.create(
    relativeToObj=geo,
    color=color,
    limitX=(-boundary, boundary),
    limitZ=(-boundary, boundary),
    name=str(geo) + "_ctrl",
  )

  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=boundary, value=50)
  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=-boundary, value=-50)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=boundary, value=50)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=-boundary, value=-50)

  if useTranslate:
    pm.setDrivenKeyframe(squashDeformer.factor, currentDriver=controlCurve.translateY, driverValue=controlCurve.ty.get() * 3, value=2.4)
    pm.setDrivenKeyframe(squashDeformer.factor, currentDriver=controlCurve.translateY, driverValue=controlCurve.ty.get() / 3, value=-1.5)
    controlCurve.translateY.lock()
  else:
    pm.addAttr(controlCurve, longName="squash", attributeType="double", keyable=True)
    pm.connectAttr(controlCurve.squash, squashDeformer.factor)

  _lockAndHide(controlCurve, "rotateX", "rotateY", "rotateZ")
  _hide(controlCurve, "scaleX", "scaleY", "scaleZ")

  controlCurve.scale.lock()

  pm.parent(controlCurve, geo)
  pm.parent(squashDeformerTransform, geo)
  pm.parent(bendDeformerXTransform, geo)
  pm.parent(bendDeformerZTransform, geo)
  pm.select(controlCurve)

def _squashDeformer(geo):
  squash, squashHandle = pm.nonLinear(
    geo,
    type="squash",
    lowBound=0,
    highBound=2,
  )

  name = str(geo) + "_squash"
  pm.rename(squash, name)
  pm.rename(squashHandle, name + "Handle")
  squashHandle.hide()

  _matchTranslation(squashHandle, geo)

  return (squash, squashHandle)

def _bendDeformer(geo, axis):
  rotationsForAxis = {
    "x": 0,
    "z": -90,
  }

  bend, bendHandle = pm.nonLinear(
    geo,
    type="bend",
    lowBound=0,
  )

  name = str(geo) + "_bend" + axis.upper()
  pm.rename(bend, name)
  pm.rename(bendHandle, name + "Handle")
  bendHandle.hide()

  _matchTranslation(bendHandle, geo)
  bendHandle.rotateY.set(rotationsForAxis[axis])

  return (bend, bendHandle)

# def _nonlinearDeformer(geo, type, axis="", **options):
#   deformer, handle = pm.nonLinear(
#     geo,
#     type=type,
#     **options,
#   )
#   name = str(geo) + "_" + type + axis.upper()
#   pm.rename(bend, name)
#   pm.rename(bendHandle, name + "Handle")

def _matchTranslation(target, source):
  sourceAbsoluteTranslation = pm.xform(source, translation=True, query=True)
  pm.xform(target, translation=sourceAbsoluteTranslation)

def _lockAndHide(object, *attrNames):
  for attrName in attrNames:
    attr = object.attr(attrName)
    pm.setAttr(
      attr,
      keyable=False,
      channelBox=False,
      lock=True,
    )

def _hide(object, *attrNames):
  for attrName in attrNames:
    attr = object.attr(attrName)
    pm.setAttr(attr, channelBox=False, keyable=False)
