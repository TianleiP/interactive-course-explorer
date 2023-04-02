"""
This file includes the functions that do operations on csv files and return graph based on the csv file.
"""
import csv
from proj_main import CourseGraph, Course


def read_csv(filename: str) -> CourseGraph:
    """return a Coursegraph based on a csv file"""
    curr_graph = CourseGraph()
    with open(filename) as file:
        reader = csv.reader(file)
        for line in reader:
            curr_graph.add_course(str(line[0])[1:9], str(line[0])[12:].lower())
            print(f'add course {str(line[0])[1:9]} with keywords {str(line[0])[12:]}')
            if line[1] is not None:
                prereq = compute_prereq(str(line[1]))
                print(str(line[1]))
                print(f'get prerequisite {compute_prereq(str(line[1]))}')
            curr_graph.add_edge(str(line[0])[1:9], prereq)
    return curr_graph


def read_csv_with_graph(filename: str, curr_graph: CourseGraph) -> CourseGraph:
    """Added courses and prerequisites into a graph that already exists, using the given file."""
    with open(filename) as file:
        reader = csv.reader(file)
        for line in reader:
            curr_graph.add_course(str(line[0])[1:9], str(line[0])[12:].lower())
            print(f'add course {str(line[0])[1:9]}')
            if line[1] is not None:
                prereq = compute_prereq(str(line[1]))
                print(f'get prerequisite {compute_prereq(str(line[1]))} with keywords {str(line[0])[12:]}')
            curr_graph.add_edge(str(line[0])[1:9], prereq)
    return curr_graph


def compute_prereq(prereq_str: str):
    """
    Compute the prerequisites of a course given a string representation.

    >>> compute_prereq("(60% or higher in CSC148H1, 60% or higher in CSC165H1)/ (60% or higher in CSC111H1)")
    [({'CSC148H1': 60}, {'CSC165H1': 60}), {'CSC111H1': 60}]
    >>> compute_prereq('(60% or higher in CSC148H1, 60% or higher in (CSC165H1/CSC240H1)/ 60% or higher in CSC111H1')
    [({'CSC148H1': 60}, [{'CSC240H1': 60}, {'CSC165H1': 60}]), {'CSC111H1': 60}]
    >>> compute_prereq('CSC436H1/ 75% or higher in CSC336H1,CSC209H1')
    [{'CSC436H1': 50}, ({'CSC336H1': 75}, {'CSC209H1': 50})]

    preconditions:
    - prerequisite should be in the right format that contains only the exact courses and the minimum grade requirement
    of the courses(if any).
    """
    if len(prereq_str) < 5:
        return []
    prereqs = []
    prereq_options = prereq_str.split('/ ')
    for option in prereq_options:
        course_reqs = []
        for req in option.split(','):
            if '(' in req:
                req = req.replace("(", "")
            if ')' in req:
                req = req.replace(")", "")
            req = req.strip()
            if '/' not in req:
                if '%' in req:
                    parts = req.split(' or higher in ')
                    course_code = parts[-1]
                    required_grade = int(parts[0].replace('%', ''))
                    course_reqs.append({course_code: required_grade})
                else:
                    course_reqs.append({req: 50})
            else:
                req_option = req.split('/')
                lst_option = []
                parts = req_option[0].split(' or higher in ')
                required_grade = int(parts[0].replace('%', ''))
                req_option.pop(0)
                req_option.append(parts[-1])
                for r in req_option:
                    lst_option.append({r: required_grade})
                course_reqs.append(tuple(lst_option))
        if len(course_reqs) > 1:
            course_reqs = tuple(course_reqs)
        else:
            while not (isinstance(course_reqs, dict) or isinstance(course_reqs, tuple)):
                course_reqs = course_reqs.pop()
        prereqs.append(course_reqs)
    return prereqs


def extract_columns(csv_file_path, new_csv_file_path) -> None:
    """extract the first 2 columns of the csv file"""
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        extracted_data = []
        for row in csv_reader:
            extracted_row = row[:2]
            extracted_data.append(extracted_row)
    with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as new_csv_file:
        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerows(extracted_data)
