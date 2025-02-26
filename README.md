## WACCM-RR
WACCM-RR is the regionally-refined (RR) version of the Whole Atmosphere Community Climate Model (WACCM).

## Relevant papers
*Paper details will go here*

## File directory
```
WACCM-RR  
|    README.md  
├───analysis  
|    ├───monthly_domain_average  
|    ├───vertical_flx_wtrans  
|    └───maps  
|  
├───data  
|    ├───processed_data  
|    |   ├───monthly_domain_average  
|    |   ├───vertical_flx_wtrans  
|    |   |   ├────flux  
|    |   |   |   ├───daily  
|    |   |   |   └───monthly  
|    |   |   ├────time_domain_means  
|    |   |   |   ├───daily  
|    |   |   |   └───monthly  
|    |   |   └───wtrans  
|    |   |       ├───daily  
|    |   |       └───monthly
|    |   └───maps  
|    ├───raw_data
|    |   ├───RR
|    |   └───Non-RR
|    └───SOR_LIDAR  
|  
├───docs  
|  
├───envs  
|    environment.yml  
|    readme.txt  
|  
├───helpers  
|  
├───notebooks  
|  
└───plots
```  

### analysis
This folder contains jupyter notebooks to process and analyse WACCM (RR and non-RR) data analysis. File paths for data and output of plots point to the **data** and **plots** directories respectively. Functions called within the notebooks are in the **helpers** folder.
#### monthly_domain_average
These plots show the variation in monthly average properties (e.g. temperature, concentration of species) across the RR area compared to the same area in Non-RR WACCM and can also plot the differences between the two.
#### vertical_flx_wtrans
A workflow to calculate daily and monthly averages of different variables, fluxes, and vertical transport velocity (wtrans) in WACCM RR and Non-RR.
#### maps
2D-lat/lon slices through the atmosphere.

### data
This folder is where the analysis notebooks look to find the raw model output and to write the processed data to. Data is not included in this repo, but the structure remains.

### docs
Useful documentation that defines the different files, variable names etc.

### envs
Instructions to install a conda environment with all of the required dependencies for analysis of the WACCM model output.

### helpers
Functions called by notebooks to analyse and plot data.

### notebooks
Short, simple example notebooks for data analysis.

### plots
The folder where figures produced by analysis noteboks are saved. Figures are not included in this repo, but the folder remains.
