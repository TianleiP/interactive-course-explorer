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


def visualize_course_graph_node(course_graph, nodes: list):
    # create a networkx graph object
    G = nx.DiGraph()

    # add nodes to the graph
    for course_name in nodes:
        G.add_node(course_name)

    # add edges to the graph
    for course_name, course_obj in course_graph.courses.items():
        if course_name in nodes:
            for higher_course_name in course_obj.higher_courses:
                if higher_course_name in nodes:
                    G.add_edge(course_name, higher_course_name)

    # draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()
