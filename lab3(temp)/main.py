from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty, \
    BooleanProperty, NumericProperty
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.clock import Clock


class ListItem(GridLayout):
    index = 0
    selected = BooleanProperty(False)
    listGrid = ObjectProperty(None)
    def __init__(self, listGrid, **kwargs):
        super().__init__(**kwargs)
        self.listGrid = listGrid

    def toggle(self):
        self.selected = not self.selected

    def on_touch_down(self, touch):
        if (self.listGrid.collapsed):
            return
        if self.collide_point(*touch.pos):
            if (self.listGrid.selected_index == -1):
                self.listGrid.selected_index = self.index
                self.toggle()
            elif (self.index != self.listGrid.selected_index):
                self.listGrid.deselect()
                self.listGrid.selected_index = self.index
                self.toggle()
            elif (self.index == self.listGrid.selected_index):
                self.listGrid.selected_index = -1
                self.toggle()

class ListGrid(GridLayout):
    selected_index = -1
    collapsed = False

    def __init__(self, items, **kwargs):
        super().__init__(**kwargs)
        for i, row in enumerate(items):
            listItem = ListItem(self)
            listItem.index = i
            for item in row:
                listItem.add_widget(Label(text=item))
            self.add_widget(listItem)

    def setCollapse(self, collapse):
        self.collapsed = collapse
        if (collapse):
            self.height = 0
            self.opacity = 0
        if (not collapse):
            self.height = self.minimum_height
            self.opacity = 1

    def reverseIndex(self, index):
        return len(self.children) - index - 1

    def deselect(self):
        self.children[self.reverseIndex(self.selected_index)].selected = False

    def insertItem(self, item):
        selected_index = self.reverseIndex(0)
        if (self.selected_index != -1):
            selected_index = self.selected_index
        listItem = ListItem(self)
        for element in item:
            listItem.add_widget(Label(text=element))
        self.add_widget(listItem, self.reverseIndex(selected_index))
        self.updateIndices()

    def deleteItem(self):
        if (len(self.children) == 0):
            return
        selected_index = self.reverseIndex(0)
        if (self.selected_index != -1):
            selected_index = self.selected_index
        self.remove_widget(self.children[self.reverseIndex(selected_index)])
        self.updateIndices()
        self.selected_index = -1

    def getItem(self):
        if (len(self.children) == 0):
            return
        selected_index = self.reverseIndex(0)
        if (self.selected_index != -1):
            selected_index = self.selected_index
        item = []
        listItem = self.children[self.reverseIndex(selected_index)]
        for element in reversed(listItem.children):
            item.append(element.text)
        return item

    def setItem(self, item):
        if (len(self.children) == 0):
            return
        selected_index = self.reverseIndex(0)
        if (self.selected_index != -1):
            selected_index = self.selected_index
        listItem = self.children[self.reverseIndex(selected_index)]
        listItem.children[2].text = item[0]
        listItem.children[1].text = item[1]
        listItem.children[0].text = item[2]

    def moveItem(self, direction):
        if (self.selected_index == -1):
                return
        if (direction == -1 and self.selected_index == 0):
                return
        if (direction == 1 and self.selected_index == len(self.children) - 1):
                return
            
        selected_index = self.selected_index

        currentListItem = self.children[self.reverseIndex(selected_index)]
        upListItem = self.children[self.reverseIndex(selected_index + direction)]

        currentListItemIndex = self.children[self.reverseIndex(selected_index)].index
        upListItemIndex = self.children[self.reverseIndex(selected_index + direction)].index

        self.children[self.reverseIndex(selected_index)] = upListItem
        self.children[self.reverseIndex(selected_index + direction)] = currentListItem

        self.children[self.reverseIndex(selected_index)].index = currentListItemIndex
        self.children[self.reverseIndex(selected_index + direction)].index = upListItemIndex

        self.selected_index = selected_index + direction

    def updateIndices(self):
        for i, listItem in enumerate(self.children):
            listItem.index = self.reverseIndex(i)


class WrapperItem(GridLayout):
    index = 0
    selected = BooleanProperty(False)
    wrapper = ObjectProperty(None)

    def __init__(self, wrapper, **kwargs):
        super().__init__(**kwargs)
        self.wrapper = wrapper

    def deselect(self):
        self.selected = False
        self.wrapper.setCollapse(self.index, not self.selected)

    def toggle(self):
        self.selected = not self.selected
        self.wrapper.setCollapse(self.index, not self.selected)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if (self.wrapper.selected_index == -1):
                self.wrapper.selected_index = self.index
                self.toggle()
            elif (self.index != self.wrapper.selected_index):
                self.wrapper.deselect()
                self.wrapper.selected_index = self.index
                self.toggle()
            elif (self.index == self.wrapper.selected_index):
                self.wrapper.selected_index = -1
                self.toggle()

class Wrapper(GridLayout):
    selected_index = -1

    def reverseIndex(self, index):
        return len(self.children) - index - 1

    def setCollapse(self, index, collapse):
        self.children[self.reverseIndex(index+1)].setCollapse(collapse)
    
    def deselect(self):
        self.children[self.reverseIndex(self.selected_index)].deselect()

    def insertItem(self, item):
        if (self.selected_index == -1):
            return
        self.children[self.reverseIndex(self.selected_index + 1)].insertItem(item)

    def deleteItem(self):
        if (self.selected_index == -1):
            return
        self.children[self.reverseIndex(self.selected_index + 1)].deleteItem()

    def getItem(self):
        if (self.selected_index == -1):
            return
        return self.children[self.reverseIndex(self.selected_index + 1)].getItem()

    def setItem(self, item):
        if (self.selected_index == -1):
            return
        self.children[self.reverseIndex(self.selected_index + 1)].setItem(item)

    def moveItem(self, direction):
        if (self.selected_index == -1):
            return
        self.children[self.reverseIndex(self.selected_index + 1)].moveItem(direction)

class Catalog(RelativeLayout):
    scrollView = ObjectProperty(None)
    scrollBar = ObjectProperty(None)
    newItemInput = ObjectProperty(None)
    newItemSlider = ObjectProperty(None)
    newItemSpinner = ObjectProperty(None)
    wrapper = ObjectProperty(None)
    listGrids = []

    itemsExtended = [
        ['Samsung', 'Odyssey G5', '3999', 'True'],
        ['LG', 'UltraGear 27GN750', '4500', 'True'],
        ['ASUS', 'TUF VG259QM', '3299', 'False'],
        ['Acer', 'Predator XB271HU', '4999', 'True'],
        ['Dell', 'S2721DGF', '4200', 'True'],
        ['BenQ', 'EX2780Q', '3500', 'False'],
        ['MSI', 'Optix MAG272C', '2899', 'True'],
        ['Philips', '278E1A', '2999', 'False'],
        ['Gigabyte', 'G32QC', '4500', 'True'],
        ['ViewSonic', 'VX2758-2KP-MHD', '2800', 'True'],
        ['Samsung', 'Odyssey G7', '4999', 'True'],
        ['LG', 'UltraWide 34WN80C', '4000', 'True'],
        ['ASUS', 'ProArt PA278QV', '3500', 'True'],
        ['Acer', 'Nitro XV272U', '4300', 'False'],
        ['Dell', 'U2720Q', '4800', 'True'],
        ['BenQ', 'Zowie XL2411P', '2800', 'True'],
        ['MSI', 'MAG271C', '3300', 'False'],
        ['Philips', 'Brilliance 276E8VJSB', '2900', 'True'],
        ['Gigabyte', 'M32Q', '3700', 'False'],
        ['ViewSonic', 'XG2405', '2600', 'True']
    ]

    def getNewItem(self):
        name = self.newItemInput.text
        price = str(int(self.newItemSlider.value))
        status = self.newItemSpinner.text
        return [name, price, status]
        
    def insertItem(self):
        item = self.getNewItem()
        self.wrapper.insertItem(item)

    def deleteItem(self):
        self.wrapper.deleteItem()

    def getItem(self):
        item = self.wrapper.getItem()
        if (item == None):
            return
        self.newItemInput.text = item[0]
        self.newItemSlider.value = int(item[1])
        self.newItemSpinner.text = item[2]

    def setItem(self):
        item = self.getNewItem()
        self.wrapper.setItem(item)

    def moveItem(self, direction):
        self.wrapper.moveItem(direction)

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        self.scrollView.bind(scroll_y=self.updateSlider)
        
        itemsDict = {}

        for row in self.itemsExtended:
            if row[0] in itemsDict:
                itemsDict[row[0]].append(row[1:])
            else:
                itemsDict[row[0]] = [row[1:]]

        for i, category in enumerate(itemsDict):
            wrapperItem = WrapperItem(self.wrapper)
            wrapperItem.index = i * 2
            wrapperItem.add_widget(Label(text=category))
            self.wrapper.add_widget(wrapperItem)
            listGrid = ListGrid(itemsDict[category])
            self.listGrids.append(listGrid)
            self.wrapper.add_widget(listGrid)

        Clock.schedule_once(self.collapseAllLists, 0)

    def collapseAllLists(self, dt):
        for listGrid in self.listGrids:
            listGrid.setCollapse(True)

    def updateSlider(self, instance, value):
        self.scrollBar.value = max(0, min(1, value))
 

class CatalogApp(App):

    listItemHeight = NumericProperty(30)
    colors = {
        'gray': [0.5, 0.5, 0.5, 1],
        'lightGray': [0.6, 0.6, 0.6, 1],
        'graySelected': [0.7, 0.7, 0.7, 1],
        'darkBlue': [0.2471, 0.3137, 0.4235, 1],
        'blueSelected': [0.4275, 0.5412, 0.7294, 1]
    }

    def build(self):
        return Catalog()

CatalogApp().run()
