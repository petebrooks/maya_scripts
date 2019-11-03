import pymel.core as pm

def swap_positions(obj_1, obj_2):
  x_1 = obj_1.translateX.get()
  y_1 = obj_1.translateY.get()
  z_1 = obj_1.translateZ.get()

  x_2 = obj_2.translateX.get()
  y_2 = obj_2.translateY.get()
  z_2 = obj_2.translateZ.get()

  obj_1.translateX.set(x_2)
  obj_1.translateY.set(y_2)
  obj_1.translateZ.set(z_2)

  obj_2.translateX.set(x_1)
  obj_2.translateY.set(y_1)
  obj_2.translateZ.set(z_1)

def sink_pivot():
  for obj in pm.selected():
    bbox = pm.exactWorldBoundingBox(obj)
    bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
    pm.xform(obj, piv=bottom, ws=True)
