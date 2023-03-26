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
    prereq: set[tuple / dict]
    higher_courses: set

    def __init__(self, name: str):
        self.name = name
        self.prereq = set()
        self.higher_courses = set()


def read_csv(filename: str) -> Coursegraph:
    """return a Coursegraph based on a csv file"""
    curr_graph = CourseGraph()
    with open(filename) as file:
        reader = csv.reader(file)
        for line in reader:
            curr_graph.add_course(line[0])
            prereq = compute_prereq(line[1])
            curr_graph.add_edge(line[0], prereq)
    return curr_graph


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

    def add_edge(self, course1: str, prereq: set[tuple / dict]) -> None:
        """add edge between a course and all of its prerequisite"""
        curr_course = self.courses[course1]
        curr_course.prereq.add(prereq)
        self._add_edge(course1, prereq)

    def _add_edge(self, course: str, prereq: any) -> None:
        for item in prereq:
            if isinstance(item, dict):
                for coursename in item:
                    curr_course = self.courses[coursename]
                    curr_course.higher_courses.add(course)
            else:
                self._add_edge(course, item)
