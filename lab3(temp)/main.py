from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty, \
    BooleanProperty, NumericProperty

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

    def reverseIndex(self, index):
        return len(self.children) - index - 1

    def deselect(self):
        self.children[self.reverseIndex(self.selected_index)].selected = False

class Catalog(RelativeLayout):
    scrollView = ObjectProperty(None)
    scrollBar = ObjectProperty(None)
    listGrid = ObjectProperty(None)
    newItemInput = ObjectProperty(None)
    newItemSlider = ObjectProperty(None)
    newItemSpinner = ObjectProperty(None)

    items = [
        ['Odyssey G5', '3999', 'True'],
        ['UltraGear 27GN750', '4500', 'True'],
        ['TUF VG259QM', '3299', 'False'],
        ['Predator XB271HU', '4999', 'True'],
        ['S2721DGF', '4200', 'True'],
        ['EX2780Q', '3500', 'False'],
        ['Optix MAG272C', '2899', 'True'],
        ['278E1A', '2999', 'False'],
        ['G32QC', '4500', 'True'],
        ['VX2758-2KP-MHD', '2800', 'True'],
        ['Odyssey G7', '4999', 'True'],
        ['UltraWide 34WN80C', '4000', 'True'],
        ['ProArt PA278QV', '3500', 'True'],
        ['Nitro XV272U', '4300', 'False'],
        ['U2720Q', '4800', 'True'],
        ['Zowie XL2411P', '2800', 'True'],
        ['MAG271C', '3300', 'False'],
        ['Brilliance 276E8VJSB', '2900', 'True'],
        ['M32Q', '3700', 'False'],
        ['XG2405', '2600', 'True']
    ]

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
        selected_index = self.listGrid.reverseIndex(0)
        if (self.listGrid.selected_index != -1):
            selected_index = self.listGrid.selected_index
        self.items.insert(selected_index, item)
        listItem = ListItem(self.listGrid)
        for element in item:
            listItem.add_widget(Label(text=element))
        self.listGrid.add_widget(listItem, self.listGrid.reverseIndex(selected_index))
        for i, listItem in enumerate(self.listGrid.children):
            listItem.index = self.listGrid.reverseIndex(i)

    def deleteItem(self):
        selected_index = self.listGrid.reverseIndex(0)
        if (self.listGrid.selected_index != -1):
            selected_index = self.listGrid.selected_index
        

    def on_kv_post(self, base_widget):
        self.scrollView.bind(scroll_y=self.updateSlider)
        for i, row in enumerate(self.items):
            listItem = ListItem(self.listGrid)
            listItem.index = i
            for item in row:
                listItem.add_widget(Label(text=item))
            self.listGrid.add_widget(listItem)
            

    def updateSlider(self, instance, value):
        self.scrollBar.value = max(0, min(1, value))
    

    

class CatalogApp(App):

    listItemHeight = NumericProperty(30)
    colors = {
        'gray': [0.5, 0.5, 0.5, 1],
        'lightGray': [0.6, 0.6, 0.6, 1],
        'graySelected': [0.7, 0.7, 0.7, 1]
    }

    def build(self):
        return Catalog()

CatalogApp().run()
