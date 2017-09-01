import sys
import os
import maya.standalone

local_paths =  [
  # os.getcwd(),
  "/usr/local/lib/python2.7/site-packages"
]

for path in local_paths:
    print path
    if path not in sys.path:
        sys.path.append(path)

import pytest

try:
    maya.standalone.initialize(name="python")
except:
    pass

if __name__ == "__main__":
    pytest.main()
