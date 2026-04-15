Install conda environment using yaml file in envs  

CONUS_WACCMRR 

# ----------------------------------------
# Figure 1a
# ----------------------------------------

cd to CONUS_WACCMRR/maps and run from the command line: 
> ncl EXODUS2plot 

# ----------------------------------------
# Figure 1b
# ----------------------------------------

cd to CONUS_WACCMRR/maps and use plot_maps_plot_2d.ipynb

# ----------------------------------------
# Figure 2
# ----------------------------------------

use CONUS_WACCMRR/spectra/2d_spectra_regimes.ipynb

# ----------------------------------------
# Figure 3, 4 - 2D maps
# ----------------------------------------

cd to CONUS_WACCMRR/maps

1) use ncks.sh as template for extracting slices from raw model output, produces data in CONUS_RR_PROCESSED_DATA/reduced_data/maps

2) use extract_and_regrid.ipynb to regrid output from (1), produces data in CONUS_RR_PROCESSED_DATA/processed_data/maps/regridded

3) use plot_regridded.ipynb to plot data from (2)

# ----------------------------------------
# Figure 5 - vertical wavenumber spectra
# ----------------------------------------

Makes use of 
- pressure to geometric height calculation utility code
- interpolating pressure altitude coordinate to geometric height utility code

Utility code found in CONUS_WACCMRR/util_files

cd CONUS_WACCMRR/spectra

1) use 1d_timeseries_ncks.sh template to extract single column timeseries data

Operate on data in /CONUS_PAPER_DATA/
Output to /CONUS_RR_PROCESSED_DATA/reduced_data/1D_timeseries/

2) run vertical_wavenumber_spectra.ipynb notebook on data from (1) to calculate and plot spectra

# ----------------------------------------
# Figure 6 - frequency spectra
# ----------------------------------------

Makes use of calculate_rho_w utility code

1) use 1d_timeseries_ncks.sh template to extract single column timeseries data

Operate on data in /CONUS_PAPER_DATA/
Output to /CONUS_RR_PROCESSED_DATA/reduced_data/1D_timeseries/

2) run 1D_frequency_spectra.ipynb on data from (1) to calculate and plot spectra.

# ----------------------------------------
# Figure 7 - horizontal wavenumber spectra
# ----------------------------------------

Makes use of spec_utils_2d utility code 

1) Follow instructions for Figures 3,4 to extract and regrid 2D maps, if not done so already

2) cd CONUS_WACCMRR/spectra, use spectra_from_2d_maps to calculate 2D spectra, bin to 1D spectra and write these out as netcdf files

These are saved in CONUS_RR_PROCESSED_DATA/processed_data/spectra/h_spectra_1d

3) use spectra_from_2d_maps to plot spectra

# ----------------------------------------
# Figure 8, 9, 10 - 2D 1 year monthly domain mean timeseries
# ----------------------------------------

Search for "user changes" in process_{nonrr,rr}.py

Adapt script in process_{nonrr,rr}.sh

Search for "user changes" in profiles_plot.ipynb

# ----------------------------------------
# Figure 11, 12
# ----------------------------------------

in flux_wtrans

1) Use derive_flx_wtrans.ipynb to process the raw data

2) Plot the results in plot_flx_wtrans.ipynb

# ----------------------------------------
# Figure 13, A1
# ----------------------------------------

Use variances/ncks.sh to extract timeseries.

See var.ipynb to produce figure, follow user changes.

# ----------------------------------------
# Figure 14
# ----------------------------------------

To get observed fluxes and transport velocities follow process_observations_flux_wtrans.ipynb

Use code in plot_flux_wtrans.ipynb in flux_wtrans to create plot.
