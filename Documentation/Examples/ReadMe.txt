Examples were written by Ciaran Welsh.  
Email c.welh2@newcastle.ac.uk

Firstly download models from biomodels using DownloadCuratedModelsFromBioModels.py. This relies on bioservices module
ConvertToCps.py uses coapsiSE to convert xml to cps
MedianNumberOfParameter.py uses the coapsiAPI.GetModelQuantites class to probe the downloaded models.
RunTimeCourseForEachModel.py runs a generic time course on each model. Some models fail for various reasons but these errors are caught
AddNoiseToTimeCourseData.py will add a specified percentage of noise to your time course data to try and make fitting more interesting
PrunePEDataHeaders.py removes the copasi references from header row in data
RunParameterEstiamtionForEachModel.py will run a generic parameter estimation using the simuated tiem course data with generic optimization parameters and estimating all model parameters
RunProfileLikelihoodOnEachModel.py uses the daat from the previous scripts to run a profile likleihood. 

Note: The profile likleihood plotting section will be provided asap. It is however simple to write yourself. Just use the Pydentify2.Plot class. 

These scripts have been run from a windows machine and a SGE based cluster. 

Also Note: More work needs to go into these scripts to ensure compatibility with all computers. At present 
there they are tailored to my own machine but can be tailored to your own by changing various file paths int the scripts. 



