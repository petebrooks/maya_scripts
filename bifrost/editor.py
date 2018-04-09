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

def _setCache(node, value):
  valueIntMappings = {
    "Re-compute": 0,
    "Read": 1,
    "Write": 2,
    "Read/Write": 3,
  }
  print "node %s" % node
  print "value %s" % value

def run():
  bifrostContainers = pm.ls("bifrostLiquidContainer*")

  windowKey = "bifrostEditor1"
  if pm.window(windowKey, exists=True):
    pm.deleteUI(windowKey, window=True)
  mainWindow = pm.window(windowKey, title="Bifrost Editor", rtf=True)

  with mainWindow:
    with pm.columnLayout():
      for bifrost in bifrostContainers:
        with pm.frameLayout(
          collapsable=True,
          label=bifrost,
          marginWidth=20,
          marginHeight=5,
        ):
          pm.checkBox(
            onCommand = pm.Callback(_enableBifrost, bifrost),
            offCommand = pm.Callback(_disableBifrost, bifrost),
            label = bifrost,
            value = bifrost.enable.get(),
          )
          for node in _toggleableBifrostNodes(bifrost):
            pm.checkBox(
              onCommand = pm.Callback(_enableBifrost, node),
              offCommand = pm.Callback(_disableBifrost, node),
              label = node,
              value = node.enable.get(),
            )
            if _isCacheableBifrostNode(node):
              with pm.columnLayout():
                pm.optionMenu(
                  label="Cache",
                  changeCommand=pm.CallbackWithArgs(_setCache, node),
                )
                pm.menuItem(label="Re-compute")
                pm.menuItem(label="Read")
                pm.menuItem(label="Write")
                pm.menuItem(label="Read/Write")

  mainWindow.show()

run()
