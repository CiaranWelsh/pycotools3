import pdoc
import os
os.chdir('D:\MPhil\Python\My_Python_Modules\Modelling_Tools\PyCoTools')
pyd= pdoc.html('pydentify2')
cp= pdoc.html('pycopi')
pea= pdoc.html('PEAnalysis')

with open('pydentify2.html','w') as f:
    f.write(pyd)
#
with open('pycpoi.html','w') as f:
    f.write(cp)

with open('PEAnalysis.html','w') as f:
    f.write(pea)






