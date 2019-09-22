import pymel.core as pm
import maya.mel as mel
import sys

def toggle(bifrostObjects=None):
  if not bifrostObjects:
    bifrostObjects = pm.selected()
  for object in bifrostObjects:
    _toggle(object)

def disable(bifrostObjects=None):
  if not bifrostObjects:
    bifrostObjects = pm.selected()
  for object in bifrostObjects:
    _toggle(object, False)

def enable(bifrostObjects=None):
  if not bifrostObjects:
    bifrostObjects = pm.selected()
  for object in bifrostObjects:
    _toggle(object, True)

def hide(bifrostObjects=None):
  if not bifrostObjects:
    bifrostObjects = pm.selected()
  for object in bifrostObjects:
    _hide(object)

def _hide(bifrostObject):
  # TODO: How to track which was toggled on initially for reverting?
  for shape in _getBifrostShapes(bifrostObject):
    shape.particles.set(0)
    shape.voxels.set(0)

def show(bifrostObjects=None):
  if not bifrostObjects:
    bifrostObjects = pm.selected()
  for object in bifrostObjects:
    _show(object)

def _show(bifrostObject):
  # TODO: How to track which was toggled on initially for reverting?
  for shape in _getBifrostShapes(bifrostObject):
    shape.particles.set(1)
    shape.voxels.set(0)

def _getBifrostShapes(bifrostObject):
  transforms = filter(lambda object: not "Container" in str(object), pm.listRelatives(bifrostObject))
  return map(lambda object: object.getShape(), transforms)

def _toggle(bifrostObject, newState=None, toggleAll=False):
  if _isGroup(bifrostObject):
    bifrostObject = _findRelativesByName(bifrostObject, "bifrostLiquid")[0]

  container = _findRelativesByName(bifrostObject, "bifrostLiquidContainer")[0]

  if newState == None:
    newState = not container.enable.get()

  if newState == True:
    mel.eval("playButtonStart")

  container.enable.set(newState)

  if toggleAll:
    liquidProps = _findConnectionsByName(container, "bifrostLiquidProperties")
    foamProps = _findConnectionsByName(container, "bifrostFoamProperties")
    emitterProps = _findConnectionsByName(container, "EmitterProps")

    for obj in liquidProps:
      obj.enable.set(newState)
    for obj in foamProps:
      obj.enable.set(newState)
    for emitter in emitterProps:
      emitter.enable.set(newState)

  if newState == True:
    sys.stdout.write("Enabled %s\n" % bifrostObject)
  else:
    sys.stdout.write("Disabled %s\n" % bifrostObject)

def _findRelativesByName(source, name):
  return filter(lambda object: name in str(object), pm.listRelatives(source))

def _findConnectionsByName(source, name):
  return filter(lambda object: name in str(object), source.listConnections())

def _isGroup(node):
  return _isTransform(node) and not node.getShape()

def _isTransform(node):
  return node and node.nodeType() == "transform"
