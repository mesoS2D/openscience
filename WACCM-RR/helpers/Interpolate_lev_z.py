import numpy as np
import xarray as xr
import time

def interpolate_lev_to_z_ncol(ds): 
# PARTIALLY DONE, TODO NEEDS IMPLEMENTATION OF DUMMY TIME IF TIME NOT IN DATASET
# THIS MIGHT LATER BE ABSORBED INTO interpolate_lev_to_z_latlon as just simply
# interpolate_lev_to_z.
                                    
    toc = time.time()
    nlev = ds.lev.size
    ntime = ds.time.size
    
    createnew = False
    # create ncol dim if not in ds
    if "ncol" not in ds.dims: 
        print("ncol not in dims")
        print("nlev, ntime", nlev, ntime)
        createnew = True

    else:
        nncol = ds.ncol.size
        print("nlev, ntime, nncol", nlev, ntime, nncol)

    # TODO immplement adding time as a dimensions if not in dataset
    
    z_interp = np.arange(120,50,-0.25) # Create vertical coordinate in z
    ds_interp_icol_step = []
    ds_interp_itime_step = []
    counter = 0
    # Loop over individual vertical columns in both space and time
    # Remove lev as a coordinate
    # Swap it with z variable, make z the coordinate and dimension
    # Interpolate the z dimension onto desired values specified by z_interp
    # Append all vertical columns to a list over each dimension.
    #
    # I.e., ds_interp_icol_step eventually contains all interpolated columns looped over for an individual time.
    # Once all columns for an individual time have been looped over and interpolated, this list is converted into
    # an xarray dataset with dimensions ncol and z, and this dataset is appended to the list ds_interp_itime_step.
    #
    # ds_interp_itime_step eventually contains all interpolated snapshots.
    # Once this occurs, it is then converted to an xarray dataset with dimensions ncol, z and time (not sure which order, this doesn't really matter anyway)
    #
    if createnew == False:
        for itime in range(ntime):
            toc1 = time.time()
            for icol in range(nncol):
                counter += 1
                # print("Interpolating, ", "{:.3f}".format(100*counter/(ntime*nncol)) + " %", end="\r")
                
                # Set up temp dataset replacing lev with z as indexed dimension
                ds_temp = ds.isel(time=itime,ncol=icol).swap_dims({'lev':'z'}).reset_coords("lev")
                # Interpolate lev to z 
                ds_temp = ds_temp.interp(z=z_interp)
                # Append 
                ds_interp_icol_step.append(ds_temp)
                
            # Concat
            ds_interp_icol_step = xr.concat(ds_interp_icol_step, dim="ncol")
            # Append
            ds_interp_itime_step.append(ds_interp_icol_step)
            # Reset
            ds_interp_icol_step = []
        
            print("Interpolating time", itime, "took", "{:.4f}".format(time.time() - toc1), "seconds")
            print("Completed", "{:.3f}".format(100*counter/(ntime*nncol)) + " %")
    else:
        for itime in range(ntime):
            print("Interpolating time", itime)
            toc1 = time.time()
            counter += 1
            # print("Interpolating, ", "{:.3f}".format(100*counter/(ntime*nncol)) + " %", end="\r")
            
            # Set up temp dataset replacing lev with z as indexed dimension
            ds_temp = ds.isel(time=itime).swap_dims({'lev':'z'}).reset_coords("lev")
            # Interpolate lev to z 
            ds_temp = ds_temp.interp(z=z_interp)
            # Append 
            ds_interp_itime_step.append(ds_temp)
    
        print("That took", "{:.4f}".format(time.time() - toc1), "seconds")
        print("Completed", "{:.3f}".format(100*counter/(ntime)) + " %")

        
        
    # Concat itime step
    ds_interpolated = xr.concat(ds_interp_itime_step, dim="time")
    print("Interpolating took", "{:.4f}".format(time.time() - toc), "seconds")
          
    return ds_interpolated

def interpolate_lev_to_z_latlon(ds, z_interp = np.arange(120,50,-1)): # In Progress
    
    toc = time.time()
    nlev = ds.lev.size
    
    create_lat = create_lon = create_time = False
    if "lat" not in ds.dims: 
        print("lat not in dims, createing dummy lat")
        ds['lat'] = 1
        ds = ds.assign_coords({"lat":ds.lat}).expand_dims(dim={"lat":1})
        create_lat = True

    if "lon" not in ds.dims:
        print("lon not in dims, creating dummy lon")
        ds['lon'] = 1
        ds = ds.assign_coords({"lon":ds.lon}).expand_dims(dim={"lon":1})
        create_lon = True

    if "time" not in ds.dims:
        print("time not in dims, creating dummy time")
        ds['time'] = 1
        ds = ds.assign_coords({"time":ds.time}).expand_dims(dim={"time":1})
        create_time = True
        
    # TODO?
    # if "ncol" in ds.dims:
    #     ds.lat = 1
    #     ds.lon = ds.ncol
    #     # This is just a hack so I don't have to rewrite
    #     # a whole new routine to do ncol.
    #     # It uses lon in space of ncol, 
    # 
    
    nlat = ds.lat.size
    nlon = ds.lon.size
    ntime = ds.time.size
    
        
    print("nlev, ntime, nlat, nlon " + str(nlev) + " " + str(ntime) + " " + str(nlat) + " " + str(nlon))

    print()

    ds_interp_itime_step = []
    ds_interp_ilat_step = []
    ds_interp_ilon_step = []
    
    counter = 0
    for itime in range(ntime):
        toc1 = time.time()
        for ilat in range(nlat):
            for ilon in range(nlon):
                counter += 1
                
                # Set up temp dataset replacing lev with z as indexed dimension
                ds_temp = ds.isel(time=itime,lat=ilat,lon=ilon).swap_dims({'lev':'z'}).reset_coords("lev")
                # Interpolate lev to z 
                ds_temp = ds_temp.interp(z=z_interp)
                # Append 
                ds_interp_ilon_step.append(ds_temp)
            
            # Concat ilon step
            ds_interp_ilon_step = xr.concat(ds_interp_ilon_step, dim="lon")
            # Append to ilat step
            ds_interp_ilat_step.append(ds_interp_ilon_step)
            # Reset ilon step
            ds_interp_ilon_step = []
        
        # Concat ilat step
        ds_interp_ilat_step = xr.concat(ds_interp_ilat_step, dim="lat")
        # Append to itime step
        ds_interp_itime_step.append(ds_interp_ilat_step)
        # Reset ilat step
        ds_interp_ilat_step = []
    
        print("Interpolating time", itime, "took", "{:.4f}".format(time.time() - toc1), "seconds")
        print("Completed", "{:.3f}".format  (100*counter/(ntime*nlat*nlon)) + " %")
    
    # Concat itime step
    ds_interpolated = xr.concat(ds_interp_itime_step,dim="time")
         
    print("Interpolating took", "{:.4f}".format(time.time() - toc), "seconds")
    
    if create_lat == True:
        ds_interpolated = ds_interpolated.isel(lat=0).drop("lat")
        print('Dropping dummy lat')
    if create_lon == True:
        ds_interpolated = ds_interpolated.isel(lon=0).drop("lon")
        print('Dropping dummy lon')
    if create_time == True:
        ds_interpolated = ds_interpolated.isel(time=0).drop("time")
        print('Dropping dummy time')
          
    return ds_interpolated


def interpolate_z_to_lev_latlon(ds): 
    
    toc = time.time()
    nz = ds.z.size
    ntime = ds.time.size
    
    if "lat" not in ds.dims: 
        print("lat not in dims, createing lat")
        ds['lat'] = 1
        ds = ds.assign_coords({"lat":ds.lat}).expand_dims(dim={"lat":1})
        create_lat = True

    if "lon" not in ds.dims:
        print("lon not in dims, creating lon")
        ds['lon'] = 1
        ds = ds.assign_coords({"lon":ds.lon}).expand_dims(dim={"lon":1})
        create_lon = True
        
    # TODO create time?

    nlat = ds.lat.size
    nlon = ds.lon.size
        
    print("nz, ntime, nlat, nlon " + str(nz) + " " + str(ntime) + " " + str(nlat) + " " + str(nlon))
    
    lev_interp = np.logspace(0,-5,51).tolist()
    ds_interp_itime_step = []
    ds_interp_ilat_step = []
    ds_interp_ilon_step = []
    
    counter = 0
    for itime in range(ntime):
        toc1 = time.time()
        for ilat in range(nlat):
            for ilon in range(nlon):
                counter += 1
                
                # Set up temp dataset replacing lev with z as indexed dimension
                ds_temp = ds.isel(time=itime,lat=ilat,lon=ilon).swap_dims({'z':'lev'}).reset_coords("z")
                # Interpolate lev to z 
                ds_temp = ds_temp.interp(lev=lev_interp)
                # Append 
                ds_interp_ilon_step.append(ds_temp)
            
            # Concat ilon step
            ds_interp_ilon_step = xr.concat(ds_interp_ilon_step, dim="lon")
            # Append to ilat step
            ds_interp_ilat_step.append(ds_interp_ilon_step)
            # Reset ilon step
            ds_interp_ilon_step = []
        
        # Concat ilat step
        ds_interp_ilat_step = xr.concat(ds_interp_ilat_step, dim="lat")
        # Append to itime step
        ds_interp_itime_step.append(ds_interp_ilat_step)
        # Reset ilat step
        ds_interp_ilat_step = []
    
        print("Interpolating time", itime, "took", "{:.4f}".format(time.time() - toc1), "seconds")
        print("Completed", "{:.3f}".format  (100*counter/(ntime*nlat*nlon)) + " %")
    
    # Concat itime step
    ds_interpolated = xr.concat(ds_interp_itime_step,dim="time")
         
    print("Interpolating took", "{:.4f}".format(time.time() - toc), "seconds")
    
    if create_lat == True:
        ds_interpolated = ds_interpolated.isel(lat=0).drop("lat")
    if create_lon == True:
        ds_interpolated = ds_interpolated.isel(lon=0).drop("lon")
          
    return ds_interpolated