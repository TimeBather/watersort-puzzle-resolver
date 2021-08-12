import hashlib
from Container import Container


class Util:
    def __init__(self):
        pass

    @staticmethod
    def printContainers(containers):
        for i in range(len(containers)):
            print(str(i) + "| " + str(containers[i]))

    @staticmethod
    def takeSnapshot(containers):
        snapshot = []
        for i in range(len(containers)):
            snapshot.append(containers[i].takeSnapshot())
        return snapshot

    @staticmethod
    def loadSnapshot(snapshot):
        containers = []
        for i in range(len(snapshot)):
            container = Container([])
            container.loadSnapshot(snapshot[i])
            containers.append(container)
        return containers

    @staticmethod
    def takeSnapshotFingerprint(containers):
        return hashlib.md5(str(Util.takeSnapshot(containers))).hexdigest()

    @staticmethod
    def vectorFullArrange(endpoint):
        arranges = []

        for i in range(len(endpoint)):
            for j in range(len(endpoint)):
                if i == j:
                    continue
                arranges.append({"from": endpoint[i], "to": endpoint[j]})
        return arranges

    @staticmethod
    def getVectorScore(vector):
        return vector['score']
