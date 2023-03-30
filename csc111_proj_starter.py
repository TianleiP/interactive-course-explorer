
import csv
from typing import Any, Optional

class Course:
    """
    name: name of the course.
    prereq: courses required in order to take this course.
    higher_courses: the courses that include this course as prerequisite.

    For example, if the prereq of course 'whateverthatis' is '(grade >= 70 for course MAT137 and pass for MAT223),
    or grade >= 60 for MAT157', then self.prereq will looks like:[({'MAT137': 70}, {'MAT223':50}), {'MAT157':75}]. In
    this case, the prerequisite is satisfied if and only if any if the requirement for (MAT137 and MAT223) is
    satisfied, or the score for MAT157 is not lower than 60. If the prereq of the course is MAT137 or MAT157, then
    self.prereq will be like [{'MAT157':50}, {'MAT223':50}], which minimum grade requirement is set to 50 by default.
    """
    name: str
    prereq: list
    # The type of self.prereq was set originally. However, adding dictionary into set will result in TypeError: unhashable type: 'dict'
    # Although this can be solved by converting dictionary into tuple, it requires more computation for types conversion, and it also has
    # a conflict with our original usage of tuple.
    higher_courses: set

    def __init__(self, name: str):
        self.name = name
        self.prereq = []
        self.higher_courses = set()




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

    def compute_cost(self, course: str) -> tuple[float, list[str]]:
        """ compute the total opportunity cost needed in order to finish this course.
        for each course, if it's a year course, it's opportunity cost is 1 + total cost
        of its prerequisite. If it's a half year course, it's opportunity is 0.5 + total
        cost of its prerequisite.
        # the following are mostly fake courses, only for testing purpose
        >>> g = CourseGraph()
        >>> g.add_course('Mat137H1')
        >>> g.add_edge('Mat137H1', [({'MAT223H2': 70}, {'MAT157Y1':50}), {'CSC111H1':75}])
        >>> g.compute_cost('Mat137H1')
        (1.0, ['CSC111H1'])
        >>> g = CourseGraph()
        >>> g.add_course('Mat137H1')
        >>> g.add_edge('Mat137H1', [({'MAT223H2': 70}, {'MAT157Y1':50}), {'CSC111H1':75}])
        >>> g.add_edge('MAT223H2', [({'MAT256H2': 70}, {'MAT177Y1':50}), {'CSC131H1':75}])
        >>> g.add_edge('CSC111H1', [({'MAT286H2': 70}, {'MAT179Y1':50}), {'CSC141H1':75}])
        >>> g.compute_cost('Mat137H1')
        (1.5, ['CSC111H1', 'CSC141H1'])
        """
        cost = 0
        if self.is_year_course(course):
            cost += 1
        else:
            cost += 0.5
        curr_course = self.courses[course]
        if curr_course.prereq == []:
            return(cost, [])
        else:
            min_courses = self.compute_list(curr_course.prereq)
            cost += min_courses[0]
            return(cost, min_courses[1])


    def compute_list(self, prereq:list) -> tuple[float, list[str]]:

        if prereq == []:
            return (0.0, [])
        else:
            compare_list = []
            for p in prereq:
                cost = 0
                lst = []
                if isinstance(p, tuple):
                    new = self.compute_tuple(p)
                    lst.extend(new[1])
                    cost += new[0]
                else:
                    lst.append([key for key in p][0])
                    new_value = self.compute_cost([key for key in p][0])
                    lst.extend(new_value[1])
                    cost +=new_value[0]
                compare_list.append((cost, lst))
            mincost = compare_list[0][0]
            minlst = compare_list[0][1]
            for item in compare_list:
                if item[0] < mincost:
                    mincost = item[0]
                    minlst = item[1]
            return (mincost, minlst)


    def compute_tuple(self, prereq:tuple) -> tuple[float, list[str]]:

        if prereq == ():
            return (0.0, [])
        else:
            cost = 0
            lst = []
            for p in prereq:
                if isinstance(p, list):
                    new = self.compute_list(p)
                    lst.extend(new[1])
                    cost += new[0]
                else:
                    new = self.compute_cost([key for key in p][0])
                    lst.extend(new[1])
                    cost += new[0]
            return (cost, lst)



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


def compute_prereq(prereq_str):
    """
    Compute the prerequisites of a course given a string representation.
    >>> compute_prereq("(60% or higher in CSC148H1, 60% or higher in CSC165H1) / (60% or higher in CSC111H1)")
    [({'CSC148H1': 60}, {'CSC165H1': 60}), {'CSC111H1': 60}]
    """
    prereqs = []
    prereq_options = prereq_str.split(' / ')
    for option in prereq_options:
        course_reqs = []
        for req in option.split(','):
            if '(' in req:
                req = req.replace("(", "")
            if ')' in req:
                req = req.replace(")", "")
            req = req.strip()
            if '%' in req:
                parts = req.split(' or higher in ')
                course_code = parts[-1]
                required_grade = int(parts[0].replace('%', ''))
                course_reqs.append({course_code: required_grade})
            else:
                course_reqs.append({req: 50})
        if len(course_reqs) > 1:
            course_reqs = tuple(course_reqs)
        else:
            course_reqs = course_reqs.pop()
        prereqs.append(course_reqs)
    return prereqs
