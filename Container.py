# coding=utf-8
import time

from Operation import Operation

colorMap = ['灰', '红', '粉', '橙', '黄', '翠', '草', '绿', '靛', '蓝', '紫']


class Container:
    def __init__(self, data=None):
        if data is None:
            data = []
        self.containerMap = data

    containerMap = []
    capacity = 4

    def isLegal(self):
        if len(self.containerMap) > self.capacity:
            return False
        return True

    def getStackTopItemVolume(self):
        d = 0
        for i in range(len(self.containerMap) - 1, -1, -1):
            if self.containerMap[i] != self.containerMap[len(self.containerMap) - 1]:
                return d
            d = d + 1
        return len(self.containerMap)

    def canPourTo(self, target):
        if len(self.containerMap) == 0:
            return -1
        if len(target.containerMap) != 0 and target.containerMap[len(target.containerMap) - 1] != self.containerMap[len(self.containerMap) - 1]:
            return -1
        if len(target.containerMap) >= 4:
            return -1
        if len(target.containerMap) + self.getStackTopItemVolume() > target.capacity:
            return 0
        return 1

    def pourTo(self, target):

        if self.canPourTo(target) < 0:
            return False
        pour_volume = min(self.getStackTopItemVolume(), target.capacity - len(target.containerMap))
        pour_color = self.containerMap[len(self.containerMap) - 1]
        for i in range(pour_volume):
            self.containerMap.pop()
        target.pourFrom(pour_color, pour_volume)
        return Operation(self, target, pour_volume)

    def pourFrom(self, color, volume):
        for i in range(volume):
            self.containerMap.append(color)

    def __str__(self):
        _str = ''
        for i in range(len(self.containerMap)):
            _str = _str + colorMap[self.containerMap[i]] + ' '
        return _str

    def takeSnapshot(self):
        serialized = ''
        for i in range(len(self.containerMap)):
            if serialized != '':
                serialized = serialized + ','
            serialized = serialized + str(self.containerMap[i])
        return serialized

    def loadSnapshot(self, containerMap):
        if len(containerMap) == 0:
            return
        data = containerMap.split(',')
        for i in range(len(data)):
            data[i] = int(data[i])
        self.containerMap = data
