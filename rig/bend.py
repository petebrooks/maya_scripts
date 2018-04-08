import pymel.core as pm
from mine import curve

def create(geo, color="yellow", boundary=10):
  """Creates a rig that bends geo in X and Z directions"""

  bendDeformerX= _bendDeformer(geo, "x")
  bendDeformerZ= _bendDeformer(geo, "z")

  controlCurve = curve.pointy.create(
    relativeToObj=geo,
    color=color,
    limitX=(-boundary, boundary),
    limitZ=(-boundary, boundary),
    name=str(geo) + "_bendCtrl",
  )

  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=boundary, value=50)
  pm.setDrivenKeyframe(bendDeformerX.curvature, currentDriver=controlCurve.translateX, driverValue=-boundary, value=-50)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=boundary, value=50)
  pm.setDrivenKeyframe(bendDeformerZ.curvature, currentDriver=controlCurve.translateZ, driverValue=-boundary, value=-50)

  pm.select(controlCurve)

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

  geoAbsoluteTranslation = pm.xform(geo, translation=True, query=True)
  pm.xform(bendHandle, translation=geoAbsoluteTranslation)
  bendHandle.rotateY.set(rotationsForAxis[axis])

  return bend
