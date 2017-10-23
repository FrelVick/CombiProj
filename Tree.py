""" FROM TP3 """
class Node():
    
    def __init__(self, children = None):
        """
        A binary tree is either a leaf or a node with two subtrees.
        
        INPUT:
            
            - children, either None (for a leaf), or a list of size excatly 2 
            of either two binary trees or 2 objects that can be made into binary trees
        """
        self._isleaf = (children is None)
        if not self._isleaf:
            if len(children) != 2:
                raise ValueError("A binary tree needs exactly two children")
            self._children = tuple(c if isinstance(c,Node) else Node(c) for c in children)
        self._size = None
        
    def __repr__(self):
        if self.is_leaf():
            return "Leaf"
        return str(self._children)
    
    def __eq__(self, other):
        """
        Return true if other represents the same binary tree as self
        """
        if not isinstance(other, Node):
            return False
        if self.is_leaf():
            return other.is_leaf()
        if other.is_leaf():
            return False
        return self.left() == other.left() and self.right() == other.right()
    
    
    def left(self):
        """
        Return the left subtree of self
        """
        return self._children[0]
    
    def right(self):
        """
        Return the right subtree of self
        """
        return self._children[1]
    
    def is_leaf(self):
        """
        Return true is self is a leaf
        """
        return self._isleaf
    
    def _compute_size(self):
        """
        Recursively computes the size of self
        """
        if self.is_leaf():
            self._size = 0
        else:
            self._size = self.left().size() + self.right().size() + 1
    
    def size(self):
        """
        Return the number of non leaf nodes in the binary tree
        """
        if self._size is None:
            self._compute_size()
        return self._size
    
    def height(self):
        """
        Return the height of a binary tree
        """
        if self.is_leaf():
            return 0
        else:
            return 1 + max(self.left().height(), self.right().height())
    
Leaf = Node ()
