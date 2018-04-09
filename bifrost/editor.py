import pymel.core as pm
import maya.cmds as cmds
from mine.bifrost.properties import *
import sys

def _enableBifrost(bifrost):
  bifrost.enable.set(True)
  print "Enabled %s" % bifrost

def _disableBifrost(bifrost):
  bifrost.enable.set(False)
  print "Disabled %s" % bifrost

def _isToggleableBifrostNode(node):
  substrings = [
    "collider",
    "emitter",
    "LiquidProperties",
    "MotionField",
    "FoamProperties",
  ]
  return any(substring in str(node) for substring in substrings)

def _isCacheableBifrostNode(node):
  substrings = [
    "LiquidProperties",
    "FoamProperties",
  ]
  return any(substring in str(node) for substring in substrings)

def _toggleableBifrostNodes(bifrostContainer):
  possibleNodes = pm.listConnections(bifrostContainer, shapes=True)
  result = filter(_isToggleableBifrostNode, set(possibleNodes))
  return sorted(result)

def _cacheableBifrostNodes(bifrostContainer):
  possibleNodes = pm.listConnections(bifrostContainer, shapes=True)
  result = filter(_isCacheableBifrostNode, set(possibleNodes))
  return sorted(result)

def _checkBoxToggle(bifrostNode):
  pm.checkBox(
    onCommand = pm.Callback(_enableBifrost, bifrostNode),
    offCommand = pm.Callback(_disableBifrost, bifrostNode),
    label = bifrostNode,
    value = bifrostNode.enable.get(),
  )

def _cacheOptionMenu(bifrostNode):
  properties = Properties(bifrostNode)
  menu = pm.optionMenu(
    label="Cache",
    changeCommand=pm.CallbackWithArgs(_setCacheMode, properties),
  )
  options = [
    "Off",
    "Re-compute",
    "Read",
    "Write",
    "Read/Write",
  ]
  for option in options:
    pm.menuItem(label=option)
  pm.optionMenu(
    menu,
    edit=True,
    select=options.index(_getCacheMode(properties)) + 1,
  )

def _editorRow(bifrostNode):
  with pm.rowLayout(numberOfColumns=2):
    _checkBoxToggle(bifrostNode)
    if _isCacheableBifrostNode(bifrostNode):
      _cacheOptionMenu(bifrostNode)

def _editorFrame(bifrostContainer):
  with pm.frameLayout(
    collapsable=True,
    label=bifrostContainer,
    marginWidth=20,
    marginHeight=5,
  ):
    with pm.columnLayout():
      _editorRow(bifrostContainer)
      for node in _toggleableBifrostNodes(bifrostContainer):
        _editorRow(node)

def _getCacheMode(properties):
  if any(cache.enabled for cache in properties.caches):
    return properties.caches[0].mode
  else:
    return "Off"

def _setCacheMode(properties, mode):
  print properties.caches
  for cache in properties.caches:
    cache.setMode(mode)

def run():
  bifrostContainers = pm.ls("bifrostLiquidContainer*")

  windowKey = "bifrostEditor1"
  if pm.window(windowKey, exists=True):
    pm.deleteUI(windowKey, window=True)

  mainWindow = pm.window(
    windowKey,
    title="Bifrost Editor",
    rtf=True,
    backgroundColor=[.251, .229, .463],
  )

  with mainWindow:
    with pm.columnLayout():
      for bifrost in bifrostContainers:
        _editorFrame(bifrost)

  mainWindow.show()

run()
