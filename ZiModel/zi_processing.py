import site
site.addsitedir('/home/b3053674/Documents/pycotools')

import pycotools



cps_file = r'/home/b3053674/Documents/pycotools/ZiModel/Zi2012.cps'



zi = pycotools.model.Model(cps_file)

print zi.reactions


































