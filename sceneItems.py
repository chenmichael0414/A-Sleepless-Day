import item
from item import Item

currScene = "CHEM"
items = {
    "CHEM": [['block'],['block', 200, 200], ['arrow', 300, 100, True]]
}

def addSceneItems(scene, item):
    for i in items[scene]:
        if len(i) ==  1:
            item.addItem(i[0])
        else:
            item.addItem(i[0], x=i[1], y=i[2])
    currScene = scene

def itemRemove(loc):
    items[currScene].pop(loc)