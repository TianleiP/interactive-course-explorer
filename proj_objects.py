"""main part of the project, including the class Course, which represents vertex in the graph, and CourseGraph,
which represent the graph. Various methods included."""
from typing import Optional


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
    # The type of self.prereq was set originally. However, adding dictionary into set will result in TypeError:
    # unhashable type: 'dict' Although this can be solved by converting dictionary into tuple, it requires more
    # computation for types conversion, and it also has a conflict with our original usage of tuple.
    higher_courses: set
    key_words: str

    def __init__(self, name: str, key_words: Optional = '') -> None:
        self.name = name
        self.prereq = []
        self.higher_courses = set()
        self.key_words = key_words


class CourseGraph:
    """
    A graph representation of the course system.
    """
    courses: dict[str, Course]

    def __init__(self) -> None:
        self.courses = {}

    def add_course(self, name: str, keywords: Optional = '') -> None:
        """add courses to the graph"""
        if name in self.courses:
            self.courses[name].key_words = keywords
        else:
            self.courses[name] = Course(name, keywords)

    def add_edge(self, course1: str, prereq: list) -> None:
        """add edge between a course and all of its prerequisite"""
        if course1 not in self.courses:
            self.add_course(course1)
        curr_course = self.courses[course1]
        for item in prereq:
            curr_course.prereq.append(item)
        self._add_edge(course1, prereq)

    def _add_edge(self, course: str, prereq: tuple | list) -> None:
        """ private helper method of self._add_edge"""
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
        if not curr_course.prereq:
            return (cost, [])
        else:
            min_courses = self.compute_list(curr_course.prereq)
            cost += min_courses[0]
            return (cost, min_courses[1])

    def compute_list(self, prereq: list) -> tuple[float, list[str]]:
        """ helper method of self.compute_cost, input a list and return a tuple that first element is the opportunity
        cost of the item with the least possible opportunity cost(can be a single course as a dictionary or a
        combination of courses like a tuple) in the list, and the second element is a list of all of the prerequisite
        of this item that compose the opportunity cost"""
        if not prereq:
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
                    cost += new_value[0]
                compare_list.append((cost, lst))
            mincost = compare_list[0][0]
            minlst = compare_list[0][1]
            for item in compare_list:
                if item[0] < mincost:
                    mincost = item[0]
                    minlst = item[1]
            return (mincost, minlst)

    def compute_tuple(self, prereq: tuple) -> tuple[float, list[str]]:
        """helper method of self.compute_cost, input a tuple and return a tuple that first element is the total
        opportunity cost of the items in the input tuple, and second item is a list of all prerequisite of the items
        in this tuple that compose the opportunity cost."""

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

    def course_with_keywords(self, keywords: str) -> list:
        """return all courses in the graph with the input keywords."""
        lst = []
        for course in self.courses:
            if keywords in self.courses[course].key_words:
                lst.append(course)
        return lst

    def find_all_prereq(self, course: str) -> list:
        """return a list of the all prerequisite, (including the prerequisite of the prerequisite, etc.)
        from a specific course."""
        lst = []
        curr_course = self.courses[course]
        for pre in curr_course.prereq:
            if isinstance(pre, dict):
                for key in pre:
                    lst.append(key)
                    lst.extend(self.find_all_prereq(key))
            else:
                lst.extend(self.find_all_prereq_collection(pre))
        return lst

    def find_all_prereq_collection(self, prerequisite: list | tuple) -> list:
        """ helper method of self.find_all_prereq. input a collection ot courses as a list or tuple, return all
        possible prerequisite(including prerequisite of prerequisite courses, etc., of the courses in this
        collection."""
        if len(prerequisite) < 1:
            return []
        else:
            lst1 = []
            for item in prerequisite:
                if isinstance(item, dict):
                    lst1.append([key for key in item][0])
                    lst1.extend(self.find_all_prereq([key for key in item][0]))
                else:
                    lst1.extend(self.find_all_prereq_collection(item))
            return lst1

    def find_higher_courses(self, courses: list) -> list:
        """input a list of courses the user took, and return the possible courses he/she can take in the future"""
        lst = []
        for course in courses:
            curr = self.courses[course]
            if curr.higher_courses:
                for higher in curr.higher_courses:
                    lst.append(higher)
        return lst


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'proj_objects'],
        'allowed-io': ['read_csv_with_graph', 'read_csv', 'extract_columns'],
        'disable': ['E9969', 'R1702', 'R1701', 'R0912', 'R1721']
    })
