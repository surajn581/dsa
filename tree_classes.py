from tree_utils import printTree as ptree

RED = 'red'
BLACK = 'black'
RIGHT = 'right'
LEFT = 'left'
NULL = 'NULL'

class Value:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return '[{key}:{value}]'.format(key = self.key, value = self.value)
    
    def __gt__(self, other):
        return self.key > other.key
    
    def __lt__(self, other):
        return self.key < other.key
    
    def __eq__(self, other):
        return self.key == other.key
    
    def __ge__(self, other):
        return self.key >= other.key
    
    def __le__(self, other):
        return self.key <= other.key
    
    def __ne__(self, other):
        return self.key != other.key
    
class NodeBase:

    def __init__(self, value, side = None, parent = None, leftChild = None, rightChild = None):
        if (parent and not side):
            raise Exception('side not assigned. node must have a side assigned when it is not a root node')
        self.value = value
        self.side = side
        self.parent = parent
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __gt__(self, other):
        return self.value > other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    @property
    def key(self):
        return self.value.key
    
    @property
    def isLeft(self):
        return True if self.side==LEFT else False
    
    @property
    def isRight(self):
        return True if self.side==RIGHT else False
    
    @property
    def isNone(self):
        return True if self.value is None else False
    
    @property
    def isLeaf(self):
        return (self.leftChild is None) and (self.rightChild is None)
    
    @property
    def isRoot(self):
        return True if self.parent is None else False
    
    @property
    def children(self):
        return [ child for child in [ self.leftChild, self.rightChild ] if child ]
    
    def __repr__(self) -> str:
        return "{value}".format(value = self.value)
    
class BinaryNode(NodeBase):
    def __init__(self,
                 value,
                 side       = None,
                 leftChild  = None,
                 rightChild = None,
                 parent     = None):        
        super().__init__(value, side = side, leftChild = leftChild, rightChild = rightChild, parent = parent)

    @property
    def sibling(self):
        if self.isRoot:
            return
        return self.parent.rightChild if self.isLeft else self.parent.leftChild
    
class RedBlackNode(BinaryNode):
    
    def __init__(self,
                 value,
                 side       = None,
                 color      = RED,
                 leftChild  = None,
                 rightChild = None,
                 parent     = None):        
        super().__init__(value, side = side, leftChild = leftChild, rightChild = rightChild, parent = parent)
        self.color = color
   
    @property
    def isRed(self):
        return True if self.color==RED else False
    
    @property
    def isBlack(self):
        return not self.isRed
    
    def __repr__(self) -> str:        
        return "{value}:{color}".format(value = super().__repr__(), color = self.color[0])
    
    @property
    def grandParent(self):
        if self.isRoot:
            raise Exception('root node {node} does not have grand parent'.format(node = self))
        if self.parent.isRoot:
            raise Exception('node {node} has parent {root} which is root'.format(node = self, root = self.parent))
        return self.parent.parent
    
    @property
    def hasGrandParent(self):
        return False if self.isRoot or self.parent.isRoot else True
    
    @property
    def aunt(self):
        if self.hasGrandParent:
            return self.grandParent.rightChild if self.parent.isLeft else self.grandParent.leftChild
        raise Exception('node {node} does not have a grand parent'.format(node = self))
    
class Tree:

    def __init__(self):
        self.root = None
    
    def __repr__(self) -> str:
        linestrList, pstrList = ptree(self.root)
        lines = []
        for linestr, pstr in zip(linestrList, pstrList):
            lines.append(linestr)
            lines.append(pstr)
        return '\n'.join(lines)
    
    @property
    def height(self):
        return 1+self._height(self.root)
    
    @property
    def isEmpty(self):
        return self.root is None

    def _height(self, node):
        if node is None or node.isLeaf:
            return 0
        return max( self._height(node.leftChild), self._height(node.rightChild) ) + 1