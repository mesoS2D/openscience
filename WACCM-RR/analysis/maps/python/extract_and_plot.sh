#!/bin/bash

# Path to the directory containing the data files
path=/path/to/data

# List of data files to process, separated by commas
file_list=file1.nc,file2.nc

# Longitude range representation in the dataset 
# Options: "O_to_360" or "n180_to_p180"
lon_range_type=n180_to_p180

# Variables to extract from the dataset, separated by commas
var_list_selection=T,OMEGA,lat,lon

# Variables to plot from the selection (subset of var_list_selection)
var_list_plot=w

# List of pressure level indices to extract, separated by commas
# These refer to specific vertical levels in the dataset
ilev_list_selection=3,15,43,103

# Indices of selected pressure levels to plot, referencing ilev_list_selection
ilev_list_plot=0,1,2,3

# List of time indices to extract, representing time steps in the dataset
itime_list_selection=0,1,2,3,4,5,6,7,8,9

# Indices of selected time steps to plot, referencing itime_list_selection
# Must be passed in as a list or array, python syntax is applicable
itime_list_plot=0

# Latitude of the center point for map projection
center_lat=70

# Longitude of the center point for map projection
center_lon=20

# Whether to apply regridding (True = perform regridding, False = use raw data)
regridding=True

# Lower and upper bounds for the regridding region in the x-direction (longitude)
rxL=-10
rxU=50

# Lower and upper bounds for the regridding region in the y-direction (latitude)
ryL=50
ryU=80

# Lower and upper bounds for the plotting region in the x-direction (longitude)
xlimL=-10
xlimU=50

# Lower and upper bounds for the plotting region in the y-direction (latitude)
ylimL=45
ylimU=80

# Whether to automatically determine the variable range for plotting
auto_vrange=True

# Whether to allow manual user-defined variable range
user_vrange=False

# Whether to use a preset variable range from a predefined source (e.g., a paper)
preset_vrange=False

# Lower and upper bounds for user-defined variable range (only used if user_vrange=True)
vrangeL=200
vrangeU=400

# Parallel settings
# Run in parallel
parallel=True
n_workers=3 # dask workers
threads_per_worker=2 
memory_limit="5GiB" # memory per worker


# Pass variables as command-line arguments
python extract_maps.py \
    -path "$path" \
    -file_list "$file_list" \
    -lon_range_type "$lon_range_type" \
    -var_list_selection "$var_list_selection" \
    -var_list_plot "$var_list_plot" \
    -ilev_list_selection "$ilev_list_selection" \
    -ilev_list_plot "$ilev_list_plot" \
    -itime_list_selection "$itime_list_selection" \
    -itime_list_plot "$itime_list_plot" \
    -center_lat "$center_lat" \
    -center_lon "$center_lon" \
    -regridding "$regridding" \
    -rxL "$rxL" \
    -rxU "$rxU" \
    -ryL "$ryL" \
    -ryU "$ryU" \
    -xlimL "$xlimL" \
    -xlimU "$xlimU" \
    -ylimL "$ylimL" \
    -ylimU "$ylimU" \
    -auto_vrange "$auto_vrange" \
    -user_vrange "$user_vrange" \
    -preset_vrange "$preset_vrange" \
    -vrangeL "$vrangeL" \
    -vrangeU "$vrangeU" \
    -parallel "$parallel" \
    -n_workers "$n_workers" \
    -threads_per_worker "$threads_per_worker" \
    -memory_limit "$memory_limit"
