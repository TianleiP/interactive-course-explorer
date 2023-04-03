"""This file includes function that visualize the CourseGraph as well as specific parts of the graph.
It also includes interactive function that ask the user to input something and generate recommended courses
and visualization for the user."""
import random

import networkx as nx
import matplotlib.pyplot as plt
from proj_objects import CourseGraph
from proj_generate_graph import read_csv_with_graph, read_csv
from tkinter import *
from tkinter import messagebox, ttk


def generate_course_graph() -> CourseGraph:
    """generate a complete course graph from our current modified csv file"""
    g = read_csv('combined_math_cs_sta.csv')
    return g


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

    def search() -> None:
        """search the keyword"""

        def yes() -> None:
            """click the YES button"""
            visualize_course_graph_node(graph, courses)
            root_graph.destroy()

        lower = entry.get().lower()
        lst = graph.course_with_keywords(lower)
        if not lst:
            messagebox.showwarning(title='Warning',
                                   message='Sorry, the keyword you enter is currently not in our dataset.')
        else:
            root_graph = Tk()
            root_graph.geometry("700x400")
            graph_frame = ttk.Frame(root_graph)
            graph_frame.pack()

            current_index = random.randint(0, len(lst) - 1)
            courses = graph.compute_cost(lst[current_index])[1]
            cost = graph.compute_cost(lst[current_index])[0]

            label = Label(graph_frame,
                          text=f'{lst[current_index]} may be a course you are interested in, which is about'
                               f' {graph.courses[lst[current_index]].key_words}. \n In order to take this course,'
                               f' you can take the following courses as prerequisite to minimize cost:\n'
                               f' {courses}([] represent that you do not need any prerequisite for this course), '
                               f'\n which include a total of {cost} credit, (including {lst[current_index]})\n')
            label.pack()
            courses.append(lst[current_index])
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
            label_course = Label(graph_frame,
                                 text=f'you can probably organize it in this way\n first year: {lst1} '
                                      f'\nsecond year: {lst2},\n third year: {lst3},\n last year: {lst4} \n')
            label_course.pack()

            label_visual = Label(graph_frame,
                                 text=f'Do you want an visualization? \n If you choose to visualize,'
                                      f' you need to close the visualize window in order to continue:\n')
            label_visual.pack()

            button_yes = ttk.Button(graph_frame, text="Yes", command=yes)
            button_yes.pack()

            button_no = ttk.Button(graph_frame, text="No", command=root_graph.destroy)
            button_no.pack()

            root_graph.mainloop()

    root = Tk()
    root.geometry("600x300")
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=100)

    graph = generate_course_graph()

    label_intro = ttk.Label(search_frame, text="please identify an area you are focusing on (choose a specific word)")
    label_intro.pack()

    entry = ttk.Entry(search_frame, width=20)
    entry.pack()

    button_submit = ttk.Button(search_frame, text="submit", command=search)
    button_submit.pack()
    root.mainloop()


def interactive_show_course() -> None:
    """Ask the user to input a specific coursecode, for example, MAT137Y1, and show all of the prerequisite
    the user can take in order to take this course. including the prerequisite of prerequisite, etc"""

    def check() -> None:
        """check the prerequisite"""
        course = entry.get().upper()
        if course not in graph.courses:
            messagebox.showwarning(title='Warning',
                                   message='Sorry, the course code you enter is not within our dataset.')
        else:
            pre = graph.find_all_prereq(course)
            pre.append(course)
            visualize_course_graph_node(graph, pre)
            root.destroy()

    root = Tk()
    root.geometry("600x300")
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=100)

    graph = generate_course_graph()

    label_intro = ttk.Label(search_frame,
                            text="please identify a course that you want to see all of its prerequisite (enter a "
                                 "course code):")
    label_intro.pack()

    entry = ttk.Entry(search_frame, width=20)
    entry.insert(0, 'MAT157Y1')
    entry.pack()

    button_submit = ttk.Button(search_frame, text="submit", command=check)
    button_submit.pack()

    root.mainloop()


def interactive_show_future_course() -> None:
    """Ask the user to input some course he/she already took, and return the potential possible course the user could
    take in the future"""

    def find_potential() -> None:
        """find the potential possible course"""

        def yes() -> None:
            """visualize the relationships"""
            visualize_course_graph_node(graph, lst2)
            root_protential.destroy()

        course = entry.get().upper()
        lst = course.split(" ")
        error = [item for item in lst if item not in graph.courses]
        error_message = ", ".join(error)
        if len(error) != 0:
            messagebox.showwarning(title='Warning',
                                   message=f'The courses {error_message} are not in our dataset')
        else:
            root_protential = Tk()
            root_protential.geometry("700x400")
            protential_frame = ttk.Frame(root_protential)
            protential_frame.pack()

            lst2 = graph.find_higher_courses(lst)

            label_courses = Label(protential_frame,
                                  text=f'Based on your input, here are the courses you have already token: \n{lst}, \n'
                                       f'and here are some potential courses you could take in the future: '
                                       f'\n{lst2[:min(5, len(lst2))]}')
            label_courses.pack()
            lst2.extend(lst)
            label_visual = Label(protential_frame,
                                 text=f'Do you want to visualize their relationship?')
            label_visual.pack()

            button_yes = ttk.Button(protential_frame, text="Yes", command=yes)
            button_yes.pack()

            button_no = ttk.Button(protential_frame, text="No", command=root_protential.destroy)
            button_no.pack()

            root_protential.mainloop()

    root = Tk()
    root.geometry("600x300")
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=100)

    graph = generate_course_graph()

    label_intro = ttk.Label(search_frame,
                            text="Please add a course code that you've already token (use spaces to slipt courses).")
    label_intro.pack()

    entry = ttk.Entry(search_frame, width=40)
    entry.insert(0, 'MAT137Y1')
    entry.pack()

    button_submit = ttk.Button(search_frame, text="submit", command=find_potential)
    button_submit.pack()

    root.mainloop()


def interactive_model() -> None:
    """The final interactive model of the project, which combines the above interactive function"""
    root = Tk()
    root.geometry("600x300")
    main_frame = ttk.Frame(root)
    main_frame.pack()

    var = StringVar()
    var.set("Hello! As an interactive graph model, there are a few ways I can help you.\n"
            "1. You can input a keyword that you are interested in, and I will help you \n"
            "look for the related courses within our dataset, as well as the courses you \n"
            "need to take in order to take this specific course. We will try our best to \n"
            "minimized the opportunity cost you need to give in order to take these courses.\n"
            "2. you can input a specific course code, and I will help you visualize all potential\n"
            "prerequisite, as well as all potential pre-prerequisite, etc. of this course.\n"
            "3. you can input a few course codes you have already token, and I will help you find and visualize the \n"
            "relationship between some potential courses you could take in the future!\n")

    label = Label(main_frame, textvariable=var)
    label.pack()

    button_graph = ttk.Button(main_frame, text="1", command=interactive_graph)
    button_graph.pack()

    button_course = ttk.Button(main_frame, text="2", command=interactive_show_course)
    button_course.pack()

    button_future = ttk.Button(main_frame, text="3", command=interactive_show_future_course)
    button_future.pack()

    root.mainloop()
