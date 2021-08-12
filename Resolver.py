# coding=utf-8
import time

from Utils import Util
from OperationTree import OperationTree
import hashlib


class Resolver:
    opTree = None  # 操作树
    containers = None  # 容器数组
    currentNode = None  # 当前操作节点，用于成功后追踪路径

    def __init__(self, containers):  # 初始化容器
        self.containers = containers  # 输入容器
        self.opTree = OperationTree(Util.takeSnapshot(self.containers))  # 创建操作树根节点

    def resolve(self, tree_node=None):  # 开始求解
        if tree_node is None:  # 如果当前节点未传入，则默认从根节点开始搜索解
            tree_node = self.opTree  # 将当前节点设置为根节点
        self.currentNode = tree_node  # 同步当前操作节点到树内
        if self.hasLoop(tree_node):  # 防止出现环(即类似A->B B->C C->A的操作)
            return False  # 出现环则回退到上一步骤
        now_containers = Util.loadSnapshot(tree_node.snapshot)  # 从树中加载快照
        # Util.printContainers(now_containers)
        if Resolver.isWin(now_containers):  # 判断是否已经赢了
            return True  # 返回True,直接回到主程序
        vectors = self.findMovableContainers(now_containers)  # 寻找可用的移动
        vectors['normal'].sort(key=Util.getVectorScore, reverse=True)  # 根据评分，优先使能够合并的合并
        vectors['lowPriority'].sort(key=Util.getVectorScore, reverse=True)  # 这里设置LowPriority的原因是，如果发生需要
        # A->B A->C 来解锁其下面的溶液的解法，则必须考虑，但由于这种情况较少见，故降低优先级考虑
        final_vector = []  # 最终的向量列表
        final_vector.extend(vectors['normal'])  # 先加正常的
        final_vector.extend(vectors['lowPriority'])  # 再是低优先级
        for i in range(len(final_vector)):  # 根据顺序进行尝试
            _snapshot = Util.loadSnapshot(tree_node.snapshot)  # 加载一个新的快照，这里其实我看到其他的Coder用了deepCopy方法
            # (主要是写这个程序之前没有学到有DeepCopy的方法，所以需要反复复制）
            operation = _snapshot[final_vector[i]['from']].pourTo(_snapshot[final_vector[i]['to']])
            # 倒入另外一个杯子
            operation.fromContainerId = final_vector[i]['from']  # 设置源杯子ID,方便后面追踪
            operation.targetContainerId = final_vector[i]['to']  # 设置目标杯子ID,方便后面追踪
            current_tree_node = OperationTree(Util.takeSnapshot(_snapshot))  # 生成一个新的树节点
            current_tree_node.parent = tree_node  # 设置树父节点
            current_tree_node.selfOperation = operation  # 设置操作
            tree_node.operationPool.append(current_tree_node)  # 添加到父节点的操作树里面
            del _snapshot  # 删除快照,节省内存
            if self.resolve(current_tree_node):  # 开始对子节点求解
                return True  # 求解成功
        return False  # 所有情况都失败了

    @staticmethod
    def isWin(containers):  # 判断是否成功
        # 成功的依据:所有杯子全部满水或者全部为空
        for i in range(len(containers)):  # 遍历杯子列表
            if containers[i].getStackTopItemVolume() != 0 \
                    and containers[i].capacity != containers[i].getStackTopItemVolume():
                # 杯子水非空且非满
                return False  # 未成功
        return True  # 成功

    @staticmethod
    def findMovableContainers(containers):
        containers_top_color = {}  # 颜色列表，用于快速匹配
        universals = []  # 万能杯(空杯)
        for i in range(len(containers)):  # 遍历杯子列表
            if len(containers[i].containerMap) == 0:  # 如果杯子空，则添加到万能杯子列表
                universals.append(i)
                continue
            target_color = containers[i].containerMap[len(containers[i].containerMap) - 1]  # 获取顶端颜色
            if target_color in containers_top_color:  # 如果颜色已经存在
                containers_top_color[target_color].append(i)  # 添加到列表中
            else:
                containers_top_color[target_color] = [i]  # 否则创建列表
        for i in containers_top_color:  # 将万能杯添加到所有颜色列表中
            containers_top_color[i].extend(universals)
        vectors = []  # 可用向量列表
        for i in containers_top_color:
            vectors.extend(Util.vectorFullArrange(containers_top_color[i]))  # 计算每一种颜色的向量
            # 此时包括从空杯到有颜色杯子的“非法情况”，下面会进行排除
        available_moves = {'normal': [], 'lowPriority': []}  # 可用移动列表
        for i in range(len(vectors)):  # 遍历向量
            operation_is_legal = containers[vectors[i]['from']].canPourTo(containers[vectors[i]['to']])  # 判断是否合法
            if operation_is_legal == -1:
                # Illegal 不合法(如对面杯子已满,或来源杯子为空)
                continue
            score = Resolver.scoreOperation(containers, vectors[i])  # 对行为进行评分，使得其更快接近解
            vectors[i]['score'] = score  # 评分赋值到每个向量上
            if operation_is_legal == 0:
                # Legal ,but least consider
                # 合法但最后考虑，是倒到对方的杯子里但没有倒满
                available_moves['lowPriority'].append(vectors[i])
            if operation_is_legal == 1:
                # 合法且优先考虑
                available_moves['normal'].append(vectors[i])
        return available_moves

    @staticmethod
    def scoreOperation(containers, vector):
        if containers[vector['from']].getStackTopItemVolume() == 4:  # 这里非常重要！
            # 这一句的作用是避免从满的杯子倒向空的杯子，这样是没有任何意义的
            # 但是在下一句这样的操作会被赋予最高优先级(999),故必须先进行排除
            return -999
        if containers[vector['from']].getStackTopItemVolume() + containers[vector['to']].getStackTopItemVolume() == \
                containers[vector['to']].capacity:
            # 对即将合并的杯子给予最高优先级
            return 999
        if containers[vector['from']].getStackTopItemVolume() == len(containers[vector['from']].containerMap) and \
                containers[vector['from']].getStackTopItemVolume() + containers[vector['to']].getStackTopItemVolume() <= \
                containers[vector['to']].capacity:
            # 尽量产生出一个空杯(万能杯),以便后续的合并等操作
            return 998

        return 0

    @staticmethod
    def hasLoop(node): # 闭环检测
        current_node = node
        mapper = {}
        while current_node.parent is not None:
            node_md5 = hashlib.md5(str(current_node.snapshot)).hexdigest()
            if node_md5 in mapper:
                return True
            mapper[node_md5] = True
            current_node = current_node.parent
        return False
