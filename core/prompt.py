import pymel.core as pm

def directory(caption="Select a directory"):
  selection = pm.fileDialog2(
    okCaption="Select",
    fileMode=3, # Directory mode
    dialogStyle=2, # Maya-style dialog
    caption=caption,
  )
  return selection[0]