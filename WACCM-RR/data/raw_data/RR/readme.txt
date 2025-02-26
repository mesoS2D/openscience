Data to produce figures in Kupilas et al. (2025)

Key:
- nonrr - data corresponding to Non-RR model
- rr - data corresponding to RR model
- diur - data averaged over 24 hours
- night - night-time data covering local times of 2230 – 0130 in the averaging domain
- on_lev - data on pressure levels
- on_z - data on geometric altitude
- cm - "conus mean" - data averaged over the 1/8-degree region
- sor - data over the Starfire Optical Range, New Mexico
- flx - flux
- wtrans - vertical (w) transport velocity


It is organised as follows:

├───maps
│       NO_3.1hPa_nonrr_2010-06-01.nc
│       NO_3.1hPa_rr_2010-06-01.nc
│       NO_300hPa_nonrr_2010-06-01.nc
│       NO_300hPa_rr_2010-06-01.nc
│       NO_5.3e-5hPa_nonrr_2010-06-01.nc
│       NO_5.3e-5hPa_rr_2010-06-01.nc
│       NO_8.8e-3hPa_nonrr_2010-06-01.nc
│       NO_8.8e-3hPa_rr_2010-06-01.nc
│       T_3.1hPa_nonrr_2010-06-01.nc
│       T_3.1hPa_rr_2010-06-01.nc
│       T_300hPa_nonrr_2010-06-01.nc
│       T_300hPa_rr_2010-06-01.nc
│       T_5.3e-5hPa_nonrr_2010-06-01.nc
│       T_5.3e-5hPa_rr_2010-06-01.nc
│       T_8.8e-3hPa_nonrr_2010-06-01.nc
│       T_8.8e-3hPa_rr_2010-06-01.nc
│       w_3.1hPa_nonrr_2010-06-01.nc
│       w_3.1hPa_rr_2010-06-01.nc
│       w_300hPa_nonrr_2010-06-01.nc
│       w_300hPa_rr_2010-06-01.nc
│       w_5.3e-5hPa_nonrr_2010-06-01.nc
│       w_5.3e-5hPa_rr_2010-06-01.nc
│       w_8.8e-3hPa_nonrr_2010-06-01.nc
│       w_8.8e-3hPa_rr_2010-06-01.nc
│
├───monthly_domain_average
│       nonrr_diur_cm_z_gph_2010.nc
│       on_lev_nonrr_diur_cm_2010.nc
│       on_lev_nonrr_night_cm_2010.nc
│       on_lev_rr_diur_cm_2010.nc
│       on_lev_rr_night_cm_2010.nc
│       on_z_nonrr_diur_cm_2010.nc
│       on_z_nonrr_night_cm_2010.nc
│       on_z_rr_diur_cm_2010.nc
│       on_z_rr_night_cm_2010.nc
│       rr_diur_cm_z_gph_2010.nc
│
└───vertical_flx_wtrans
    ├───flux
    │   └───monthly
    │           on_lev_nonrr_flx_monthly_mean_2010-06.nc
    │           on_lev_nonrr_flx_monthly_mean_2010-12.nc
    │           on_lev_nonrr_sor_flx_monthly_mean_2010-06.nc
    │           on_lev_nonrr_sor_flx_monthly_mean_2010-12.nc
    │           on_lev_rr_flx_monthly_mean_2010-06.nc
    │           on_lev_rr_flx_monthly_mean_2010-12.nc
    │           on_lev_rr_sor_flx_monthly_mean_2010-06.nc
    │           on_lev_rr_sor_flx_monthly_mean_2010-12.nc
    │           on_z_nonrr_flx_monthly_mean_2010-06.nc
    │           on_z_nonrr_flx_monthly_mean_2010-12.nc
    │           on_z_nonrr_sor_flx_monthly_mean_2010-12.nc
    │           on_z_rr_flx_monthly_mean_2010-06.nc
    │           on_z_rr_flx_monthly_mean_2010-12.nc
    │           on_z_rr_sor_flx_monthly_mean_2010-12.nc
    │           SOR_monthly_T_flux.nc
    │
    ├───time_domain_means
    │   └───monthly
    │           nonrr_sor_mean_z_fullcol_2010-12.nc
    │           on_lev_nonrr_monthly_mean_2010-06.nc
    │           on_lev_nonrr_monthly_mean_2010-12.nc
    │           on_lev_nonrr_sor_mean_T_fullcol_2010-12.nc
    │           on_lev_rr_monthly_mean_2010-06.nc
    │           on_lev_rr_monthly_mean_2010-12.nc
    │           on_lev_rr_sor_mean_T_fullcol_2010-12.nc
    │           rr_sor_mean_z_fullcol_2010-12.nc
    │           SOR_monthly_T.nc
    │
    └───wtrans
        └───monthly
                on_lev_nonrr_sor_wtrans_2010-06.nc
                on_lev_nonrr_sor_wtrans_2010-12.nc
                on_lev_nonrr_wtrans_2010-06.nc
                on_lev_nonrr_wtrans_2010-12.nc
                on_lev_rr_sor_wtrans_2010-06.nc
                on_lev_rr_sor_wtrans_2010-12.nc
                on_lev_rr_wtrans_2010-06.nc
                on_lev_rr_wtrans_2010-12.nc
                on_z_nonrr_sor_wtrans_2010-12.nc
                on_z_nonrr_wtrans_2010-06.nc
                on_z_nonrr_wtrans_2010-12.nc
                on_z_rr_sor_wtrans_2010-12.nc
                on_z_rr_wtrans_2010-06.nc
                on_z_rr_wtrans_2010-12.nc
                SOR_monthly_T_wtrans.nc
