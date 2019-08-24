import pymel.core as pm
import re

def assign(meshes=None, shaderType="aiStandardSurface", ignoreDigits=True):
  meshes = meshes or pm.selected()
  for mesh in meshes:
    materialName = _meshBasename(mesh, ignoreDigits) + "_Mat"
    print mesh
    shader = _findOrCreateMaterial(materialName, shaderType=shaderType)
    print shader
    pm.select(mesh)
    pm.hyperShade(assign=shader)

def _findOrCreateMaterial(materialName, shaderType="aiStandardSurface"):
  matching_materials = pm.ls(materialName)

  if len(matching_materials):
    return matching_materials[0]

  return pm.shadingNode(shaderType,
                        asShader=True,
                        name=materialName)

def _toMaterialName(mesh):
  base_name = _meshBasename(mesh)
  return base_name + "_Mat"

def _meshBasename(node, ignoreDigits=True):
  if ignoreDigits:
    matches = re.match(r"(.+?)_(?:hi|lo|mesh|\d+)", str(node))
  else:
    matches = re.match(r"(.+?)_(?:hi|lo|mesh)", str(node))

  if matches:
    return matches.group(1)
  return str(node)
