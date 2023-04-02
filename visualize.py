import networkx as nx
import matplotlib.pyplot as plt


def visualize_course_graph(course_graph):
    # create a networkx graph object
    G = nx.DiGraph()

    # add nodes to the graph
    for course_name in course_graph.courses:
        G.add_node(course_name)

    # add edges to the graph
    for course_name, course_obj in course_graph.courses.items():
        for higher_course_name in course_obj.higher_courses:
            G.add_edge(course_name, higher_course_name)

    # draw the graph
    nx.draw(G, with_labels=True)
    plt.show()


def visualize_course_graph_with_levels(course_graph):
    """
    Visualizes the given course graph with levels of courses based on the fourth digit of the course code.

    :param course_graph: the course graph to visualize
    """
    G = nx.DiGraph()

    # add nodes to the graph
    for course_name in course_graph.courses:
        G.add_node(course_name)

    # add edges to the graph
    for course_name, course_obj in course_graph.courses.items():
        for higher_course_name in course_obj.higher_courses:
            G.add_edge(course_name, higher_course_name)

    levels = {}
    for node in G.nodes():
        levels[node] = int(node[3])

    # Compute the position of each node
    pos = hierarchy_pos(G, root='CSC108H1', levels=levels, width=1., height=1.)

    # Draw the graph
    nx.draw(G, pos=pos, with_labels=True, node_size=1500, font_size=10, node_color='#4CB4E7')
    print('ababababababa')


def hierarchy_pos(G, root, levels=None, width=1., height=1., sep=10):
    """Compute the layout of a tree-like graph in a hierarchical way.

    Parameters:
    - G: the graph (must be a tree)
    - root: the root node of the tree
    - levels: a dictionary that maps each node to its level (optional)
    - width, height: size of the figure
    - sep: separation between nodes

    Returns:
    - pos: a dictionary that maps each node to its (x, y) coordinates
    """
    if levels is None:
        levels = {root: 0}
    else:
        root = max(levels, key=levels.get)
    max_level = max(levels.values())
    pos = {root: (0.5 * width, 0)}
    for level in range(1, max_level + 1):
        nodes = [node for node in G.nodes() if levels[node] == level]
        nodes.sort()
        count = len(nodes)
        for i, node in enumerate(nodes):
            pos[node] = ((i + 0.5) * width / count, -level * height - level * sep)
    return pos
