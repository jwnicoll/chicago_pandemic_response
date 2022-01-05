#1
#1-1
#SELECT title FROM courses WHERE dept = 'CMSC';

sql1 = 'SELECT title FROM courses WHERE dept = ?;'

#1-2
#SELECT c.dept, c.course_num, s.section_num 
#FROM sections AS s JOIN courses as c ON s.course_id = c.course_id 
#WHERE s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start = 1030 AND day = 'MWF'));

sql2 = ('SELECT c.dept, c.course_num, s.section_num ' + 
'FROM sections AS s JOIN courses as c ON s.course_id = c.course_id ' +
'WHERE s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start = ? AND day = ?));')

#1-3
#SELECT c.dept, c.course_num FROM sections AS s JOIN courses as c ON s.course_id = c.course_id 
#WHERE s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start > 1030 AND time_end < 1500 AND day = 'MWF'));

sql3 = ('SELECT c.dept, c.course_num FROM sections AS s JOIN courses as c ON s.course_id = c.course_id ' +
'WHERE s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start > ? AND time_end < ? AND day = ?));')

#1-4
#SELECT DISTINCT c.dept, c.course_num, c.title FROM sections 
#AS s JOIN courses as c JOIN catalog_index AS c_i ON s.course_id = c.course_id = c_i.course_id 
#WHERE (s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start = 930)) 
#AND c.course_id IN (SELECT l.course_id FROM catalog_index AS l JOIN catalog_index AS r ON l.course_id = r.course_id WHERE (l.word = 'programming' AND r.word = 'abstract')));

sql4 = ('SELECT DISTINCT c.dept, c.course_num, c.title FROM sections ' +
'AS s JOIN courses as c JOIN catalog_index AS c_i ON s.course_id = c.course_id = c_i.course_id ' +
'WHERE (s.meeting_pattern_id = (SELECT meeting_pattern_id FROM meeting_patterns WHERE (time_start = ?)) ' +
'AND c.course_id IN (SELECT l.course_id FROM catalog_index AS l JOIN catalog_index AS r ON l.course_id = r.course_id WHERE (l.word = ? AND r.word = ?)));')

#2
import sqlite3
connection = sqlite3.connect('course-info.db')
cursor = connection.cursor()
#2-1
cursor.execute(sql1,('CMSC',))
#2-2
cursor.execute(sql2,(1030, 'MWF'))
#2-3
cursor.execute(sql3, (1030, 1500, 'MWF'))
#2-4
cursor.execute(sql4, (930, 'programming', 'abstract'))c