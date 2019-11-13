import pymel.core as pm
import os
import prompt

def export(nodes, path):
  pm.select(nodes)
  return pm.exportSelected(
    path,
    force=True,
    typ="FBX export",
    options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"
  )

def exportEach(nodes = None, directory = None):
  nodes = nodes or pm.selected()
  directory = directory or prompt.directory()
  for node in nodes:
    export(node, os.path.join(directory, str(node)))