import site
site.addsitedir('/home/b3053674/Documents/pycotools')

from  pycotools import *



cps_file1 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012.cps'
cps_file2 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_2.cps'
cps_file3 = r'/home/b3053674/Documents/pycotools/ZiModel/zi2012_3.cps'

zi = model.Model(cps_file2)

TC=tasks.TimeCourse(
    zi,
    report_name='kholodenko_timecourse_report.txt',
    end=1000,
    intervals=50,
    step_size=20,
    metabolites=['Smad3c','Smad3n'],
    global_quantities = [],
    save=True
)

# print tasks.Scan(zi, scan_type='scan',
#            variable='Smad3c', subtask='time_course')

# x = model.Metabolite(zi, 'x')
#
# y = x
#
# print y == x
#
#
# r = model.Reaction(zi, 'r5', 'A -> B', 'k*A')
#
#
# #
# # zi.add('reaction', r)
#
# zi.open(cps_file2)
#
#
#
















































