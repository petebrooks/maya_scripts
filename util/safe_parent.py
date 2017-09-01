def safeParent(child, prent):
  if prent:
    pm.parent(child, prent)
  else:
    pm.parent(child, world=True)
