
import csv
from typing import Any, Optional

class Course:
    """
    name: name of the course.
    prereq: courses required in order to take this course.
    higher_courses: the courses that include this course as prerequisite.

    For example, if the prereq of course 'whateverthatis' is '(grade >= 70 for course MAT137 or pass for MAT157),
    and grade >= 75 for CSC111', then self.prereq will looks like:[({'MAT137': 70}, {'MAT157':50}), {'CSC111':75}]. In
    this case, the prerequisite is satisfied if and only if any if the requirement for (MAT137 and MAT157) is
    satisfied, and the score for CSC111 is not lower than 75. If the prereq of the course is MAT137 or MAT157, then
    self.prereq will be like [({'MAT157':50}, {'MAT223':50})], which minimum grade requirement is set to 50 by default.
    """
    name: str
    prereq: list
    higher_courses: set

    def __init__(self, name: str):
        self.name = name
        self.prereq = []
        self.higher_courses = set()




def compute_prereq(information: str) -> list:
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

    def add_edge(self, course1: str, prereq: list) -> None:
        """add edge between a course and all of its prerequisite"""
        if course1 not in self.courses:
            self.add_course(course1)
        curr_course = self.courses[course1]
        for item in prereq:
            curr_course.prereq.append(item)
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

    def compute_cost(self, course: Any) -> tuple[float, list[str]]:
        """ compute the total opportunity cost needed in order to finish this course.
        for each course, if it's a year course, it's opportunity cost is 1 + total cost
        of its prerequisite. If it's a half year course, it's opportunity is 0.5 + total
        cost of its prerequisite.
        >>> g = CourseGraph()
        >>> g.add_course('Mat137H1')
        >>> g.add_edge('Mat137H1', [({'MAT223H2': 70}, {'MAT157Y1':50}), {'CSC111H1':75}])
        >>> g.compute_cost('Mat137H1')
        (1.5, ['Mat137H1', 'MAT223H2', 'CSC111H1'])
        >>> g = CourseGraph()
        >>> g.add_course('Mat137H1')
        >>> g.add_edge('Mat137H1', [({'MAT223H2': 70}, {'MAT157Y1':50}), {'CSC111H1':75}])
        >>> g.add_edge('MAT223H2', [({'MAT256H2': 70}, {'MAT177Y1':50}), {'CSC131H1':75}])
        >>> g.add_edge('MAT157Y1', [({'MAT286H2': 70}, {'MAT179Y1':50}), {'CSC141H1':75}])
        >>> g.compute_cost('Mat137H1')
        (2.5, ['Mat137H1', 'MAT223H2', 'MAT256H2', 'CSC131H1', 'CSC111H1'])
        """
        if isinstance(course, str):
            curr_course = self.courses[course]
            if not curr_course.prereq:
                if self.is_year_course(course):
                    return (1.0, [course])
                else:
                    return (0.5, [course])
            else:
                cost = 0
                lst = [course]
                for item in curr_course.prereq:
                    if isinstance(item, dict):
                        for key in item:
                            cost += self.compute_cost(key)[0]
                            lst.extend(self.compute_cost(key)[1])
                    else:
                        cost += self.compute_cost(item)[0]
                        lst.extend(self.compute_cost(item)[1])
                if self.is_year_course(course):
                    cost += 1.0
                else:
                    cost += 0.5
                if len(lst) != len(set(lst)):
                    lst = list(set(lst))
                return (cost, lst)
        elif isinstance(course, list):
            if course == []:
                return (0.0, [])
            else:
                cost = 0.0
                courselst = []
                for item in course:
                    cost += self.compute_cost(item)[0]
                    courselst.extend(self.compute_cost(item)[1])
                return (cost ,courselst)
        else:
            if course == ():
                return (0, [])
            else:
                course_code = [key for key in course]
                min_cost = self.compute_cost(course_code)[0]
                for c in course:
                    if self.compute_cost(c)[0] < min_cost:
                        min_cost = self.compute_cost(c)[0]
                        course_code = [key for key in c][0]
                lst2 = []
                lst2.extend(self.compute_cost(course_code)[1])
                return (min_cost, lst2)


    def is_year_course(self, course: str) -> bool:
        """return whether a course is a year course or a half year course"""
        if course[6] == 'Y':
            return True
        else:
            return False



def create_graph(course: str, prereq: list) -> CourseGraph:
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
