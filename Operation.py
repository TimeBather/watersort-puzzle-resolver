class Operation:
    def __init__(self, from_container, toContainer, volume):
        self.fromContainer = from_container
        self.targetContainer = toContainer
        self.volume = volume

    fromContainer = None
    targetContainer = None
    volume = None
    fromContainerId = None
    targetContainerId = None

    def __eq__(self, other):
        return self.volume == other.volume and self.fromContainer == other.fromContainer and self.fromContainer == other.fromContainer
