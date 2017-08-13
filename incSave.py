import pymel.core as pm
import os


def incSave(dirName="archive"):
    scenePath = pm.sceneName()
    sceneName = os.path.basename(scenePath).partition(".")[0]
    sceneDir = os.path.dirname(scenePath)
    archiveDir = os.path.join(sceneDir, dirName)
    num = 1

    if os.path.exists(archiveDir):
        lastVersion = maxVersion(archiveDir, match=sceneName)
        num = lastVersion + 1
    else:
        os.makedirs(archiveDir)

    newName = incSceneName(sceneName, num)
    archiveFilePath = os.path.join(archiveDir, newName)

    pm.system.saveAs(archiveFilePath)
    pm.system.saveAs(path)

    print archiveFilePath

def maxVersion(path, match=""):
    nums = []
    for file in os.listdir(path):
        if match in file:
            parts = file.split(".")
            if len(parts) > 2:
                nums.append(int(parts[-2]))
    return max(nums)

def incSceneName(name, num):
    version = str(num).zfill(4)
    return ".".join([name, version, "ma"])

incSave()
