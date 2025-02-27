cd <path-to-code-location>

### Load Conda/Python module and activate NPL environment
module load conda
conda activate analysis

# Assigns contents of varfile.txt to var, format var=var1,var2,var3,... etc
var=$(cat ./scripts/varfile.txt)
months=$(cat ./scripts/monthfile.txt)
### Run analysis script
time python process_nonrr.py -var=$var -lats=$latL,$latU -lons=$lonL,$lonU -months=$months -times=$timeL,$timeU -timestr=$timestr -diur=$diur
