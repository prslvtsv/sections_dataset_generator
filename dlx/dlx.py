import sys
from .dataObject import DataObject
from .columnObject import ColumnObject

defaultOptions = {
    "numSolutions": sys.maxsize,
    "numPrimaryColumns": sys.maxsize
}


def solve(matrix, options={}):
    return Dlx().solve(matrix, options)


def solutionGenerator(matrix, options={}):
    yield from Dlx().solutionGenerator(matrix, options)


class Dlx:
    def solve(self, matrix, options={}):
        actualOptions = {**defaultOptions, **options}
        if isinstance(actualOptions["numSolutions"], int) is False:
            raise Exception('options["numSolutions"] must be an integer')

        if actualOptions["numSolutions"] < 0:
            raise Exception(
                'options["numSolutions"] can\'t be negative ')
        generator = self.solutionGenerator(matrix, actualOptions)
        numSolutions = actualOptions["numSolutions"]
        solutions = []
        index = 0
        while index < numSolutions:
            try:
                iteratorResult = next(generator)
                solutions.append(iteratorResult)
                index += 1
            except StopIteration:
                break
        return solutions

    def solutionGenerator(self, matrix, options):
        actualOptions = {**defaultOptions, **options}
        if not isinstance(actualOptions["numSolutions"], int):
            raise Exception('options["numSolutions"] must be an integer')

        if actualOptions["numSolutions"] < 0:
            raise Exception(
                'options["numSolutions"] can\'t be negative ')
        root = buildInternalStructure(
            matrix, actualOptions["numPrimaryColumns"])
        searchState = SearchState(self, root)
        yield from search(searchState)


def buildInternalStructure(matrix, numPrimaryColumns=None):
    if numPrimaryColumns is None:
        numPrimaryColumns = len(matrix[0]) if matrix[0] else 0

    root = ColumnObject()
    colIndexToListHeader = {}

    for rowIndex, row in enumerate(matrix):
        firstDataObjectInThisRow = None
        for colIndex, col in enumerate(row):
            if rowIndex == 0:
                listHeader = ColumnObject()
                if colIndex < numPrimaryColumns:
                    root.appendColumnHeader(listHeader)
                colIndexToListHeader[colIndex] = listHeader
            if col:
                listHeader = colIndexToListHeader[colIndex]
                dataObject = DataObject(listHeader, rowIndex)
                if firstDataObjectInThisRow is None:
                    firstDataObjectInThisRow = dataObject
                else:
                    firstDataObjectInThisRow.appendToRow(dataObject)

    return root


def search(searchState):
    searchState.searchStep()

    if searchState.isEmpty():
        if len(searchState.currentSolution):
            searchState.solutionFound()
            yield searchState.currentSolution[:]
        return

    c = chooseColumnWithFewestRows(searchState)
    coverColumn(c)
    r = c.down
    while r != c:
        searchState.pushRowIndex(r.rowIndex)
        r.loopRight(lambda j: coverColumn(j.listHeader))
        yield from search(searchState)
        r.loopLeft(lambda j: uncoverColumn(j.listHeader))
        searchState.popRowIndex()
        r = r.down
    uncoverColumn(c)


def chooseColumnWithFewestRows(searchState):
    chosenColumn = None

    def cb(column):
        nonlocal chosenColumn
        if chosenColumn is None or column.numberOfRows < chosenColumn.numberOfRows:
            chosenColumn = column

    searchState.root.loopNext(cb)
    return chosenColumn


def coverColumn(c):
    c.unlinkColumnHeader()
    c.loopDown(lambda i: i.loopRight(
        lambda j: j.listHeader.unlinkDataObject(j)))


def uncoverColumn(c):
    c.loopUp(lambda i: i.loopLeft(lambda j: j.listHeader.relinkDataObject(j)))
    c.relinkColumnHeader()


class SearchState:

    def __init__(self, dlx, root):
        self.dlx = dlx
        self.root = root
        self.currentSolution = []
        self.stepIndex = 0
        self.solutionIndex = 0

    def isEmpty(self):
        return self.root.nextColumnObject == self.root

    def pushRowIndex(self, rowIndex):
        self.currentSolution.append(rowIndex)

    def popRowIndex(self):
        self.currentSolution.pop()

    def searchStep(self):
        if len(self.currentSolution):
            e = {
                "partialSolution": self.currentSolution[:],
                "stepIndex": self.stepIndex
            }
            self.stepIndex += 1
            # self.dlx.emit('step', e)

    def solutionFound(self):
        e = {
            "solution": self.currentSolution[:],
            "solutionIndex": self.solutionIndex
        }
        self.solutionIndex += 1
        # self.dlx.emit('solution', e)
