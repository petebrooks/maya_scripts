import pymel.core as pm
import maya.cmds as cmds

def create(name="camera1", lockAttrs=True):
  cameraName = pm.mel.camera(
    name=name,
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
  camera.setLockTransform(True) # Equivalent to MEL `camera -e -lockTransform 1 camera1Shape1`

  if lockAttrs:
    _lockAndHide(cameraGroup, "translate", "rotate", "scale", "offset", "twist")
    _lockAndHide(camera, "translate")
    _lockAndHide(transformGroup, "rotate")
    _lockAndHide(aim, "rotate")
    _lockAndHide(up, "rotate")

  result = {
    "camera": camera,
    "transform": transformGroup,
    "aim": aim,
    "up": up,
  }
  return result

def createFromView():
  cameraResult = create()
  cameraView = cmds.cameraView(camera=_currentCameraName())

  _matchTransform(cameraResult["transform"], _currentCameraName())
  return cameraResult

def _matchTransform(target, source):
  print _toTransform(target)
  print _toTransform(source)
  pm.matchTransform(_toTransform(target), _toTransform(source))

def _toTransform(object):
  if object.nodeType() == "transform":
    return object
  return pm.listRelatives(object, type="transform", parent=True)[0]

def _currentCameraName():
  panel = pm.getPanel(withFocus=True)
  return pm.windows.modelPanel(panel, query=True, camera=True)

def _lockAndHide(object, *attr_names):
  for attr_name in attr_names:
    attr = object.attr(attr_name)
    attr.lock()
    attr.setKeyable(False)
    attr.showInChannelBox(False)

# def _createDOFRig():
  # distanceDimension -sp 19.219313 0 58.041905 -ep 0.464048 0 -4.813578 ;
  # parent new locators and distance to camera grp
  # parent constrain locator1 to camera
  # parentConstraint -weight 1;
  # connectAttr -f distanceDimensionShape1.distance cameraShape1.aiFocusDistance;
  # setAttr "cameraShape1.aiEnableDOF" 1;
  # _lockAndHide(locator1, "translate", "rotate")
  # _lockAndHide(locator2, "rotate")
