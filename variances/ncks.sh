#!/bin/bash/

module load anaconda3
source activate analysis

path_in_nonrr=path-to-full_globe_full_atmos_nonrr/
path_in_rr=path-to-full_globe_full_atmos_rr/

path_out=path-to-reduced_data/1D_timeseries/

cd $path_in_nonrr
for file in *2010-06*
do 
    ncks -d ncol,32041 -v T,OMEGA,U,V,NO,O,O3,CO2,CO,lat,lon,area $file $path_out/sor_extracted_$file
done

for file in *2010-12*
do 
    ncks -d ncol,32041 -v T,OMEGA,U,V,NO,O,O3,CO2,CO,lat,lon,area $file $path_out/sor_extracted_$file
done

cd $path_in_rr
for file in *2010-06*
do 
    ncks -d ncol,117008 -v T,OMEGA,U,V,NO,O,O3,CO2,CO,lat,lon,area $file $path_out/sor_extracted_$file
done

for file in *2010-12*
do 
    ncks -d ncol,117008 -v T,OMEGA,U,V,NO,O,O3,CO2,CO,lat,lon,area $file $path_out/sor_extracted_$file
done
