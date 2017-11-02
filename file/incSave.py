import pymel.core as pm
import os
import sys
import datetime
import shutil


def incSave(dirName="archive", description=False):
  scenePath = pm.sceneName()
  sceneName = _getBasename(scenePath)
  sceneDir = os.path.dirname(scenePath)
  archiveDir = os.path.join(sceneDir, dirName)
  nextVersion = 1

  if os.path.exists(archiveDir):
    lastVersion = _maxVersion(archiveDir, match=sceneName)
    nextVersion = lastVersion + 1
  else:
    os.makedirs(archiveDir)

  newName = _incSceneName(sceneName, nextVersion)
  archiveFilePath = os.path.join(archiveDir, newName)

  pm.system.saveAs(scenePath)
  sys.stdout.write("\nScene saved as %s" % scenePath)
  shutil.copy2(scenePath, archiveFilePath)
  sys.stdout.write("\nVersion saved as %s" % archiveFilePath)

  if description:
    descriptionFilePath = os.path.join(archiveDir, sceneName + "--list.txt")
    _writeUserDescription(descriptionFilePath, sceneName, nextVersion, archiveFilePath)

def _getBasename(path):
  base = os.path.splitext(path)[0]
  return os.path.basename(base)

def _maxVersion(path, match=""):
  nums = []
  for file in os.listdir(path):
    if match in file:
      parts = file.split(".")
      if len(parts) > 2:
        try:
          nums.append(int(parts[-2]))
        except ValueError:
          pass

  if len(nums) > 0:
    return max(nums)
  else:
    return 0

def _incSceneName(name, num):
  version = str(num).zfill(4)
  return ".".join([name, version, "ma"])

def _writeUserDescription(path, sceneName, version, scenePath):
  description = _getUserDescription()
  today = datetime.datetime.now()

  with open(path, "a") as descriptionFile:
    descriptionFile.write("---------------------\n")
    descriptionFile.write(sceneName + "\n")
    descriptionFile.write(today.strftime("%d-%b-%Y %I:%M:%S") + "\n")
    descriptionFile.write("Version %s\n" % version)
    descriptionFile.write(scenePath + "\n")
    descriptionFile.write(description + "\n")

def _getUserDescription():
  result = cmds.promptDialog(
    title="Commit Version",
    message="Enter description:",
    button=["OK", "Cancel"],
    defaultButton="OK",
    cancelButton="Cancel",
    dismissString="Cancel"
  )

  if result == "OK":
    return pm.promptDialog(query=True, text=True)
  else:
    return "No description"
