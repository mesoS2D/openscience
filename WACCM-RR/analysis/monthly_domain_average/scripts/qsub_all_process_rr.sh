cd /glade/derecho/scratch/mmkupilas/Analysis/WACCM-RR/analysis/profiles_cm/
### Load Conda/Python module and activate NPL environment
module load conda
conda activate mmk_env_ncar

# NIGHT CM
var=O,O3,H2O,NO,lat,lon,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
months=01
latL=20 
latU=55 
lonL=210 
lonU=310 
timeL=7 
timeU=7 
timestr=night_cm 
diur=False
time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur >> $timestr.out

# # DAY CM
# sleep 5 # MMK: Needs to be here, otherwise the lines below execute faster than the lines in the submission scripts called by qsub
# # When this happens then the monthfile called from within each submission script will not be what corresponds
# # to the one set for it. 
# # Previously when I had no sleep, all lines in this script were executed really fast
# # and the monthfile.txt contained all months - as set by the final
# # echo "01, 02,..." > monthfile.txt line that appears in this script.
# # Sleep gives time for the lines in the script called by the qsub command to be executed first.
# # echo "O,O3,CO2,CO,NO,T,H2O,lat,lon,Z3" > varfile.txt
# # echo "01,02,03,04,05,06,07,08,09,10,11,12" > monthfile.txt
# # latL=20 latU=55 lonL=210 lonU=310 
# timeL=19 timeU=19 timestr=day_cm diur=False
# qsub -v latL=$latL,latU=$latU,lonL=$lonL,lonU=$lonU,timeL=$timeL,timeU=$timeU,timestr=$timestr,diur=$diur process_rr.sh 

# # NIGHT OCM
# sleep 5
# # echo "O,O3,CO2,CO,NO,T,H2O,lat,lon,Z3" > varfile.txt
# # echo "01,02,03,04,05,06,07,08,09,10,11,12" > monthfile.txt
# # latL=-70 latU=-35 lonL=30 lonU=130
# timeL=19 timeU=19 timestr=night_ocm diur=False
# qsub -v latL=$latL,latU=$latU,lonL=$lonL,lonU=$lonU,timeL=$timeL,timeU=$timeU,timestr=$timestr,diur=$diur process_rr.sh 

# # DAY OCM
# sleep 5
# # echo "O,O3,CO2,CO,NO,T,H2O,lat,lon,Z3" > varfile.txt
# # echo "01,02,03,04,05,06,07,08,09,10,11,12" > monthfile.txt
# latL=-70 latU=-35 lonL=30 lonU=130 
# timeL=7 timeU=7 timestr=day_ocm diur=False
# qsub -v latL=$latL,latU=$latU,lonL=$lonL,lonU=$lonU,timeL=$timeL,timeU=$timeU,timestr=$timestr,diur=$diur process_rr.sh 

# # DIUR OCM
# sleep 5
# # echo "O,O3,CO2,CO,NO,T,H2O,lat,lon,Z3" > varfile.txt
# # echo "01,02,03,04,05,06,07,08,09,10,11,12" > monthfile.txt
# latL=-70 latU=-35 lonL=30 lonU=130 
# timeL=0 timeU=0 timestr=diur_ocm diur=True # Not used because diur=True, but must be passed in
# qsub -v latL=$latL,latU=$latU,lonL=$lonL,lonU=$lonU,timeL=$timeL,timeU=$timeU,timestr=$timestr,diur=$diur process_rr.sh 

# # DIUR CM
# sleep 5
# # echo "O,O3,CO2,CO,NO,T,H2O,lat,lon,Z3" > varfile.txt
# # echo "01,02,03,04,05,06,07,08,09,10,11,12" > monthfile.txt
# latL=20 latU=55 lonL=210 lonU=310 
# timeL=0 timeU=0 timestr=diur_cm diur=True # Not used because diur=True, but must be passed in
# # echo "09,10,11,12" > monthfile.txt
# qsub -v latL=$latL,latU=$latU,lonL=$lonL,lonU=$lonU,timeL=$timeL,timeU=$timeU,timestr=$timestr,diur=$diur process_rr.sh 
