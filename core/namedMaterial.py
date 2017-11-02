import pymel.core as pm
import re

def assign_named_material(mesh, shaderType="aiStandardSurface"):
  shader = find_or_create_named_material(mesh, shaderType="aiStandardSurface")
  pm.select(mesh)
  pm.hyperShade(assign=shader)

def find_or_create_named_material(mesh, shaderType="aiStandardSurface"):
  name = to_material_name(mesh)
  matching_materials = pm.ls(name)

  if len(matching_materials):
    return matching_materials[0]

  return pm.shadingNode(shaderType,
                        asShader=True,
                        name=name)

def to_material_name(mesh):
  base_name = mesh_basename(mesh)
  return base_name + "_Mat"

def mesh_basename(mesh):
  return re.match(r"(.+)_(?:Geo|(?:s_)?lo).*", str(mesh)).group(1)

# for mesh in pm.selected():
#   assign_named_material(mesh)
# assign_named_material(pm.selected()[0])
