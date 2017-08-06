import pymel.core as pm
import sys 

def createAiUserDataAttr(name, value, type):
    attrName = name.getText()
    attrVal = value.getText()
    attrType = pm.optionMenu(type, query=True, value=True)
    
    sys.stdout.write("%s" % attrName)
    sys.stdout.write("%s" % attrVal)
    sys.stdout.write("%s" % attrType)
    
    for node in pm.ls(sl=True):
        shape = node.listRelatives(shapes=True)[0]
        attrFullName = "mtoa_constant_" + attrName
        if attrType == "Color":
            shape.addAttr(attrFullName, keyable=1, attributeType="double3")
            for channel in ["R", "G", "B"]:
                shape.addAttr(attrFullName + channel, parent=attrFullName, keyable=1, attributeType="double")
        shape.addAttr(attrFullName, keyable=1, dataType=attrType.lower())
        if attrVal:
            shape.attr(attrFullName).set(int(attrVal))
    
windowID = "aiAttrWin"
if pm.window(windowID, exists=True):
    pm.deleteUI(windowID)
    
window = pm.window(windowID, title="Add aiUserData Attribute")
pm.rowColumnLayout(numberOfColumns=2, columnWidth=(2, 300), columnSpacing=[(1, 10), (2, 10)], rowSpacing=(10, 10))

pm.text(label="*Attribute Name")
name = pm.textField()
pm.text(label="Attribute Value")
value = pm.textField()
pm.text(label="Attribute Type")
type = pm.optionMenu()
pm.menuItem(label = "Color")
pm.menuItem(label = "Float")
pm.menuItem(label = "Integer")
pm.menuItem(label = "Boolean")
pm.menuItem(label = "String")
pm.menuItem(label = "Enum")

pm.button(label="Cancel", command="pm.deleteUI('" + window + "', window=True)")
pm.button(label="Add aiUserData Attribute", command=pm.Callback(createAiUserDataAttr, name, value, type))
pm.showWindow(window)
