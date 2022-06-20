class DataObject:
    def __init__(self, listHeader, rowIndex):
        self.listHeader = listHeader
        self.rowIndex = rowIndex
        self.up = self
        self.down = self
        self.left = self
        self.right = self
        if listHeader is not None:
            listHeader.addDataObject(self)

    def appendToRow(self, dataObject):
        self.left.right = dataObject
        dataObject.right = self
        dataObject.left = self.left
        self.left = dataObject

    def appendToColumn(self, dataObject):
        self.up.down = dataObject
        dataObject.down = self
        dataObject.up = self.up
        self.up = dataObject

    def unlinkFromColumn(self):
        self.down.up = self.up
        self.up.down = self.down

    def relinkIntoColumn(self):
        self.down.up = self
        self.up.down = self

    def loopUp(self, fn):
        self.loop(fn, 'up')

    def loopDown(self, fn):
        self.loop(fn, 'down')

    def loopLeft(self, fn):
        self.loop(fn, 'left')

    def loopRight(self, fn):
        self.loop(fn, 'right')

    def loop(self, fn, propName):
        next = self.__dict__[propName]
        while next != self:
            fn(next)
            next = next.__dict__[propName]
