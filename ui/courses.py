### CS122, Winter 2021: Course search engine: search
###
### Jake Nicoll

from math import radians, cos, sin, asin, sqrt
import sqlite3
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')

def find_courses(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day a list with variable number of elements
           -> ["'MWF'", "'TR'", etc.]
      - time_start an integer in the range 0-2359
      - time_end an integer in the range 0-2359
      - walking_time an integer
      - enroll_lower an integer
      - enroll_upper an integer
      - building a string
      - terms a string: "quantum plato"]

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''

    query, args = build_sql_query_args(args_from_ui)
    connection = sqlite3.connect(DATABASE_FILENAME)
    connection.create_function("time_between", 4, compute_time_between)
    cursor = connection.cursor()
    info = cursor.execute(query, args)
    info_list = info.fetchall()
    header = get_header(info)
    if info_list:
        return (header, info_list)
    # Return tuple of two empty lists of no courses meet the criteria
    return ([], [])


########### auxiliary functions #################
def build_where_string_args(args_from_ui):
    '''
    Builds the where component of the sql query to be used in find_courses,
    and also the list of arguments to be passed into the sql query

    Inputs:
        args_from_ui

    Returns: tuple of lists:
        first element is the where component of the sql query,
        and the second is the list of arguments for the sql query
    '''

    where_string = []
    args = []
    # dictionary for associating arguments in args_from_ui with the required
    # component of the associated sql query
    dic = {'dept': ['courses.dept = ?'],
            'day': ['meeting_patterns.day = ?'],
           'time_start': ['meeting_patterns.time_start >= ?'],
           'time_end': ['meeting_patterns.time_end <= ?'],
           'enroll_lower': ['sections.enrollment >= ?'],
           'enroll_upper': ['sections.enrollment <= ?'],
           'walking_time': ['walking_time <= ?'],
           'building': ['b.building_code = ?'],
           'terms': [('courses.course_id IN (SELECT' +
                   ' course_id FROM catalog_index' +
                   ' WHERE catalog_index.word = ?)')],}
    for arg, value in args_from_ui.items():
        if arg == 'day':
            day_lst = []
            for one_day in value:
                day_lst += dic['day']
                args += [one_day]
            day_string = ' OR '.join(day_lst)
            where_string += ['(' + day_string + ')']
        elif arg == 'terms':
            term_list = value.split()
            for one_term in term_list:
                where_string += dic['terms']
                args += [one_term]
        else:
            where_string += dic[arg]
            args += [value]
    return where_string, args


def build_join_on_string(args_from_ui):
    '''
    Builds the join and on components of the sql query
    to be used in find_courses

    Inputs:
        args_from_ui

    Returns: dictionary (dic) with 'join' and 'on' as keys
        and their associated components of the sql query as values
    '''

    join_string = []
    on_string = []
    sql_dic = {}
    terms = args_from_ui.get('terms')
    day = args_from_ui.get('day')
    time_start = args_from_ui.get('time_start')
    time_end = args_from_ui.get('time_end')
    walking_time = args_from_ui.get('walking_time')
    enroll_lower = args_from_ui.get('enroll_lower')
    enroll_upper = args_from_ui.get('enroll_upper')

    if (day or time_start or time_end or walking_time
        or enroll_upper or enroll_lower):
        join_string += ['sections', 'meeting_patterns']
        on_string += ['courses.course_id = sections.course_id',
                      ('sections.meeting_pattern_id =' +
                      ' meeting_patterns.meeting_pattern_id')]
        if walking_time:
            join_string += ['gps as a', 'gps as b']
            on_string += ['sections.building_code = a.building_code']
    if terms:
        join_string += ['catalog_index']
        on_string += ['courses.course_id = catalog_index.course_id']
    sql_dic['join'] = join_string
    sql_dic['on'] = on_string
    return sql_dic


def build_sel_join_on(args_from_ui):
    '''
    Builds the join, on, and select component of the sql query
    to be used in find_courses

    Inputs:
        args_from_ui

    Returns: dictionary (dic) with 'join', 'on', and 'select' as keys
        and their associated components of the sql query as values
    '''

    terms = args_from_ui.get('terms')
    dept = args_from_ui.get('dept')
    walking_time = args_from_ui.get('walking_time')
    enroll_lower = args_from_ui.get('enroll_lower')
    enroll_upper = args_from_ui.get('enroll_upper')
    sql_dic = build_join_on_string(args_from_ui)
    on = sql_dic.get('on')
    select_string = ['courses.dept, courses.course_num']
    if on:
        select_string += ['sections.section_num', 'meeting_patterns.day',
                       'meeting_patterns.time_start',
                       'meeting_patterns.time_end']
    if walking_time:
        select_string += ['a.building_code AS building',
                          ('time_between(a.lon, a.lat, b.lon, b.lat)' +
                          ' AS walking_time')]
    if (enroll_lower or enroll_upper):
        select_string += ['sections.enrollment']
    if (terms or dept):
        select_string += ['courses.title']
    sql_dic['select'] = select_string
    return sql_dic


def build_sql_query_args(args_from_ui):
    '''
    Builds the full sql query and list of arguments
    to be used in find_courses

    Inputs:
        args_from_ui

    Returns: tuple whose first entry is the full sql query (str),
        and whose second entry is the associated arguments (list)
    '''

    sql_dic = build_sel_join_on(args_from_ui)
    where, args = build_where_string_args(args_from_ui)
    select = sql_dic.get('select')
    joins = sql_dic.get('join')
    on = sql_dic.get('on')
    sql_query = 'SELECT DISTINCT ' + ', '.join(select)
    sql_query += ' FROM courses'
    if joins:
        sql_query += ' JOIN ' + ' JOIN '.join(joins)
        sql_query += ' ON ' + ' AND '.join(on)
    if where:
        sql_query += ' WHERE ' + ' AND '.join(where)
    return sql_query, args

########### do not change this code #############

def compute_time_between(lon1, lat1, lon2, lat2):
    '''
    Converts the output of the haversine formula to walking time in minutes
    '''
    meters = haversine(lon1, lat1, lon2, lat2)

    # adjusted downwards to account for manhattan distance
    walk_speed_m_per_sec = 1.1
    mins = meters / (walk_speed_m_per_sec * 60)

    return mins


def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points
    on the earth (specified in decimal degrees)
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    m = km * 1000
    return m


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i, _ in enumerate(s):
        if s[i] == ".":
            s = s[i + 1:]
            break

    return s


########### some sample inputs #################

EXAMPLE_0 = {"time_start": 930,
             "time_end": 1500,
             "day": ["MWF"]}

EXAMPLE_1 = {"dept": "CMSC",
             "day": ["MWF", "TR"],
             "time_start": 1030,
             "time_end": 1500,
             "enroll_lower": 20,
             "terms": "computer science"}
