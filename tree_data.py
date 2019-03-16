"""
Using GUI to visualize the byte size of files in a repository through recursive methods.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None

        >>> t1 = AbstractTree(1, [], 30)
        >>> t1.is_empty()
        False
        >>> len(t1._subtrees) == 0
        True
        >>> t1._parent_tree is None
        True
        >>> x, y, z = t1.colour
        >>> x in range(0, 256)
        True
        >>> y in range(0, 256)
        True
        >>> z in range(0, 256)
        True
        >>> t1.data_size
        30
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        # data size of the tree.
        self.data_size = data_size
        if len(self._subtrees) > 0:
            for subtree in self._subtrees:
                self.data_size += subtree.data_size
        # sets the parent tree of each subtree as self.
        for subtree in self._subtrees:
            subtree._parent_tree = self

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
        @rtype: bool

        >>> at0 = AbstractTree(0, [], 30)
        >>> at0.is_empty()
        False
        >>> at = AbstractTree(None, [])
        >>> at.is_empty()
        True
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        Precondition: rect width != height

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]

        >>> path = "C:/Users/James Park/Desktop/photos"
        >>> fst = FileSystemTree(path)
        >>> tree_map = fst.generate_treemap((0, 0, 1024, 768))
        >>> len(tree_map) > 0
        True
        """
        treemap_lst = []
        remainder = 0
        subtrees = self._subtrees
        index = 0
        if self.data_size == 0:  # self is a leaf and has 0 data
            return treemap_lst
        elif len(self._subtrees) == 0:  # self is a leaf and has some data
            treemap_lst += [(rect, self.colour)]
        else:  # self is not a leaf
            # divide the rectangles vertically
            if rect[2] > rect[3]:
                x_position = rect[0]
                while index != len(subtrees) - 1:
                    width = rect[2] * (subtrees[index].data_size
                                       / self.data_size)
                    width = math.floor(width)
                    v_rect = (x_position, rect[1], width, rect[3])
                    treemap_lst += subtrees[index].generate_treemap(v_rect)
                    remainder += width
                    x_position += width
                    index += 1
                width = rect[2] - remainder
                v_rect = (x_position, rect[1], width, rect[3])
                treemap_lst += subtrees[index].generate_treemap(v_rect)
            # divide the rectangles horizontally
            elif rect[3] > rect[2]:
                y_position = rect[1]
                while index != len(subtrees) - 1:
                    height = rect[3] * (subtrees[index].data_size
                                        / self.data_size)
                    height = math.floor(height)
                    h_rect = (rect[0], y_position, rect[2], height)
                    treemap_lst += subtrees[index].generate_treemap(h_rect)
                    remainder += height
                    y_position += height
                    index += 1
                height = rect[3] - remainder
                h_rect = (rect[0], y_position, rect[2], height)
                treemap_lst += subtrees[index].generate_treemap(h_rect)
        return treemap_lst

    def locate_leaf(self, pos, rect):
        """Returns the path of the node from itself to its parent tree
        and the node's data_size as a list of strings.

        Searches through the tree recursively, creating new rectangles for
        each file similarily to generate_treemap and finds the recatangle
        which contains pos inside its space.

        Precondition: pos is a tuple of two positive integers.

        @type self: AbstractTree
        @type pos: (int, int, int, int)
        @type rect: (int, int, int, int)
        @rtype: list[str]
        """
        remainder = 0
        leaf_data = []
        if self.data_size == 0:
            return ['', '']
        elif len(self._subtrees) == 0:
            leaf_data = [self.get_separator(), str(self.data_size)]
        else:
            if rect[2] > rect[3]:
                x_position = rect[0]
                for subtree in self._subtrees:
                    if subtree == self._subtrees[-1]:
                        width = rect[2] - remainder
                        v_rect = (x_position, rect[1], int(width), rect[3])
                    else:
                        width = rect[2]*(subtree.data_size/self.data_size)
                        width = math.floor(width)
                        v_rect = (x_position, rect[1], int(width), rect[3])
                        remainder += width
                        x_position += width
                    x_range = v_rect[0] + v_rect[2]
                    y_range = v_rect[1] + v_rect[3]
                    if pos[0] in range(x_range) and pos[1] in range(y_range):
                        leaf_data = subtree.locate_leaf(pos, v_rect)
                        break
            else:
                y_position = rect[1]
                for subtree in self._subtrees:
                    if subtree == self._subtrees[-1]:
                        height = rect[3] - remainder
                        h_rect = (rect[0], y_position, rect[2], int(height))
                    else:
                        height = rect[3]*(subtree.data_size/self.data_size)
                        height = math.floor(height)
                        h_rect = (rect[0], y_position, rect[2], int(height))
                        remainder += height
                        y_position += height
                    x_range = h_rect[0] + h_rect[2]
                    y_range = h_rect[1] + h_rect[3]
                    if pos[0] in range(x_range) and pos[1] in range(y_range):
                        leaf_data = subtree.locate_leaf(pos, h_rect)
                        break
        return leaf_data

    def increase_data_size(self, leaf):
        """Takes the given leaf of the tree and increases its data size by
        1%. Adjusts all of the subtrees and the entire tree's data size
        accordingly.

        Precondition: leaf must be a valid leaf node of this class.

        There is no upper limit on the leaf's data_size.

        Used in treemap_visualiser to increase the leaf's data_size
        whenever the up key is pressed.

        @type self: AbstractTree
        @type leaf: AbstractTree
        @rtype: None
        """
        leaf_name = os.path.basename(leaf)
        if self._root == leaf:
            self.data_size += math.ceil((self.data_size*0.01))
        else:
            for subtree in self._subtrees:
                subtree.increase_data_size(leaf_name)
                subtree.data_size = subtree.update_data_size()

    def decrease_data_size(self, leaf):
        """Takes the given leaf of the tree and decreases its data size
        by 1%. Adjusts all of the subtrees and the entire tree's data
        size accordingly.

        Precondition: leaf must be a valid leaf node of this class.

        The leaf's data_size cannot drop below 1.

        Used in treemap_visualiser to decrease the leaf's data_size
        whenever the down key is pressed.

        @type self: AbstractTree
        @type leaf: AbstractTree
        @rtype: None
        """
        leaf_name = os.path.basename(leaf)
        if self._root == leaf_name:
            self.data_size -= math.ceil((self.data_size * 0.01))
            if self.data_size < 1:
                self.data_size = 1
        else:
            for subtree in self._subtrees:
                subtree.decrease_data_size(leaf_name)
                subtree.data_size = subtree.update_data_size()

    def update_data_size(self):
        """Finds the total data_size of self by recursing through each of
        the subtrees in self with a data_size > 0.

        If the subtree has a data_size of 0, it will be ignored.

        Used in treemap_visualizer whenever the data_size of the tree is
        altered.

        @type self: FileSystemTree
        @rtype: int
        """
        updated_data_size = 0
        if len(self._subtrees) == 0:
            return self.data_size
        else:
            for subtree in self._subtrees:
                updated_data_size += subtree.update_data_size()
        return updated_data_size

    def delete_leaf(self, leaf):
        """Locates the given leaf inside the tree and sets it as an empty tree.
        Meaning that its root is set to None, it will have no subtrees and its
        data_size will be set to 0.

        Updates entire tree's data_size accordingly.

        The leaf will still be inside the subtree of its parent tree. It
        will simply be ignored when generate_treemap is run on the tree.

        Used by treemap_visualiser to rerender the AbstractTree without
        the selected leaf.

        @type self: AbstractTree
        @type leaf: str
        @rtype: None
        """
        leaf_name = os.path.basename(leaf)
        found = False
        if self._root == leaf_name:
            self._root = None
            self._subtrees = []
            return True
        elif len(self._subtrees) == 0:
            return False
        else:
            for subtree in self._subtrees:
                if found is False:
                    if subtree.delete_leaf(leaf_name):
                        subtree.data_size = 0
                        found = True
                subtree.data_size = subtree.update_data_size()

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None

        >>> path = "C:/Users/James Park/Desktop/test1"
        >>> fst = FileSystemTree(path)
        >>> fst._root
        'test1'
        >>> fst.data_size > 0
        True
        >>> fst._parent_tree is None
        True
        >>> x, y, z = fst.colour
        >>> x in range(0, 256)
        True
        >>> y in range(0, 256)
        True
        """
        self._name = path

        if os.path.isfile(self._name):
            AbstractTree.__init__(self, os.path.basename(self._name), [])
            self.data_size = os.path.getsize(self._name)
        elif os.path.isdir(self._name):
            AbstractTree.__init__(self, os.path.basename(self._name), [])
            for file_name in os.listdir(self._name):
                directory_item = os.path.join(self._name, file_name)
                temp_fst = FileSystemTree(directory_item)
                self._subtrees += [temp_fst]
            for file in self._subtrees:
                self.data_size += file.data_size
                file._parent_tree = self

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        @type self: FileSystemTree
        @rtype: str

        >>> path = "C:/Users/James Park/Desktop/test1"
        >>> fst = FileSystemTree(path)
        >>> fst.get_separator()
        'test1'
        """
        route = ''
        if self._parent_tree is None:
            return str(self._root)
        else:
            route += self._parent_tree.get_separator()
            route += ("\\" + str(self._root))
        return route


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
