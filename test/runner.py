import sys
import os

user_python_path = "/usr/local/lib/python2.7/site-packages"
maya_python_path = "/Applications/Autodesk/maya2018/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages"

local_paths =  [
  # os.getcwd(),
  user_python_path,
  maya_python_path,
]

for path in local_paths:
    print path
    if path not in sys.path:
        sys.path.append(path)

import pytest

# try:
#     maya.standalone.initialize(name="python")
# except:
#     pass

if __name__ == "__main__":
    pytest.main()
