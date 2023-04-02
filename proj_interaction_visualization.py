"""This file includes function that visualize the CourseGraph as well as specific parts of the graph.
It also includes interactive function that ask the user to input something and generate recommended courses
and visualization for the user."""

import networkx as nx
import matplotlib.pyplot as plt
from proj_main import Course, CourseGraph
from proj_generate_graph import read_csv_with_graph, read_csv


def generate_course_graph() -> CourseGraph:
    """generate a complete course graph from our current modified csv file"""
    g = read_csv('modified_cs.csv')
    g1 = read_csv_with_graph('modified_math.csv', g)
    g2 = read_csv_with_graph('modified_sta.csv', g1)
    return g2


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


def visualize_whole_coursegraph() -> None:
    """visualize the whole graph using networkx"""
    graph = generate_course_graph()
    visualize_course_graph(graph)


def interactive_graph() -> None:
    """Ask the user to input a specific keyword, for example, algorithm, and print out
    some recommended courses for this user, as well as its potential prerequisite that minimize the
    opportunity cost(a year course have opportunity cost of 1 and half year course have 0.5) for taking
    this course. Visualize the relationship between the recommended courses and its potential prerequisite. """

    graph = generate_course_graph()
    keyword = input("please identify an area you are focusing on (choose a specific word)")
    lower = keyword.lower()
    lst = graph.course_with_keywords(lower)
    while not lst:
        w = input('sorry, the keyword you enter is '
                  'currently not in our dataset. Do you want to try another one? (Yes/No)')
        whether_continue = w.lower()
        if whether_continue != 'yes':
            return
        keyword = input("please identify an area you are focusing on (choose a specific word)")
        lower = keyword.lower()
        lst = graph.course_with_keywords(lower)
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
            f'last year: {lst4}\n')
        v = input('Do you want an visualization? (Yes/No). If you choose to visualize, you need to close the '
                  'visualize window in order to continue:\n')
        lower_v = v.lower()  # user can input lower case as well as upper case
        if lower_v == 'yes':
            visualize_course_graph_node(graph, courses)


def interactive_show_course() -> None:
    """Ask the user to input a specific coursecode, for example, MAT137Y1, and show all of the prerequisite
    the user can take in order to take this course. including the prerequisite of prerequisite, etc"""

    graph = generate_course_graph()
    c = input("please identify a course that you want to see all of its prerequisite(enter a course code):")
    course = c.upper()
    while course not in graph.courses:
        print("sorry, the course code you enter is not within our dataset\n")
        w = input("Do you want to continue? (Yes/No)")
        whether_continue = w.lower()
        if whether_continue != 'yes':
            return
        c = input("please identify a course that you want to see all of its prerequisite(enter a course code):")
        course = c.upper()
    pre = graph.find_all_prereq(course)
    pre.append(course)
    visualize_course_graph_node(graph, pre)


def interactive_show_future_course() -> None:
    """Ask the user to input some course he/she already took, and return the potential possible course the user could
    take in the future"""
    graph = generate_course_graph()
    lst = []
    w = input("Please add a course code that you've already token(enter no to stop):")
    course = w.upper()
    while course != 'NO':
        if course in graph.courses:
            lst.append(course)
        else:
            print('sorry, the course code you enter is currently not in our dataset')
        w = input("Please add a course code that you've already token(enter no to stop):")
        course = w.upper()
    lst2 = graph.find_higher_courses(lst)
    print(f'Based on your input, here are the courses you have already token: {lst}, and here are some potential '
          f'courses you could take in the future: {lst2}\n')
    lst2.extend(lst)
    v = input('Do you want to visualize their relationship? (yes/no)')
    vis = v.lower()
    if vis == 'yes':
        visualize_course_graph_node(graph, lst2)
    else:
        print('Thanks for using!')


def interactive_model() -> None:
    """The final interactive model of the project, which combines the above interactive function"""
    print("Hello! As an interactive graph model, there are a few ways I can help you.\n"
          "1. You can input a keyword that you are interested in, and I will help you \n"
          "look for the related courses within our dataset, as well as the courses you \n"
          "need to take in order to take this specific course. We will try our best to \n"
          "minimized the opportunity cost you need to give in order to take these courses.\n"
          "2. you can input a specific course code, and I will help you visualize all potential\n"
          "prerequisite, as well as all potential pre-prerequisite, etc. of this course.\n"
          "3. you can input a few course codes you have already token, and I will help you find and visualize the \n"
          "relationship between some potential courses you could take in the future!\n")
    num = input('choose the function you hope to use: (1,2 or 3, just type a single number).')
    if num == '1':
        interactive_graph()
    elif num == '2':
        interactive_show_course()
    elif num == '3':
        interactive_show_future_course()
    else:
        print('Sorry, I can not reconize the number you chose')
        b = input('Do you want to try again?(Yes/No):')
        w = b.lower()
        if w == 'yes':
            interactive_model()
        else:
            print('Thank you for using!')
    i = input('Thank you for using our interactive model! Do you want to use it again? (Yes/No):')
    inp = i.lower()
    if inp == 'yes':
        interactive_model()
    else:
        print('Hope our model help you!')
