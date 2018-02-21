import pymel.core as pm
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

def _toggle(bifrostObject, newState=None):
  container = _findRelativesByName(bifrostObject, "bifrostLiquidContainer")[0]
  liquidProps = _findConnectionsByName(container, "bifrostLiquidProperties")
  foamProps = _findConnectionsByName(container, "bifrostFoamProperties")
  emitterProps = _findConnectionsByName(container, "EmitterProps")

  if newState == None:
    newState = not container.enable.get()

  container.enable.set(newState)
  for obj in liquidProps:
    obj.enable.set(newState)
  for obj in foamProps:
    obj.enable.set(newState)
  for emitter in emitterProps:
    emitter.enable.set(newState)

  if newState == True:
    sys.stdout.write("Enabled %s" % bifrostObject)
  else:
    sys.stdout.write("Disabled %s" % bifrostObject)

def _findRelativesByName(source, name):
  return filter(lambda object: name in str(object), pm.listRelatives(source))

def _findConnectionsByName(source, name):
  return filter(lambda object: name in str(object), source.listConnections())
