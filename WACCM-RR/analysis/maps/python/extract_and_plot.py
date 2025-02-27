# import xarray as xr
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import griddata
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from matplotlib.tri import Triangulation
import argparse
# import glob 
# import time 

# TESTS
# TODO - creates a single map using serial computation
# TODO - creates a single map when using DASK submitted to cluster - 2 workers, 2 cores, 2GiB Ram
# TODO - Regrids map and saves
# TODO - Regrids map, saves, plots, saves plot
# TODO - Reads in regridded data, plots
# TODO - Reads in regridded data, plots, saves plot


def validate_list(lst): # Function to enforce specific pressure level selections (just execute this and don't worry about it). 
    """
    Raises a ValueError if the list does not meet the following criteria:
        - Contains only numbers 0, 1, 2, and 3
        - Contains no duplicate elements

        Purpose - validate pressure selection list. 
        This might be more relaxed once we want to plot other pressure levels.

    Args:
        lst: The list to validate

    Raises:
        ValueError: If the list does not meet the criteria.
    """

    if not all(x in [0, 1, 2, 3] for x in lst):
        raise ValueError("List can only contain numbers 0, 1, 2, or 3. Your code won't work.")
    if len(lst) != len(set(lst)):
        raise ValueError("List cannot contain duplicate elements. Your code won't work.")
    
def converta_omega_to_w(omega,T,pressure): # Convert Pa/s to m/s (take care with units!)

    # Calculate mass density: kg m^-3
    # Conversion constants
    R = 287.058 # J/ kg^-1 K^-1 => m^2 s^-2 K^-1
    to_Pa = 100 # convert from hPa to Pa. Pa => kg m^-1 s^-2
    rho = pressure*to_Pa/(R*T) # Units: kg m^-1 s^-2 * m^-2 s^2 K * K^-1 => kg m^-3

    g = 9.80665 # m s^-2
    w = -omega/(rho*g) # Units: kg m^-1 s^-2 * s^-1 * kg^-1 m^3 * m^-1 s^2 => m s^-1

    return w
    
if __name__ == "__main__":
    
    # Create parser, get arguments, parse
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, required=True, help='Path to the dataset directory.')
    parser.add_argument('-file_list', type=str, required=True, help='List of files to read data from.')
    parser.add_argument('-lon_range_type', type=str, required=True, help="Choice of longitude representation in dataset. Options: 'O_to_360' or '-180_to_180'.")
    parser.add_argument('-var_list_selection', type=str, required=True, help='List of variables to extract from the dataset. Must include latitude and longitude for plotting.')
    parser.add_argument('-var_list_plot', type=str, required=True, help='Subset of var_list_selection to plot. Options: Any subset from var_list_selection plus "w" (vertical velocity).')
    parser.add_argument('-ilev_list_selection', type=str, required=True, help='List of pressure level indices to extract. Example: [3,15,43,103].')
    parser.add_argument('-ilev_list_plot', type=str, required=True, help='Indices from ilev_list_selection to plot. Must be a subset of ilev_list_selection.')
    parser.add_argument('-itime_list_selection', type=str, required=True, help='List of time indices to extract from raw data.')
    parser.add_argument('-itime_list_plot', type=str, required=True, help='Indices from itime_list_selection to plot.')
    parser.add_argument('-center_lat', type=str, required=True, help='Latitude of the center of the map projection.')
    parser.add_argument('-center_lon', type=str, required=True, help='Longitude of the center of the map projection. This value depends on lon_range_type.')
    parser.add_argument('-regrid_save_plot_save', type=str, required=True, help='List of true and falses, e.g., [1,0,1,0] - regrids, plots, but doesn\'t save either')
    parser.add_argument('-rxL', type=str, required=True, help='Lower bound for regridding in the x direction.')
    parser.add_argument('-rxU', type=str, required=True, help='Upper bound for regridding in the x direction.')
    parser.add_argument('-ryL', type=str, required=True, help='Lower bound for regridding in the y direction.')
    parser.add_argument('-ryU', type=str, required=True, help='Upper bound for regridding in the y direction.')
    parser.add_argument('-xlimL', type=str, required=True, help='Lower x limit for plotting (applies regardless of regridding).')
    parser.add_argument('-xlimU', type=str, required=True, help='Upper x limit for plotting (applies regardless of regridding).')
    parser.add_argument('-ylimL', type=str, required=True, help='Lower y limit for plotting (applies regardless of regridding).')
    parser.add_argument('-ylimU', type=str, required=True, help='Upper y limit for plotting (applies regardless of regridding).')
    parser.add_argument('-auto_vrange', type=str, required=True, help='Use auto specified variable range (True/False).')
    parser.add_argument('-user_vrange', type=str, required=True, help='Use manually specified variable range (True/False).')
    parser.add_argument('-preset_vrange', type=str, required=True, help='Use a preset variable range (True/False).')
    parser.add_argument('-vrangeL', type=str, required=False, help='Lower bound for variable range, used if user_vrange=True.')
    parser.add_argument('-vrangeU', type=str, required=False, help='Upper bound for variable range, used if user_vrange=True.')
    parser.add_argument('-parallel', type=str, required=True, help='Running serial or in parallel using dask')
    parser.add_argument('-n_workers', type=str, required=False, help='Running serial or in parallel using dask')
    parser.add_argument('-threads_per_worker', type=str, required=False, help='Running serial or in parallel using dask')
    parser.add_argument('-memory_limit', type=str, required=False, help='Running serial or in parallel using dask')

    # Get parsed arguments
    args = parser.parse_args()
        
    # Assign parsed arguments to internal variables
    path = args.path  
    file_list = args.file_list.split(',') 
    lon_range_type = args.lon_range_type  # Longitude representation choice
    var_list_selection = args.var_list_selection.split(',')  # List of variables to extract
    var_list_plot = args.var_list_plot.split(',')  # Subset of var_list_selection for plotting
    ilev_list_selection = list(map(int, args.ilev_list_selection.split(',')))  # Pressure level indices
    ilev_list_plot = list(map(int, args.ilev_list_plot.split(',')))  # Indices from ilev_list_selection to plot
    itime_list_selection = list(eval(args.itime_list_selection))  # Time indices from raw data
    itime_list_plot = list(map(int, args.itime_list_plot.split(',')))  # Indices from itime_list_selection to plot
    center_lat = float(args.center_lat)  # Latitude of the map center
    center_lon = float(args.center_lon)  # Longitude of the map center
    
    regrid_save_plot_save =  list(map(int, args.regrid_save_plot_save.split(',')))   # bools for regrid, save regrid, plot, save plot, default = [1,0,1,0]
    if regrid_save_plot_save[0:2] == [0,1]:
        print("Cannot save a regrid that has not been performed, setting save regrid to False")
        regrid_save_plot_save[0:2] = [0,0]     
    if regrid_save_plot_save[2:4] == [0,1]:
        print("Cannot save a plot that has not been performed, setting save plot to False")
        regrid_save_plot_save[2:4] = [0,0]
    
    rxL = float(args.rxL)  # Lower lon bound for regridding
    rxU = float(args.rxU)  # Upper lon bound for regridding
    ryL = float(args.ryL)  # Lower lat bound for regridding
    ryU = float(args.ryU)  # Upper lat bound for regridding
    xlimL = float(args.xlimL)  # Lower lon limit for plotting
    xlimU = float(args.xlimU)  # Upper lon limit for plotting
    ylimL = float(args.ylimL)  # Lower lat limit for plotting
    ylimU = float(args.ylimU)  # Upper lat limit for plotting
    
    # Check for auto plotting bool
    if args.auto_vrange.upper() in ["TRUE",'1']:
        auto_vrange = True
    elif args.auto_vrange.upper() in ['FALSE','0']:
        auto_vrange = False
    else:
        raise ValueError('Error: parallel must be either True or False')
    
    # Check for user plotting bool
    if args.user_vrange.upper() in ["TRUE",'1']:
        user_vrange = True
    elif args.user_vrange.upper() in ['FALSE','0']:
        user_vrange = False
    else:
        raise ValueError('Error: parallel must be either True or False')
     
    # Check for preset plotting bool
    if args.preset_vrange.upper() in ["TRUE",'1']:
        preset_vrange = True
    elif args.preset_vrange.upper() in ['FALSE','0']:
        preset_vrange = False
    else:
        raise ValueError('Error: parallel must be either True or False')
    
    # Check at least one plotting bool is chosen
    if 1 not in set([auto_vrange,user_vrange,preset_vrange]):
        raise(ValueError('One of auto, user or preset vranges must be set to true!'))
    
    vrangeL = float(args.vrangeL) if args.vrangeL else None  # Lower bound for variable range (optional)
    vrangeU = float(args.vrangeU) if args.vrangeU else None  # Upper bound for variable range (optional)
    
    # Check for auto plotting bool
    if args.parallel.upper() in ["TRUE",'1']:
        parallel = True
    elif args.parallel.upper() in ['FALSE','0']:
        parallel = False
        n_workers = None
        threads_per_worker = None
        memory_limit = None
    else:
        raise ValueError('Error: parallel must be either True or False')
    
    if parallel == True: # Import dask, read in cluster parameters, spin up cluster
        from dask.distributed import Client, LocalCluster
        n_workers=int(args.n_workers)
        threads_per_worker=int(args.threads_per_worker)
        memory_limit=args.memory_limit
        cluster = LocalCluster(n_workers=n_workers,threads_per_worker=threads_per_worker,memory_limit=memory_limit)
        client = Client(cluster)
    
    print(client)
    # Print parsed arguments for debugging
    print("path", path)
    print("file_list", file_list)
    print("lon_range_type", lon_range_type)
    print("var_list_selection", var_list_selection)
    print("var_list_plot", var_list_plot)
    print("ilev_list_selection", ilev_list_selection)
    print("ilev_list_plot", ilev_list_plot)
    print("itime_list_selection", itime_list_selection)
    print("itime_list_plot", itime_list_plot)
    print("center_lat", center_lat)
    print("center_lon", center_lon)
    print("regridding", regridding)
    print("rxL", rxL)
    print("rxU", rxU)
    print("ryL", ryL)
    print("ryU", ryU)
    print("xlimL", xlimL)
    print("xlimU", xlimU)
    print("ylimL", ylimL)
    print("ylimU", ylimU)
    print("auto_vrange", auto_vrange)
    print("user_vrange", user_vrange)
    print("preset_vrange", preset_vrange)
    print("vrangeL", vrangeL)
    print("vrangeU", vrangeU)
    print("parallel", parallel)
    print("n_workers",n_workers)
    print("threads_per_worker",threads_per_worker)
    print("memory_limit",memory_limit)