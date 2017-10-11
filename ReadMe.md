# PyCoTools

Package was developed by Ciaran Welsh (c.welsh2@newcastle.ac.uk) at Newcastle University, UK. 


## Installation 
Use:
    `pip install PyCoTools` 
        
## Version 
        
This package was developed on Python 2.7 and Copasi version 19. This is a beta version of PyCoTools that is being actively developed. If you happen to find any bugs please feel free to post a github issue.

## jupyter notebook tutorial
The tutorials are being actively developed. They are available under the [tutorials] (https://github.com/CiaranWelsh/PyCoTools/tree/CopasiVersion19/PyCoTools/PyCoToolsTutorial)


# Modules

## tasks

The `tasks` module is a set of python classes for interfacing with copasi via python. 


    Features include:
        - `Reports`               - Automate the setting up of specific and commonly used reports
        
        - `ParameterEstimation`   - Automate the setting up of a parameter estimation in copasi. 
                                
                                  - Run a parameter estiamtion through copasi Via python and visualize 
                                  the results
        
        - `ExperimentMapper`      - Automate the process of mapping model species to experimental data. 
                                    Used by ParameterEstimation class
        
        - `TimeCourse`            - Simulate a time course using Copasi. Parse this data into python 
                                    and plot it optionally. 
        
        - `Scan`                  - Automate the process of setting up a parameter scan. All three 
                                    scan, repeat and random number generation) are supported. 
        
        - `Run`                   - Submit copasi file to CopasiSE. Unticks all 'executable boxes' then ticks 
                                    the executable box of interest. 
                                  
        - `ProfileLikelihood`     - Setup and run profile likleihood for a model around current parameters
                                
                                  - Optionally take parameters from a file (copasi output file for example) 
                                    and perform profile likelihood around these parameters
                                
                                  - Optionally take multiple sets of parameters from parameter estimation                                        output file and perform profile likelihoods around each of them. 
                                
                                  - Optionally run on a cluster (sun grid engine is implemented but modular 
                                    nature of the code means this bit can be replaced by code for any job
## `model`  
        
        - Model                   - Class for parsing Copasi models into python, adding, removing or changing                                     model quantities
        
        - Translator              - Translates strings into copasi style reactions
        
        - KeyGenerator            - Generate new keys on the fly for model components
        
        - InsertParameters        - Take parameters from file, folder of files, pandas.DataFrame or dict and                                     insert into model. 
        
        The following classes are for storing information about a model component:
              - Metabolite  
        
              - Substrate
              
              - Product
              
              - Modifier
              
              - Reaction
              
              - Function
              
              - ParameterDescription
              
              - LocalParameter
              
              - Expression
              
              - Compartment
              
              - GlobalQuantity
              
              - ParameterDescription
              
                                  
# viz 

The `viz` module provides a number of convenient classes for visualizing and analysing parameter estimation data or results from other copasi or pycotools tasks. 
    
    Features Include:
        
        - `Parse`                - Parse data into python. Accepts instances of other pycotools classes or
                                   a full file path to a folder of parameter estimation files. 
        
        - `PlotTimeCourse`       - Plot a time course that was simulated using `tasks.TimeCourse`
        
        - `PlotTimeCourseEnsemble` - Plot time courses using multiple parameter sets
        
        - `PlotParameterEstimation` - Plot experimental vs simulated data after parameter estimation
        
        - `Histograms`         - Plot histogram for each parameter in your estiation file
        
        - `Scatters`          - Plot scatter graphs of chosen components. 
        
        - `Boxplots`          - visualize variance with box plots
        
        - `RssVsIteration`    - evaluate optimization performance with plot of (ordered) 
                                        likelihood Vs iteration. The flatter the graph the better. 
        
        - `Pca`               - Principle component analysis on PE data

      	- `LinearRegression`  - Lasso regression on PE data 
      	
      	- PlotProfileLikelihood - plot results from `tasks.ProfileLikelihood`
 