class node(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
def depth(tree):
    if tree == None:
        return 0
    else:
        left, right = depth(tree.left), depth(tree.right)
        return max(left, right)+1
def pre_order(tree):
    if tree == None:
        return
    else:
        print (tree.data)
        pre_order(tree.left)
        pre_order(tree.right)
def mid_order(tree):
    if tree == None:
        return
    else:
        mid_order(tree.left)
        print (tree.data)
        mid_order(tree.right)
def post_order(tree):
    if tree == None:
        return
    else:
        post_order(tree.left)
        post_order(tree.right)
        print (tree.data)
#depth traverse
def depth_order(tree):
    if tree == None:
        return
    else:
        print (tree.data)
        if tree.left != None:
            depth_order(tree.left)
        if tree.right != None:
            depth_order(tree.right)
def level_order(tree):
    if tree == None:
        return
    else:
        stack = []
        stack.append(tree)
        while stack:
            current = stack.pop(0)
            print (current.data)
            if current.left != None:
                stack.append(current.left)
            if current.right != None:
                stack.append(current.right)
if __name__ == '__main__':
    tree = node('A', node('B', node('D'), node('E')), node('C'))
    print (depth(tree))
    print (pre_order(tree))
    print (mid_order(tree))
    print (post_order(tree))
    print (depth_order(tree))
    print (level_order(tree))