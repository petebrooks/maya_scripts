import pymel.core as pm
import re

def assign(meshes=None, shaderType="aiStandardSurface"):
  meshes = meshes or pm.selected()
  for mesh in meshes:
    print mesh
    shader = _findOrCreate(mesh, shaderType=shaderType)
    print shader
    pm.select(mesh)
    pm.hyperShade(assign=shader)

def _findOrCreate(mesh, shaderType="aiStandardSurface"):
  name = _toMaterialName(mesh)
  matching_materials = pm.ls(name)

  if len(matching_materials):
    return matching_materials[0]

  return pm.shadingNode(shaderType,
                        asShader=True,
                        name=name)

def _toMaterialName(mesh):
  base_name = _meshBasename(mesh)
  return base_name + "_Mat"

def _meshBasename(node):
  matches = re.match(r"(.+?)_(?:hi|lo|mesh)", str(node))
  if matches:
    return matches.group(1)
  return str(node)
