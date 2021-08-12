class OperationTree:
    snapshot = []
    operationPool = []
    parent = None
    selfOperation = None

    def __init__(self, snapshot):
        self.snapshot = snapshot
