import pymel.core as pm
from mine import curve

def create(geo, color="yellow"):
  bendDeformerX, bendDeformerXTransform = pm.nonLinear(
    geo,
    type="bend",
    lowBound=0,
    name=str(geo) + "_bendX"
  )
  geoAbsoluteTranslation = pm.xform(geo, translation=True, query=True)
  pm.xform(bendDeformerXTransform, translation=geoAbsoluteTranslation)
  bendDeformerXTransform.rotateY.set(0)

  bendDeformerZ, bendDeformerZTransform = pm.nonLinear(
    geo,
    type="bend",
    lowBound=0,
    name=str(geo) + "_bendZ"
  )
  geoAbsoluteTranslation = pm.xform(geo, translation=True, query=True)
  pm.xform(bendDeformerZTransform, translation=geoAbsoluteTranslation)
  bendDeformerZTransform.rotateY.set(-90)

  controlCurve = curve.pointy.create(relativeToObj=geo, color=color)
  pm.transformLimits(controlCurve, etx=(True, True), etz=(True, True), tx=(-10, 10), tz=(-10, 10))

  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=10, value=45)
  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=-10, value=-45)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=10, value=45)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=-10, value=-45)

  pm.select(controlCurve)
