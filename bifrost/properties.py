import pymel.core as pm

class Cache():
  """Handles interactions with Bifrost cache properties"""

  INDICES_TO_MODES = {
    0: "Re-compute",
    1: "Read",
    2: "Write",
    3: "Read/Write",
  }

  MODES_TO_INDICES = {
    "Re-compute": 0,
    "Read": 1,
    "Write": 2,
    "Read/Write": 3,
  }

  CACHE_TYPE_SUFFIX = "Cache"

  def __init__(self, cacheType, bifrostContainer):
    self.cacheType = cacheType
    self.bifrostContainer = bifrostContainer

  def enable(self):
    self._enableAttr.set(True)

  def disable(self):
    self._enableAttr.set(False)

  @property
  def enabled(self):
    return self._enableAttr.get()

  @property
  def disabled(self):
    return not self._enableAttr.get()

  @property
  def mode(self):
    return self.INDICES_TO_MODES[self._controlAttr.get()]

  def setMode(self, mode):
    if mode == "Off":
      return self.disable()
    elif isinstance(mode, int):
      index = mode
    else:
      index = self.MODES_TO_INDICES[mode]
    print "Setting %s to %s" % (self._controlAttr, index)
    self.enable()
    self._controlAttr.set(index)

  @property
  def _controlAttr(self):
    return self.bifrostContainer.attr(self._controlAttrName)

  @property
  def _controlAttrName(self):
    return self.cacheType.lower() + self.CACHE_TYPE_SUFFIX + "Control"

  @property
  def _enableAttr(self):
    return self.bifrostContainer.attr(self._enableAttrName)

  @property
  def _enableAttrName(self):
    return "enable" + self.cacheType[0].upper() + self.cacheType[1:] + self.CACHE_TYPE_SUFFIX

class InitialStateCache(Cache):
  """Handles interactions with Bifrost initial state cache properties"""

  CACHE_TYPE_SUFFIX = "InitialState"

  def __init__(self, cacheType, bifrostContainer):
    Cache.__init__(self, cacheType, bifrostContainer)

  @property
  def mode(self):
    return None

  def setMode(self, mode):
    pass

  def _controlAttr(self):
    return None

class Properties():
  """Wraps a bifrostFoamPropertiesContainer or bifrostLiquidPropertiesContainer"""
  def __init__(self, node):
    self.node = node
    self._caches = []

  @property
  def caches(self):
    return self._caches or self.rebuildCaches()

  def rebuildCaches(self):
    self._caches = []
    attrs = pm.listAttr(self.node)
    if "enableFoamCache" in attrs:
      self._caches.append(Cache("foam", self.node))
    # if "enableFoamInitialState" in attrs:
      # self._caches.append(InitialStateCache("foam", self.node))
    if "enableSolidCache" in attrs:
      self._caches.append(Cache("solid", self.node))
    if "enableLiquidCache" in attrs:
      self._caches.append(Cache("liquid", self.node))
    if "enableLiquidMeshCache" in attrs:
      self._caches.append(Cache("liquidMesh", self.node))
    # if "enableLiquidInitialState" in attrs:
      # self._caches.append(InitialStateCache("liquid", self.node))
    return self._caches
