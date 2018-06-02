import csv
with open('course.csv') as f:
...     r = csv.reader(f,delimiter=',')
...     for row in r:
...             c = Course(code=row[0],credit=row[1])
...             db.session.add(c)

