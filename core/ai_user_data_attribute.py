import pymel.core as pm
import sys

def createAiUserDataAttr(nameField, valueField, typeField):
    typeMappings = {
        "Float": "float",
        "Integer": "short",
        "Boolean": "bool",
        "String": "string",
    }

    attrName = nameField.getText()
    attrVal = valueField.getText()
    rawType = pm.optionMenu(typeField, query=True, value=True)

    for node in pm.ls(sl=True):
        shape = node.listRelatives(shapes=True)[0]
        attrFullName = "mtoa_constant_" + attrName

        if rawType == "Color":
            shape.addAttr(attrFullName, keyable=1, attributeType="double3")
            for channel in ["R", "G", "B"]:
                shape.addAttr(attrFullName + channel, parent=attrFullName, keyable=1, attributeType="double")
        else:
            attrType = typeMappings[rawType]
            shape.addAttr(attrFullName, keyable=1, attributeType=attrType)

        if attrVal:
            shape.attr(attrFullName).set(int(attrVal))

        sys.stdout.write("Added %s to %s\n" % (attrFullName, str(shape)))

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

pm.button(label="Cancel", command="pm.deleteUI('" + window + "', window=True)")
pm.button(label="Add aiUserData Attribute", command=pm.Callback(createAiUserDataAttr, name, value, type))
pm.showWindow(window)
