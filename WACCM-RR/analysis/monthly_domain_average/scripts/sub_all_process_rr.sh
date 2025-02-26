cd /glade/derecho/scratch/mmkupilas/Analysis/WACCM-RR/analysis/profiles_cm/
### Load Conda/Python module and activate NPL environment
module load conda
conda activate mmk_env_ncar

# NIGHT CM
var=O,O3,lat,lon,Z3,T
months=01,02,03,04,05,06,07,08,09,10,11,12
latL=22 latU=52 lonL=240 lonU=285 timeL=7 timeU=7 timestr=rr_night_cm diur=False
(time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &

# sleep 1
# # DAY CM
# var=O,O3,H2O,NO,T,lat,lon,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
# latL=20 latU=55 lonL=210 lonU=310 timeL=19 timeU=19 timestr=rr_day_cm diur=False
# (time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &

# sleep 1
# # NIGHT OCM
# var=O,O3,H2O,NO,T,lat,lon,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
# latL=-70 latU=-35 lonL=30 lonU=130 timeL=19 timeU=19 timestr=rr_night_ocm diur=False
# (time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &

# sleep 1
# # DAY OCM
# var=O,O3,H2O,NO,T,lat,lon,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
# latL=-70 latU=-35 lonL=30 lonU=130 timeL=7 timeU=7 timestr=rr_day_ocm diur=False
# (time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &

# sleep 1
# DIUR OCM
# var=U,V,OMEGA,O,O3,CO2,CO,NO,T,H2O,CH4,lat,lon,Z3
# var=O,O3,CO2,CO,NO,T,H2O,lat,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
# latL=-70 latU=-35 lonL=35 lonU=125 timeL=7 timeU=7 timestr=rr_diur_ocm diur=True
# (time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &

# sleep 1
# # DIUR CM
# # var=U,V,OMEGA,O,O3,CO2,CO,NO,T,H2O,CH4,lat,lon,Z3
# var=O,CO2,CO,NO,T,H2O,lat,lon,Z3
# months=01,02,03,04,05,06,07,08,09,10,11,12
# latL=22 latU=52 lonL=240 lonU=285 timeL=7 timeU=7 timestr=rr_diur_cm diur=True
# (time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur > ./scripts/$timestr.out 2>&1) &
