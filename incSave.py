import pymel.core as pm
import os


def incSave(dirName="archive"):
    path = pm.sceneName()
    fileName = path.split("/")[-1].partition(".")[0]
    newFileName = fileName + "_0001" + ".ma"
    fileFolder = os.path.abspath(os.path.join(path, os.pardir))
    incSaveFolderPath = os.path.join(fileFolder, dirName)
    projectSaveFolder = os.path.join(incSaveFolderPath, fileName)
    incSaveFilePath = os.path.join(projectSaveFolder, newFileName)

    if os.path.exists(incSaveFilePath):
        savedFiles = sorted(os.listdir(projectSaveFolder))
        incFiles = []
        for ifl in savedFiles:
            if fileName in i:
                incFiles.append(i)
        lastFile = incFiles[len(incFiles) - 1]
        name = lastFile.partition(".")[0]
        newName = name[:-4] + (str(int(name[-4:]) + 1).zfill(4)) + ".ma"
        incSaveFilePath = os.path.join(projectSaveFolder, newName)
    else:
        os.makedirs(projectSaveFolder)

    pm.system.saveAs(incSaveFilePath)
    pm.system.saveAs(path)
