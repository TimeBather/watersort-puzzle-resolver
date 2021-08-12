# coding=utf-8
# 倒水排序小游戏求解算法 WaterSortPuzzleResolver
# Powered by MuChen<2387911242@qq.com>
from Container import Container
from Resolver import Resolver
from Utils import Util
import sys
sys.setrecursionlimit(100000)
# colorMap = ['灰', '红', '粉', '橙', '黄', '翠', '草', '绿', '靛', '蓝', '紫']
containerTable = [
    Container([1, 2, 3, 3]),
    Container([3,3,2,1]),
    Container([2,2,1,1]),
    Container([])
]
print(Util.printContainers(containerTable))
resolver = Resolver(containerTable)
print(resolver.resolve())
steps = []
_currentNode = resolver.currentNode
while _currentNode.parent != None:
    steps.append(_currentNode.selfOperation)
    _currentNode = _currentNode.parent
steps.reverse()
for i in steps:
    print(str(i.fromContainerId) + '--->' + str(i.targetContainerId))
Util.printContainers(
    Util.loadSnapshot(resolver.currentNode.snapshot)
)
