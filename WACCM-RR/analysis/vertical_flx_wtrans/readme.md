# Vertical flux and transport calculations

Calculations and plotting of mean vertical transport fluxes and transport velocities calculated for temperature and various constituents.  

All calculations are performed in derive_flx_wtrans.ipynb - the notebook is split into sections by headings for readability. Rough plots can be produced to test the data has been calculated correctly.  
Plotting is performed by plot_flx_wtrans.ipynb - **to be added**  
The calculation notebook is designed to be worked through from top to bottom and will use the previous filenames where data was saved to read in new data. However, if necessary, sections can be used alone, but filenames will need to be provided.  
A simple but uncommented example of flux calculations for a single day can be found in ```notebooks/flux.ipynb```.

Data is saved in ```WACCM-RR/data/processed_data/vertical_flx_wtrans/``` in subfolders for mean values (time_domain_means), fluxes (flux) and transport velocities (wtrans), each of which is further split into daily and monthly mean files.
  
  
## derive_flx_wtrans.ipynb

Workflow for derive_flx_wtrans.ipynb is as follows:

### Functions
- **p2gph** (imported from ```helpers/P_to_GPH_ncol```) calculates geopotential height from pressure
- **derive_rho** calculates atmospheric mass density (kg m<sup>-3</sup>)
- **derive_n** calculates atmospheric number density (particles cm<sup>-3</sup>)
- **derive_w** calculates vertical velocity in m s<sup>-1</sup> from omega in Pa s<sup>-1</sup>
- **calculate_daily_wtrans** calculates the daily mean w in cm s<sup>-1</sup>
- **get_daily_flux** calculates mean daily flux across the domain given
- **calculate_mean** calculates the mean of givenn variables across the domain given
- **parse_days** converts the range of days given to python indexing to select the correct files
- **name_file** combines variable names in a given order when creating a filename to prevent accidental duplication of files

### Calculating variable means

#### q - compute daily mean (dm)
These two cells calculate the daily means of variables 'q' (e.g. temperature, O mixing ratio etc.)  

1. Enter inputs and controls
    - provide the path to the raw data and the output data path
    - provide the year (string), months (list of strings) and days to use (list of lists, one for each month)
    - list the variables to be used, which vertical levels (by index) to use, and the area (Continental US ("conus") and Starfire optical range ("sor") are preset, others can be provided as custom settings
    - set whether to save daily mean files, automatically set filenames, and print a list of the files being used for the calculations (for checking).
    - If not using automatic filenaming and preset (conus/sor) areas, provide the RR and Non-RR filenames and latitude and longitude range to use.
2. The code reads in the lat and long range for presets if needed, sets the variables to use, determines the RR and non-RR paths to the input data, sets the output filenames and checks there is a list of days for each month being used.
3. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
4. For each day, the h0 file is read in and the specified lat-lon domain isolated.
    - h0 files are daily files containing 24 instantaneous samples every hour.
5. Means of each of the variables (in mixing ratio and number density for species) are calculated and daily mean files saved if save_individual_days == True.
    - Non-RR files take ~30s per day to process
    - RR files take ~2 min per day to process
  
#### q - compute monthly mean (mm)
These two cells calculate the monthly means of variables 'q' (e.g. temperature, O mixing ratio etc.) from the daily mean files. 

6. Enter inputs and controls
    - provide the path to the daily mean data and the output data path
    - provide the year (string) and months (list of strings). All days available for each month will be used.
    - set whether to use previous daily mean filename, or enter a custom dm filename to look for if you did not just calculate the daily mean files.
    - Specify whether to print a list of the files being used for the calculations (for checking).
7.  The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
8.  For the RR and Non-RR data, the daily mean files are read in and concatenated into a single data set. The time average of the data is calculated and written to the new monthly mean file.

#### q - interp to z
These two cells calculate the geopotential height, z of the data and add it to the files as a **variable**, not a co-ordinate. This can be performed for either daily or monthly files. Flux and wtrans z interpolation required z on the **monthly mean q files**.

9. Enter inputs and controls
    - Specify monthly or daily files and provide the path to the time domain means (monthly/daily will be appended automatically)
    - Specify the year (string) and months (list of strings).
    - set whether to use previous mean filenames, or enter a custom filename to look for if you did not just calculate the daily and monthly mean files.
    - set whether to print the list of files used and whether to display the dataset before and after the calculation (for checking)
    - set whether to automattically generate a filename (add z to variable list) or provide a custom name if not
10. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
11. Datasets are read in and concatenated on time if necessary.
12. z is calculated using p2gph and the dataset with z included as a variable is saved out.


### Calculating fluxes

#### flx - compute daily mean (dm)
1. Enter inputs and controls
    - provide the path to the raw data and the output data path
    - provide the year (string), months (list of strings) and days to use (list of lists, one for each month)
    - list the variables to be used, which vertical levels (by index) to use, and the area (Continental US ("conus") and Starfire optical range ("sor") are preset, others can be provided as custom settings
    - set whether to save daily mean files, automatically set filenames, and print a list of the files being used for the calculations (for checking).
    - If not using automatic filenaming and preset (conus/sor) areas, provide the RR and Non-RR filenames and latitude and longitude range to use.
2. The code reads in the lat and long range for presets if needed, sets the variables to use, determines the RR and non-RR paths to the input data, sets the output filenames and checks there is a list of days for each month being used.
3. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
4. For each day, the h0 file is read in and the specified lat-lon domain isolated.
    - h0 files are daily files containing 24 instantaneous samples every hour.
5. The fluxes are calculated by get_daily_flux. The calcualtion is as follows:
     1. Convert data to relevant units.
         - OMEGA to vertical velocity w - from Pa s<sup>-1</sup> to m ss<sup>-1</sup> 
         - Mixing ratio to concentration - from mol/mol to cm<sup>-3</sup>
     2. For relevant fields, subtract 24 hour mean from data.
         - This produces a dataset of perturbations. 
     3. Multiply constituent perturbations by vertical velocity perturbations.
         - This produces a dataset of fluxes = w'q', where q is quantity of interest.
     4. Take average over time.
         - This produces a dataset with a single time sample consisting of the daily mean of w'q'. I.e., daily fluxes for all columns within the region of interest.
     5. Weigh dataset by cell area, and average over space.
         - This produces a dataset with a single daily flux averaged over time (day) and space (region of interest)
6. Daily mean files are saved if save_individual_days == True.

#### flx - compute monthly mean (mm)
These two cells calculate the monthly means of fluxes from the daily mean files. 

7. Enter inputs and controls
    - provide the path to the daily mean data and the output data path
    - provide the year (string) and months (list of strings). All days available for each month will be used.
    - set whether to use previous daily mean flux filename, or enter a custom dm filename to look for if you did not just calculate the daily mean flux files.
    - Specify whether to print a list of the files being used for the calculations (for checking).
8.  The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
9.  For the RR and Non-RR data, the daily flux mean files are read in and concatenated into a single data set. The time average and standard deviation of the daily fluxes is calculated and written to the new monthly mean flux file.

#### flx - interp to z
These two cells read the altitude z from the **monthly mean q** data and swap to flx vs x, not pressure ("lev").

10. Enter inputs and controls
    - Provide the path to the time domain monthly means on z and the monthly mean flux files.
    - Specify the year (string) and months (list of strings).
    - set whether to use previous filenames for z and fluxes, or enter custom filenames to look for if you did not just calculate the monthly mean q on z and monthly mean fluxes. Specify whether to automatically name the output file and provide an custom name if not.
    - set whether to print the list of files used and whether to display the dataset before and after the calculation (for checking). Set whether to plot examples and which variables to plot if so. Variables are in the form ```'T_flux'``` or ```'O_n_flux'``` for gas phase species. Gas fluxes are only in number density, not mixing ratio. Specify whether to save the monthly mean z files.
10. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True. If no z files are found, a warning will be printed.
11. Datasets are read in. The same pressure levels are taken from the flux and z files and z copied into the flux files as a variable. z and lev are swapped to produce a second dataset on z, not pressure.
12. If plot_examples == True, the Non-RR and RR fluxes will be plotted for each variable (rows) on pressure (left column) and (approximate) altitude (right column)
13. Data on z is saved out if save_out == True

### Calculating transport velocities 

#### wtrans - compute daily mean (dm)
These two cells calculate the daily transport velocity for each variable of interest from the flux and q  
i.e., for quantity $q$ of interest, calculate $\overline{w}_{q}$ = $\overline{w'q'}/\overline{q}$  

1. Enter inputs and controls
    - provide the path to the daily mean q and flux data and the output data path
    - provide the year (string) and months (list of strings).
    - set whether to use previous filenames for flux and q mean files and provide custom filenames if not. Specify additional info to include in filename (RR/Non-RR, wtrans and date are added automatically). INcluding an indication of the region (e.g. cm or sor) is recommended.
    - set whether to save daily mean files and print a list of the files being used for the calculations (for checking).
3. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True. The code checks that the same number of q and flux files have been found and will print a warning if not.
4. Calculate_daily_wtrans reads in the q and flux files.
     1. Read in daily mean flux and q for each variable.
     2. Calculate wtrans = flux/q and convert units for T
         - heat flux is in K m s<sup>-1</sup>, multiply by 100 to convert to K cm s<sup>-1</sup>
     4. The time co-ordinate of the data is set as the date
         - Dates are extracted from q filenames
     5. If save_outfiles = True, daily mean files are saved.

#### wtrans - compute monthly mean (mm)
These two cells calculate the monthly means of transport velocities from the daily mean files. 

6. Enter inputs and controls
    - provide the path to the daily mean data and the output data path
    - provide the year (string) and months (list of strings). All days available for each month will be used.
    - set whether to use previous daily mean wtrans filename, or enter a custom filename to look for if you did not just calculate the daily mean wtrans files.
    - Provide a list of variables to calculate monthly mean wtrans for.
    - Specify whether to print a list of the files being used for the calculations (for checking), save monthly mean files, print parts of the dataset during the calculations and plot examples. If plot_examples == True, specify which variable to plot examples for.
7.  The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True
8.  For the RR and Non-RR data, the daily wtrans mean files are read in and concatenated into a single data set.
9.  If plot_examples == True, examples of the monthly mean values will be plotted for the variables in plot_for.
10. The time average and standard deciation are calculated.If plot_examples == True, the wtrans with std of each variable will be plotted for checking.
12. The time average and standard deviation datasets are printed if inspect_ds == True and are written to the new monthly mean wtrans files if save_outfiles == True

#### wtrans - interp to z
These two cells read the altitude z from the **monthly mean q** data and swap to flx vs x, not pressure ("lev").

11. Enter inputs and controls
    - Provide the path to the time domain monthly means on z and the monthly mean wtrans files.
    - Specify the year (string) and months (list of strings).
    - set whether to use previous filenames for z and wtrans, or enter custom filenames to look for if you did not just calculate the monthly mean q on z and monthly mean wtrans.
    - set whether to print the list of files used and whether to display the dataset before and after the calculation (for checking). Set whether to plot examples and which variables to plot if so. Variables are in the form ```'T_wtrans'``` or ```'O_n_wtrans'``` for gas phase species. Gas fluxes are only in number density, not mixing ratio. Specify whether to save the monthly mean z files.
10. The files are found and the filenames saved in lists. These will be printed for checking if print_file_list == True. If no z files are found, a warning will be printed.
11. Datasets are read in. The same pressure levels are taken from the wtrans and z files and z copied into the wtrans files as a variable. z and lev are swapped to produce a second dataset on z, not pressure.
13. If plot_examples == True, the Non-RR and RR wtrans values will be plotted for each variable (rows) on pressure (left column) and (approximate) altitude (right column)
14. Data on z is saved out if save_out == True.


# Description of data

Data found in data/processed_data/vertical_flx_wtrans/

Filename components may not be present in all names, but will be in the following order:
Components of filenames and meanings (separated by _):
- on_lev / on_z : all monthly mean files and wtrans daily mean files begin with a prefix of whether the vertical co-ordinate is pressure (on_lev) or altitude (on_z)
- nonrr / rr : all files specify Non-RR or RR output
- cm / sor : all files should specify the domain used - Continental US, CONUS mean (cm) or Starfire optical range (sor)
- flx / mean / wtrans : all files indicate whether they are fluxes (flx), q (mean) or transport velocity (wtrans)
- z : q files with z calculated will include a z at the beginning of the variable list
- w : daily mean flux files will include a w at the beginning of the variable list
- T_NO_O_CO2_CO_H2O : all q files and daily mean flux files include a list of the variables in the files. Some may be absent, but the order should remain unchanged.
- monthly_mean : monthly mean flux files have a monthly_mean tag
- fullcol : files that contain the full column (Top of atmosphere to surface) have this tag
- {yyyy}-{mm} : all files specify the year and month numerically
- -{dd}-##### : daily mean files have the day number and a 5 digit number (should be 00000) after the year and month
- .nc : all files are netcdf

Note: 
- fields contained in daily files are listed in filename
- Daily mean files of fields (not fluxes) contain both mixing ratios and number densities
- Continentral US domain averages computed over
  - [240,285] # lonL, lonU
  - [22,52] # latL, latU
- SOR averages computerd over range
  - [252,256] # lonL, lonU
  - [33,37] # latL, latU
