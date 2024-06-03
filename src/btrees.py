from typing import Tuple, List

class BTree:

    def __init__(self, value, parent=None, left=None, right=None):
        self.value: int    = value
        self.parent   = parent
        self.left: BTree     = left
        self.right: BTree    = right
        self.diameter = 0

    def getOffsetFromRoot(self, curLeftOffset, curRightOffset) -> Tuple[int, int]:

        if not self.left and not self.right:
            return (curLeftOffset, curRightOffset)

        leftOffsetFromLeftChild, rightOffsetFromLeftChild = 0, 0
        leftOffsetFromRightChild, rightOffsetFromRightChild = 0, 0
        if self.left:
            leftOffsetFromLeftChild, rightOffsetFromLeftChild = self.left.getOffsetFromRoot(curLeftOffset + 1, curRightOffset)
        if self.right:
            leftOffsetFromRightChild, rightOffsetFromRightChild = self.right.getOffsetFromRoot(curLeftOffset, curRightOffset + 1)
        
        return (max(curLeftOffset, leftOffsetFromLeftChild, leftOffsetFromRightChild), max(curRightOffset, rightOffsetFromLeftChild, rightOffsetFromRightChild))


    def loadTreeFromConfig(configs: List):
        bTreeNodeMapping = {} # maps unique id to BTree node
        for config in configs['nodes']:
            if config['id'] in bTreeNodeMapping:
                raise Exception("Non unique BTree id ", config['id'])

            node = BTree(config['value'])
            bTreeNodeMapping[config['id']] = node
        try:
            for config in configs['nodes']:
                    node = bTreeNodeMapping[config['id']]
                    if config['parent']:
                        node.parent = bTreeNodeMapping[config['parent']]
                    if config['left']:
                        node.left = bTreeNodeMapping[config['left']]
                    if config['right']:
                        node.right = bTreeNodeMapping[config['right']]
            return bTreeNodeMapping[configs['root']]
        except KeyError as e:
            print("FATAL: Keyerror. Should not happen %s", e)

    def inOrderTraversal(self, aggregator) -> List[int]:
        if not self.left and not self.right:
            aggregator += [self.value]
            return aggregator

        if self.left:
            self.left.inOrderTraversal(aggregator)
        aggregator += [self.value]
        if self.right:
            self.right.inOrderTraversal(aggregator)
        return aggregator
    
if __name__ == "__main__":
    configs = {
        "nodes": [
            {"id": "1", "left": "2", "parent": None, "right": "3", "value": 1},
            {"id": "2", "left": "4", "parent": "1", "right": "5", "value": 2},
            {"id": "3", "left": None, "parent": "1", "right": None, "value": 3},
            {"id": "4", "left": "6", "parent": "2", "right": None, "value": 4},
            {"id": "5", "left": None, "parent": "2", "right": None, "value": 5},
            {"id": "6", "left": None, "parent": "4", "right": None, "value": 6}
            ],
            "root": "1"
        }
    tree: BTree = BTree.loadTreeFromConfig(configs)

    print(tree.inOrderTraversal([]))
    print(tree.getOffsetFromRoot(0,0))
