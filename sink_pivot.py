import pymel.core as pm

def sink_pivot():
  for obj in pm.ls(sl=True):
    bbox = pm.exactWorldBoundingBox(obj)
    bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
    pm.xform(obj, piv=bottom, ws=True)
