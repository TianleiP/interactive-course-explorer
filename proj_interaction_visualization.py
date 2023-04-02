"""This file includes function that visualize the CourseGraph as well as specific parts of the graph.
It also include interactive function that ask the user to input something and generate recommended courses
and visualization for the user."""

import networkx as nx
import matplotlib.pyplot as plt
from proj_main import Course, CourseGraph
from proj_generate_graph import read_csv_with_graph, read_csv


def visualize_course_graph(course_graph: CourseGraph) -> None:
    """visualize the whole course graph"""
    g = nx.DiGraph()
    for course_name in course_graph.courses:
        g.add_node(course_name)
    for course_name, course_obj in course_graph.courses.items():
        for higher_course_name in course_obj.higher_courses:
            g.add_edge(course_name, higher_course_name)
    nx.draw(g, with_labels=True)
    plt.show()


def visualize_course_graph_node(course_graph: CourseGraph, nodes: list) -> None:
    """visualize the interaction betwee a list of input node
    preconditions:
    - all(node in course_graph.courses for node in nodes)
    """
    g = nx.DiGraph()
    for course_name in nodes:
        g.add_node(course_name)
    for course_name, course_obj in course_graph.courses.items():
        if course_name in nodes:
            for higher_course_name in course_obj.higher_courses:
                if higher_course_name in nodes:
                    g.add_edge(course_name, higher_course_name)
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True)
    plt.show()


def visualize_whole_coursegraph(graph: CourseGraph) -> None:
    """visualize the whole graph using networkx"""
    visualize_course_graph(graph)


def interactive_graph(graph: CourseGraph) -> None:
    """Ask the user to input a specific keyword, for example, algorithm, and print out
    some recommended courses for this user, as well as its potential prerequisite that minimize the
    opportunity cost(a year course have opportunity cost of 1 and half year course have 0.5) for taking
    this course. Visualize the relationship between the recommended courses and its potential prerequisite. """

    keyword = input("please identify an area you are focusing on (choose a specific word)")
    lower = keyword.lower()
    lst = graph.course_with_keywords(lower)
    if not lst:
        print('Sorry, your keyword is not in our database, please try another one')
    else:
        for item in lst:
            courses = graph.compute_cost(item)[1]
            cost = graph.compute_cost(item)[0]
            print(f'{item} may be a course you are interested in, which is about {graph.courses[item].key_words}. '
                  f'In order to take this course, \n you can take the following courses as prerequisite to minimize '
                  f'cost: {courses}([] represent that \n you do not need any prerequisite for this course), which '
                  f'include a total of {cost} credit, (including {item})\n')
            courses.append(item)
            lst1 = []
            lst2 = []
            lst3 = []
            lst4 = []
            for course in courses:
                if course[3] == '1':
                    lst1.append(course)
                elif course[3] == '2':
                    lst2.append(course)
                elif course[3] == '3':
                    lst3.append(course)
                else:
                    lst4.append(course)
            print(
                f'you can probably organize it in this way, first year: {lst1}, '
                f'second year: {lst2}, third year: {lst3},'
                f'last year: {lst4}')
            visualize_course_graph_node(graph, courses)


def interactive_show_course(graph: CourseGraph) -> None:
    """Ask the user to input a specific coursecode, for example, MAT137Y1, and show all of the prerequisite
    the user can take in order to take this course. including the prerequisite of prerequisite, etc"""

    course = input("please identify a course that you want to see all of its prerequisite(enter a course code):")
    if course not in graph.courses:
        print("sorry, the course code you enter is not within our dataset")
    pre = graph.find_all_prereq(course)
    pre.append(course)
    visualize_course_graph_node(graph, pre)
