#!/bin/bash
# load nco

path_in=path_to_input
path_out=path_to_output
file=FWmaHIST_ne30pg3_ne30pg3_mg17_no_conus_gravity_waves.cam.h0.2010-06-01-00000.nc

ncks -d lev,17 $path_in$file $path_out/ilev_17_nonrr_extracted_$file
