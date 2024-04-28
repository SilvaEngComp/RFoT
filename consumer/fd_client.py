class FdClient:
    def __init__(self, name, fdModel):
        self._name = name
        self._fdModel = fdModel
    def getName(self):
        return self._name
    def getFdModel(self):
        return self._fdModel