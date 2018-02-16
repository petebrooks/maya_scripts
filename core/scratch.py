import re

def is_color_attr(attr):
  name = attr.outputs(plugs=True)[0].name()
  return re.match(r"\A.*\.color\Z", str(name))

material = pm.selected()[0]


for material in pm.selected():
  print "-----------"

  name = str(material) + "_Mat"
  ai_material = pm.shadingNode("aiStandardSurface", asShader=True, name=name)
  attrs = pm.listConnections(
    material,
    destination=False,
    source=True,
    plugs=True,
  )

  connected_color_attr = next((a for a in attrs if is_color_attr(a)), None)
  if connected_color_attr:
    file_node = connected_color_attr.node()
    pm.connectAttr(file_node.outColor, ai_material.baseColor, force=True)
  else:
    color = material.color.get()
    ai_material.baseColor.set(color)

  ai_material.base.set(1)
  pm.hyperShade(objects=material)
  pm.hyperShade(assign=ai_material)
