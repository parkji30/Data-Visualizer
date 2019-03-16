"""
=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import math
import pygame

from tree_data import FileSystemTree
from population import PopulationTree

# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 600
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    tree_map = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
    if len(tree_map) == 0:
        pass
    else:
        for file_rect in tree_map:
            pygame.Surface.fill(screen, file_rect[1], file_rect[0])
        _render_text(screen, text)
    pygame.display.flip()


def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
    @type text: str
    @rtype: None
    """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @rtype: None
    """
    selected_leaf = ''
    rect = (0, 0, WIDTH, TREEMAP_HEIGHT)
    leaf_info = []
    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            # left click
            if event.button == 1:
                new_leaf = tree.locate_leaf(event.pos, rect)
                leaf_info = set_selected_leaf(new_leaf, selected_leaf)
                selected_leaf = leaf_info[0]
                # leaf's data size as a text.
                leaf_data = '  ' + leaf_info[1]
                render_display(screen, tree,
                               (selected_leaf + leaf_data).strip())
            # right click
            elif event.button == 3:
                new_leaf = tree.locate_leaf(event.pos, rect)
                tree.delete_leaf(new_leaf[0])
                leaf_info = set_selected_leaf(new_leaf, selected_leaf)
                selected_leaf = leaf_info[0]
                # leaf's data size as a text.
                leaf_data = '  ' + leaf_info[1]
                tree.data_size = tree.update_data_size()
                render_display(screen, tree,
                               (selected_leaf + leaf_data).strip())
                # No longer can the user update the previous
                # deleated leaf.
                leaf_info = []
                selected_leaf = ''
        elif event.type == pygame.KEYUP:
            # up key
            if event.key == pygame.K_UP and selected_leaf is not '':
                tree.increase_data_size(selected_leaf)
                leaf_data_size = int(leaf_info[1])
                leaf_data_size += math.ceil(leaf_data_size * 0.01)
                leaf_info[1] = str(leaf_data_size)
                tree.data_size = tree.update_data_size()
                # displays the new leaf data_size
                render_display(screen, tree, selected_leaf
                               + '  ' + str(leaf_data_size))
            # down key
            elif event.key == pygame.K_DOWN and selected_leaf is not '':
                tree.decrease_data_size(selected_leaf)
                leaf_data_size = int(leaf_info[1])
                leaf_data_size -= math.ceil(leaf_data_size * 0.01)
                leaf_info[1] = str(leaf_data_size)
                tree.data_size = tree.update_data_size()
                # displays the new leaf data_size
                render_display(screen, tree, selected_leaf
                               + '  ' + str(leaf_data_size))


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


def set_selected_leaf(leaf_info, selected_leaf):
    """Compares selected leaf to the first item in leaf_info. If the two
    are different or if selected_leaf is an empty string, selected_leaf
    will be set to that item. If the first item in leaf_info and the
    selected_leaf are the same string, selected_leaf will be set to an
    empty string.

    Returns the selected_leaf as either None or a new AbstractTree leaf.

    @type leaf_info: list[str]
    @type selected_leaf: str
    @rtype: str
    """
    if leaf_info[0] == selected_leaf:
        return['', '']
    else:
        selected_leaf = leaf_info[0]
        selected_leaf_data_size = leaf_info[1]
    return [selected_leaf, selected_leaf_data_size]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='pylintrc.txt')

    path1 = "C:/Users/James Park/Desktop/music"
    fst = FileSystemTree(path1)
    run_visualisation(fst)
