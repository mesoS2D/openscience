Code used to produce seasonality plots

- bash script to extract Non-RR h0 data - sub_all_process_nonrr.sh  
- python script that does extraction - process_nonrr.py - optimised to run on Casper  
- script to extract RR h0 data - sub_all_process_rr.sh  
- python script that does extraction - process_rr.py  


Both scripts work by specifying  
var : Variable of choice present in the dataset, see docs hist_rr/nonrr.txt  
months : One or more of 01,02,03,04,05,06,07,08,09,10,11,12  
latL=22 : lower latitude limit  
latU=52 : upper lat lim  
lonL=240 : lower lon lim (works on 0 - 360 axis, not -180 - 180)  
lonU=285 : upper lon lim   
timeL=7 : lower time limit (in UTC)  
timeU=7 : upper time limit   
timestr : "time string" - this goes into filename and can be whatever you want, for now chosen as (nonrr_night_cm/rr_night_cm, nonrr_day_cm, nonrr_diur_cm)   
diur : Boolean True or False : if False, does nothing, if True, ignores time specifications and calculates diurnal average from instantaneous data every 3 hours.  

Options are also documented in the script.  

