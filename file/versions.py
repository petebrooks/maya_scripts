import pymel.core as pm
import maya.cmds as cmds
import os
import sys
import datetime
import shutil

# TODO:
# - Store version info as JSON for easy parsing
# - Overwrite last version message on amend
# - Autofill last version message when prompting on amend

def incSave(dirName="archive", promptMessage=True, amend=False, dryRun=False):
  scenePath = pm.sceneName()
  sceneName = _getBasename(scenePath)
  archiveDir = os.path.join(
    os.path.dirname(scenePath),
    dirName,
  )

  lastVersion = _maxVersion(archiveDir, match=sceneName)

  if lastVersion == 0:
    if amend:
      sys.stdout.write("Nothing to amend.")
      return False

  if not os.path.exists(archiveDir):
    os.makedirs(archiveDir)

  if amend:
    currentVersion = lastVersion
  else:
    currentVersion = lastVersion + 1

  archiveFilePath = os.path.join(
    archiveDir,
    _versionName(sceneName, currentVersion),
  )

  if promptMessage:
    _writeUserMessage(
      archiveDir,
      sceneName,
      currentVersion,
      archiveFilePath,
    )

  _saveVersion(scenePath, archiveFilePath, dryRun=dryRun)

def _saveVersion(scenePath, archiveFilePath, dryRun=False):
  if dryRun:
    sys.stdout.write("\n[dry run] Scene saved as %s" % scenePath)
    sys.stdout.write("\n[dry run] Version saved as %s" % archiveFilePath)
  else:
    pm.system.saveAs(scenePath)
    sys.stdout.write("\nScene saved as %s" % scenePath)
    shutil.copy2(scenePath, archiveFilePath)
    sys.stdout.write("\nVersion saved as %s" % archiveFilePath)

def _indexFilePath(archiveDir, sceneName):
  return os.path.join(archiveDir, sceneName + "--list.txt")

def _getBasename(path):
  base = os.path.splitext(path)[0]
  return os.path.basename(base)

def _maxVersion(path, match=""):
  if not os.path.exists(path):
    return 0

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

def _versionName(name, num):
  version = str(num).zfill(4)
  return ".".join([name, version, "ma"])

def _writeUserMessage(archiveDir, sceneName, version, scenePath):
  path = _indexFilePath(archiveDir, sceneName)
  message = _getUserMessage()
  today = datetime.datetime.now()

  with open(path, "a") as indexFile:
    indexFile.write("---------------------\n")
    indexFile.write(sceneName + "\n")
    indexFile.write(today.strftime("%d-%b-%Y %I:%M:%S") + "\n")
    indexFile.write("Version %s\n" % version)
    indexFile.write(scenePath + "\n")
    indexFile.write(message + "\n")

def _getUserMessage(text=""):
  result = cmds.promptDialog(
    title="Commit Version",
    text=text,
    message="Enter message:",
    button=["OK", "Cancel"],
    defaultButton="OK",
    cancelButton="Cancel",
    dismissString="Cancel"
  )

  if result == "OK":
    return pm.promptDialog(query=True, text=True)
  else:
    return "No message"
