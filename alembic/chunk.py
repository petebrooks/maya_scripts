import pymel.core as pm
from .. import util

# Used when imported chunked Alembic caches.
# Reads start/end frames and keys visibility appropriately.

def keyVisibility(transforms=None):
  if transforms:
    transforms = util.wrapList(transforms)
  else:
    transforms = pm.selected()

  for transform in transforms:
    _keyVisibility(transform)

def _keyVisibility(transform):
  alembicNode = pm.listConnections(transform.getShape(), type='AlembicNode')[0]

  startFrame = alembicNode.startFrame.get()
  endFrame = alembicNode.endFrame.get()

  pm.setKeyframe(transform, attribute='visibility', t=1, v=0)
  pm.setKeyframe(transform, attribute='visibility', t=startFrame, v=1)
  pm.setKeyframe(transform, attribute='visibility', t=endFrame + 1, v=0)
