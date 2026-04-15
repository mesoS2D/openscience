# Search for "user changes"

import xarray as xr
import numpy as np
import dask
from dask.distributed import Client
from dask_jobqueue import PBSCluster
import argparse
import time
import datetime
import glob

def process_data(variable, ds_month, month, client):
    print(f'processing variable month lats lons times {variable} {month} {lats} {lons} {times}')
    tic = time.time()
    
    # Calculate weights and perform weighted average
    weights = np.cos(np.deg2rad(ds_month.lat))
    ds_weighted = ds_month.weighted(weights)
    ds_mean = ds_weighted.mean(dim=('ncol','time'))
        
    # set time coordinate
    ds_mean['time'] = int(f'2010{month}')
    ds_mean = ds_mean.expand_dims('time')
    ds_mean = ds_mean.set_coords({'time':ds_mean['time']})
    
    print('ds_mean to be written to file', ds_mean)
    
    out = client.persist(ds_mean)
    out = client.compute(out)
    out = out.result()
    
    # Write to file
    out.to_netcdf(f'{path_out}{timestr}_2010{month}.nc')
    
    print(f'processing and writing to file took {time.time() - tic:.2f} seconds\n')

def main():
    
    # ------------------------------------------
    # Connect to Dask client
    # ------------------------------------------
    #For casper
    # Configure the PBSCluster with updated parameters
    #cluster = PBSCluster(
    #    account='P93300043',
    #    queue='casper',
    #    walltime='6:00:00',  # Set the walltime as needed
    #    name=f'{timestr}',
    #    cores=36,                         # Total cores for the entire job
    #    memory='150GB',                   # Memory per job (worker)
    #    processes=4,                    # Number of Dask worker processes - threads per worker calculated as cores/processes
    #    resource_spec='select=1:ncpus=36:mem=150GB',  # Adjust the resource specification as needed
    #    job_extra_directives=['-j oe',
    #                          f'-N {timestr}'],  # Updated PBS options
    #)
    #cluster.scale(1)
    #client = Client(cluster)

    #For local:
    cluster = LocalCluster()
    client = Client(cluster)
    # -------------------------------------------
    
    
    #-------------------------------------
    # Get ncol indices for geography
    #-------------------------------------
    path_map = '../util_data/'
    file_map = 'FWmaHIST_ne0CONUSne30x8_ne0CONUSne30x8_mt12_no_conus_gravity_waves_lat_lon_area.nc'
    ds_map = xr.open_dataset(path_map + file_map)[['lat','lon']]
    
    ncol_indices = np.argwhere((ds_map.lon.values > lons[0]) & # conditions
                      (ds_map.lon.values < lons[1]) &
                      (ds_map.lat.values > lats[0]) &
                      (ds_map.lat.values < lats[1])
                     ).flatten().tolist() # convert to 1D numpy array, and then to list

    print(len(ncol_indices))
    #-------------------------------------
    # Loop over months and process data
    #-------------------------------------
      
    # Loop over months
    for variable in var:
        for month in months:

            tic = time.time()
            print(f'\nProcessing month {month}')
            # Get all filenames and ignore 'subset' file
            file_pattern = f'{path_in}/*h0*2010-{month}*'
            file_list = [filename for filename in glob.iglob(file_pattern) if 'subset' not in filename]
            
            datasets=[]
            for ifile,filename in enumerate(sorted(file_list)):
                print(f'Reading file {ifile}')
                ds = xr.open_mfdataset(filename,parallel=True, chunks={'time': 48, 'lev': 55})[variable].isel(ncol=ncol_indices)
                datasets.append(ds)
            print(f'That took {time.time() - tic:.2f} seconds')
            
            # combine datasets
            tic = time.time()
            print('Combining datasets')
            combined_ds = xr.combine_nested(datasets, 'time')
            print(f'That took {time.time() - tic:.2f} seconds')        
            
            # Extract time
            if month=='02':
                days = 27
            else:
                days = 29
            if diur=='True': # Get diurnal average
                indices = np.arange(0,days*24,3)
            else: # Get specific indices for either day or night
                indices = np.array([j for i in range(days) for j in range(24 * i + times[0], 24 * i + times[1] +1)])
            ds_month = combined_ds.isel(time=indices)

            print('\nds_month', ds_month)
            print('\nds_month.time',ds_month.time)
            print('\nds_month.lat first 5',sorted(ds_month.isel(lev=0,time=0).lat.values)[:5])
            print('\nds_month.lat last 5',sorted(ds_month.isel(lev=0,time=0).lat.values)[-5:])
            # print('\nds_month.lon first 5',sorted(ds_month.isel(lev=0,time=0).lon.values)[:5])
            # print('\nds_month.lon last 5',sorted(ds_month.isel(lev=0,time=0).lon.values)[-5:])
            
            process_data(variable, ds_month, month, client)

            # if diur=='True':
            #     ds_month.to_netcdf(f'{path_out}/{timestr}_raw_2010{month}.nc')


    client.close()
    cluster.close()
    grand_toc = time.time()
    print(f'The whole script took {grand_toc - grand_tic:.2f} seconds')
    
if __name__ == "__main__":
    
    now = datetime.datetime.now()
    # Display a message indicating what is being printed
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    grand_tic = time.time()
    
    path_in = '<path-to-raw-h0-data>' # user changes
    path_out = '<path-to-processed_data>/time_domain_means/monthly/' # user changes
    
    # Create parser, get arguments, parse
    parser = argparse.ArgumentParser()
    parser.add_argument('-var', type=str, required=True, help='variable for extraction')
    parser.add_argument('-lats', type=str, required=True, help='Latitude range in the format min,max')
    parser.add_argument('-lons', type=str, required=True, help='Longitude range in the format min,max')
    parser.add_argument('-months', type=str, required=True, help='Months for calculating monthly means in, format 01,02,03,... etc')
    parser.add_argument('-times', type=str, required=True, help='time range in the format min,max = min and max hour of each day. Will be ignored if diur=True')
    parser.add_argument('-timestr', type=str, required=True, help='time string to store in file name with options day,night,diur')
    parser.add_argument('-diur', required=True, help="required options: 'True','False'")

    args = parser.parse_args()
    
    var = args.var.split(',') # Create a list of vars
    lats = list(map(float, args.lats.split(','))) # create a list of lat floats
    lons = list(map(float, args.lons.split(','))) # create a list of lon floats
    months = args.months.split(',') # create a list of lon floats
    timestr = args.timestr # get time string for filename, options: day,night,diur
    times = list(map(int, args.times.split(','))) # create a list of itime floats  
    diur = args.diur # Calculates diurnal average
    print('var, lats, lons, months, timestr, times, diur')
    print(var, lats, lons, months, timestr, times, diur)
    
    main()
