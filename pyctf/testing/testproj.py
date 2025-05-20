from project import projectHD
from numpy import array
h = array([10,11,12],'d')
D = []
d = array([range(5), range(2, 7), range(5)], 'd')
D.append(d)
d = array([range(1, 6), range(3, 8), range(5)], 'd')
D.append(d)
r = projectHD(h, D)
