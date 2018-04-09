import pymel.core as pm
import maya.cmds as cmds
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
  menu = pm.optionMenu(
    label="Cache",
    changeCommand=pm.CallbackWithArgs(_setCacheState, bifrostNode),
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
    select=options.index(_getCacheState(bifrostNode)) + 1,
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

def _hasAttribute(node, attrName):
  return pm.attributeQuery(attrName, node=node, exists=True)

def _getCacheState(bifrostNode):
  intValueMappings = {
    0: "Re-compute",
    1: "Read",
    2: "Write",
    3: "Read/Write",
  }
  possibleCaches = [
    "liquidCache",
    "solidCache",
    "foamCache",
  ]
  for cache in possibleCaches:
    if _hasAttribute(bifrostNode, _enableCacheAttrName(cache)):
      if bifrostNode.attr(_enableCacheAttrName(cache)).get():
        cacheAttr = cache + "Control"
        return intValueMappings[bifrostNode.attr(cacheAttr).get()]
  return "Off"

def _upcaseFirst(s):
  if len(s) == 0:
    return s
  else:
    return s[0].upper() + s[1:]

def _enableCacheAttrName(cacheType):
  return "enable" + _upcaseFirst(cacheType)

def _setCacheState(bifrostNode, value):
  valueIntMappings = {
    "Re-compute": 0,
    "Read": 1,
    "Write": 2,
    "Read/Write": 3,
  }
  if value == "Off":
    bifrostNode.enableLiquidCache.set(False)
  else:
    bifrostNode.enableLiquidCache.set(True)
    bifrostNode.liquidCacheControl.set(valueIntMappings[value])

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
