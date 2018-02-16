import os
import re
import mtoa

def eunuch():
  pass

def skydome():
  light, _ = mtoa.utils.createLocator("aiSkyDomeLight", asLight=True)
  file_path = "/Volumes/Pegasus/maya/shared/hdr_spheres/cirrus_skydome.hdr"
  connect_texture(light.color, file_path)
  light.camera.set(0) # Disable camera visibility
  light.skyRadius.set(0) # Hide in viewport

# #Apply transforms to the light
# cmds.xform( myLight[1], r=1, ro=rotation, t=translation, s=(30,30,30))
def connect_texture(attr, file):
  file_node = pm.shadingNode(
                "file",
                name=os.path.basename(file),
                asTexture=True,
                isColorManaged=True,
              )
  file_node.fileTextureName.set(file)
  pm.connectAttr(file_node.outColor, attr, force=True)
