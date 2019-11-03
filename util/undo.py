import maya.cmds as cmds

class disableUndo:
  def __enter__(self):
    cmds.undoInfo(stateWithoutFlush=False)

  def __exit__(self, type, value, traceback):
    cmds.undoInfo(stateWithoutFlush=True)