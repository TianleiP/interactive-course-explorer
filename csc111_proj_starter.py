import csv
from typing import Any, Optional


class Course:
    """
    name: name of the course.
    prereq: courses required in order to take this course.
    higher_courses: the courses that include this course as prerequisite.

    For example, if the prereq of course 'whateverthatis' is '(grade >= 70 for course MAT137 or pass for MAT157),
    and grade >= 75 for CSC111', then self.prereq will looks like:{({'MAT137': 70}, {'MAT157':50}), {'CSC111':75}}. In
    this case, the prerequisite is satisfied if and only if any if the requirement for (MAT137 and MAT157) is
    satisfied, and the score for CSC111 is not lower than 75. If the prereq of the course is MAT137 or MAT157, then
    self.prereq will be like {({'MAT157':50}, {'MAT223':50})}, which minimum grade requirement is set to 50 by default.
    """
    name: str
    prereq: set
    higher_courses: set

    def __init__(self, name: str):
        self.name = name
        self.prereq = set()
        self.higher_courses = set()




def compute_prereq(information: str) -> set:
    """compute a set of prerequisite based on information contained in a line in the csv file"""
    # implement this based on the actual format of the csv file, may use additional helper function.


class CourseGraph:
    """
    A graph representation of the course system.
    """
    courses: dict[str, Course]

    def __init__(self):
        self.courses = {}

    def add_course(self, name: str) -> None:
        """add courses to the graph"""
        self.courses[name] = Course(name)

    def add_edge(self, course1: str, prereq: Any) -> None:
        """add edge between a course and all of its prerequisite"""
        if course1 not in self.courses:
            self.add_course(course1)
        curr_course = self.courses[course1]
        curr_course.prereq.add(prereq)
        self._add_edge(course1, prereq)

    def _add_edge(self, course: str, prereq: Any) -> None:
        for item in prereq:
            if isinstance(item, dict):
                for coursename in item:
                    if coursename not in self.courses:
                        self.add_course(coursename)
                    curr_course = self.courses[coursename]
                    curr_course.higher_courses.add(course)
            else:
                self._add_edge(course, item)

    def compute_cost(self, course: Any) -> float:
        """ compute the total opportunity cost needed in order to finish this course.
        for each course, if it's a year course, it's opportunity cost is 1 + total cost
        of its prerequisite. If it's a half year course, it's opportunity is 0.5 + total
        cost of its prerequisite."""
        if isinstance(course, str):
            curr_course = self.courses[course]
            if curr_course.prereq == set():
                if self.is_year_course(course):
                    return 1.0
                else:
                    return 0.5
            else:
                cost = 0
                for item in curr_course.prereq:
                    if isinstance(item, dict):
                        for key in item:
                            cost += self.compute_cost(key)
                    else:
                        cost += self.compute_cost(item)
                if self.is_year_course(course):
                    cost += 1.0
                else:
                    cost += 0.5
                return cost
        elif isinstance(course, set):
            if course == set():
                return 0.0
            else:
                cost = 0.0
                for item in course:
                    cost += self.compute_cost(item)
                return cost
        else:
            if course == ():
                return 0
            else:
                lst = []
                for item in course:
                    lst.append(self.compute_cost(item))
                return min(lst)


    def is_year_course(self, course: str) -> bool:
        """return whether a course is a year course or a half year course"""
        if course[6] == 'Y':
            return True
        else:
            return False



def create_graph(course: str, prereq: set) -> CourseGraph:
    """return a coursegraph for testing purpose"""
    g = CourseGraph()
    g.add_course(course)
    g.add_edge(course, prereq)
    return g


def read_csv(filename: str) -> CourseGraph:
    """return a Coursegraph based on a csv file"""
    curr_graph = CourseGraph()
    with open(filename) as file:
        reader = csv.reader(file)
        for line in reader:
            curr_graph.add_course(line[0])
            prereq = compute_prereq(line[1])
            curr_graph.add_edge(line[0], prereq)
    return curr_graph
