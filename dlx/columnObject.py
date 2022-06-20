from .dataObject import DataObject


class ColumnObject(DataObject):
    def __init__(self):
        super().__init__(None, -1)
        self.previousColumnObject = self
        self.nextColumnObject = self
        self.numberOfRows = 0

    def appendColumnHeader(self, columnObject):
        self.previousColumnObject.nextColumnObject = columnObject
        columnObject.nextColumnObject = self
        columnObject.previousColumnObject = self.previousColumnObject
        self.previousColumnObject = columnObject

    def unlinkColumnHeader(self,):
        self.nextColumnObject.previousColumnObject = self.previousColumnObject
        self.previousColumnObject.nextColumnObject = self.nextColumnObject

    def relinkColumnHeader(self,):
        self.nextColumnObject.previousColumnObject = self
        self.previousColumnObject.nextColumnObject = self

    def addDataObject(self, dataObject):
        self.appendToColumn(dataObject)
        self.numberOfRows += 1

    def unlinkDataObject(self, dataObject):
        dataObject.unlinkFromColumn()
        self.numberOfRows -= 1

    def relinkDataObject(self, dataObject):
        dataObject.relinkIntoColumn()
        self.numberOfRows += 1

    def loopNext(self, fn):
        next = self.nextColumnObject
        while next != self:
            fn(next)
            next = next.nextColumnObject
