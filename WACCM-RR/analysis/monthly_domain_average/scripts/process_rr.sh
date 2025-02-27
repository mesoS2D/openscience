cd /glade/derecho/scratch/mmkupilas/Analysis/WACCM-RR/analysis/profiles_cm/

### Load Conda/Python module and activate NPL environment
module load conda
conda activate mmk_env_ncar

# Assigns contents of varfile.txt to var, format var=var1,var2,var3,... etc
var=$(cat /glade/derecho/scratch/mmkupilas/Analysis/WACCM-RR/analysis/profiles_cm/scripts/varfile.txt)
months=$(cat /glade/derecho/scratch/mmkupilas/Analysis/WACCM-RR/analysis/profiles_cm/scripts/monthfile.txt)
### Run analysis script
time python process_rr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur
