import pymel.core as pm

def create(lockAttrs=True):
  cameraName = pm.mel.camera(
    centerOfInterest=5,
    focalLength=35,
    lensSqueezeRatio=1,
    cameraScale=1,
    horizontalFilmAperture=1.41732,
    horizontalFilmOffset=0,
    verticalFilmAperture=0.94488,
    verticalFilmOffset=0,
    filmFit="Fill",
    overscan=1,
    motionBlur=0,
    shutterAngle=144,
    nearClipPlane=0.1,
    farClipPlane=10000,
    orthographic=0,
    orthographicWidth=30,
    panZoomEnabled=0,
    horizontalPan=0,
    verticalPan=0,
    zoom=1,
    displayResolution=1,
    displayGateMask=1,
  )[0]
  pm.mel.objectMoveCommand()
  pm.mel.cameraMakeNode(3, "")

  camera = pm.ls(cameraName)[0]
  cameraGroup = camera.getParent()
  children = cameraGroup.getChildren()

  aim = filter(lambda object: "_aim" in str(object), children)[0]
  up = filter(lambda object: "_up" in str(object), children)[0]

  transformGroupName = "%s_transform" % str(camera)
  transformGroup = pm.group(camera, up, name=transformGroupName)

  camera.displayGateMaskColor.set((0.0, 0.0, 0.0))
  camera.displayGateMaskOpacity.set(1)
  camera.filmFit.set(1)
  camera.overscan.set(1.05)

  if lockAttrs:
    _lockAndHide(cameraGroup, "translate", "rotate", "scale", "offset", "twist")
    _lockAndHide(camera, "translate")
    _lockAndHide(transformGroup, "rotate")
    _lockAndHide(aim, "rotate")
    _lockAndHide(up, "rotate")

def _lockAndHide(object, *attr_names):
  for attr_name in attr_names:
    attr = object.attr(attr_name)
    attr.lock()
    attr.setKeyable(False)
    attr.showInChannelBox(False)
