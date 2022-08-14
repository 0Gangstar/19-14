class Item:
    def __init__(self, name, size, description, image):
        self.name = name
        self.size = size
        self.description = description
        self.image = image

    def info(self):
        return "name: " + self.name + " size: " + str(self.size) + " with description: " + self.description


class UseableItem(Item):
    def __init__(self, name, size, description):
        super().__init__(name, size, description, None)

    def use(self):
        pass


apple = UseableItem('apple', 2, "Its classic red apple")
all_items = {apple.name: apple}
