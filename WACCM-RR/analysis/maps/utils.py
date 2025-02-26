import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker

import time 

def auto_fmt(x, pos): # Tick formatting function for colorbar for auto_vrange 
    return f'{x:.2e}'
    
def validate_list(lst): # Function to enforce specific pressure level selections (just execute this and don't worry about it). 
    """
    Raises a ValueError if the list does not meet the following criteria:
        - Contains only numbers 0, 1, 2, and 3
        - Contains no duplicate elements

        Purpose - validate pressure selection list. 
        This might be more relaxed once we want to plot other pressure levels.

    Args:
        lst: The list to validate

    Raises:
        ValueError: If the list does not meet the criteria.
    """

    if not all(x in [0, 1, 2, 3] for x in lst):
        raise ValueError("List can only contain numbers 0, 1, 2, or 3. Your code won't work.")
    if len(lst) != len(set(lst)):
        raise ValueError("List cannot contain duplicate elements. Your code won't work.")
    
def get_labels(var, lev_str):
    if var == 'T':
        cmap = 'RdYlBu_r'        
        title = f'{float(lev_str):.2e} hPa'     
        cbar_label = 'T (K)'  
    elif var == 'U':
        cmap = 'seismic'           
        title = f'{float(lev_str):.2e} hPa'  
        cbar_label = 'U (m s$^{-1}$)' 
    elif var == 'V':
        cmap ='seismic'           
        title = f'{float(lev_str):.2e} hPa'  
        cbar_label = 'V (m s$^{-1}$)'
    elif var == 'w':
        cmap = 'seismic'           
        title = f'{float(lev_str):.2e} hPa'  
        cbar_label = 'w (m s$^{-1}$)'     
    elif var == 'ELECDEN':
        cmap = 'RdYlBu_r'           
        title = f'{float(lev_str):.2e} hPa'  
        cbar_label = 'log$_{10}$ Elec den (cm$^{-3}$)'  
    else:
        cmap = 'RdYlBu_r'
        title = ""
        cbar_label = ""
        
    return cmap, title, cbar_label
    
def get_preset_vrange_and_scale(var, lev_str, preset_str, season_str, ds_plot):
    
    print(f'getting presets for var {var} lev_str {lev_str} preset_str {preset_str} season_str {season_str}')
    
    # -------------------------------
    # Temperature
    # -------------------------------                  
                    
    if var == 'T':
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = 290
                    vrangeU = 390
        if var == 'T':
            if lev_str == '104.00000000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 200
                        vrangeU = 220
        if var == 'T':
            if lev_str == '10.00000000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 200
                        vrangeU = 220
        if var == 'T':
            if lev_str == '2.96000000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 212
                        vrangeU = 240
        if var == 'T':
            if lev_str == '1.06000000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 240
                        vrangeU = 280
        if var == 'T':
            if lev_str == '0.09670000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 250
                        vrangeU = 300
        if var == 'T':
            if lev_str == '0.01080000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 210
                        vrangeU = 250
        if var == 'T':
            if lev_str == '0.00743000':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 210
                        vrangeU = 250
        if var == 'T':
            if lev_str == '0.00097800':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 170
                        vrangeU = 210
        if var == 'T':
            if lev_str == '0.00011500':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 180
                        vrangeU = 280
        if var == 'T':
            if lev_str == '0.00004750':
                if preset_str == 'scandi-rr':
                    if season_str == 'DJF':
                        vrangeL = 250
                        vrangeU = 400
    # -------------------------------
    # Zonal Wind
    # -------------------------------               
    if var == 'U':
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -30
                    vrangeU = 30

        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -60
                    vrangeU = 60

        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -100
                    vrangeU = 100

        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -140
                    vrangeU = 140

    # -------------------------------
    # Meridional wind
    # -------------------------------   
    if var == 'V':
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -40
                    vrangeU = 40

        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -50
                    vrangeU = 50

        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -100
                    vrangeU = 100

        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -120
                    vrangeU = 120

    # -------------------------------
    # Vertical wind
    # -------------------------------    
    if var == 'w':
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -0.3
                    vrangeU = 0.3
    if var == 'w':
        if lev_str == '104.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -0.3
                    vrangeU = 0.3
    if var == 'w':
        if lev_str == '10.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -0.75
                    vrangeU = 0.75
    if var == 'w':
        if lev_str == '1.06000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -2
                    vrangeU = 2
                    
        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -2
                    vrangeU = 2
    if var == 'w':
        if lev_str == '0.09670000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -3
                    vrangeU = 3
    if var == 'w':
        if lev_str == '0.01080000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -3
                    vrangeU = 3
                    
        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -5
                    vrangeU = 5

        if lev_str == '0.00097800':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -5
                    vrangeU = 5

        if lev_str == '0.00011500':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -5
                    vrangeU = 5

        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = -5
                    vrangeU = 5

    # -------------------------------
    # ELECTRON DENSITY
    # -------------------------------   
    if var == 'ELECDEN':
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = np.log10(1e-17)
                    vrangeU = np.log10(1e-15)

        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = np.log10(1e-18)
                    vrangeU = np.log10(1e-17)

        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = np.log10(5e2)
                    vrangeU = np.log10(1.5e3)

        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                if season_str == 'DJF':
                    vrangeL = np.log10(2e3)
                    vrangeU = np.log10(1.5e5)
        ds_plot = np.log10(ds_plot)        

    # -------------------------------
    # Atomic oxygen
    # -------------------------------     
    if var == 'O':
        None
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                None 
        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                None

    # -------------------------------
    # Nitric oxide
    # -------------------------------     
    if var == 'NO':
        None
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                None 
        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                None

    # -------------------------------
    # Ozone
    # -------------------------------     
    if var == 'O3':
        None
        if lev_str == '302.00000000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '2.96000000':
            if preset_str == 'scandi-rr':
                None 
        if lev_str == '0.00743000':
            if preset_str == 'scandi-rr':
                None
        if lev_str == '0.00004750':
            if preset_str == 'scandi-rr':
                None
                
    cbar_ticks = [vrangeL,vrangeU]
    return vrangeL, vrangeU, cbar_ticks, ds_plot



# Main plotting function called from both notebook and script
def plot_maps(ds1, var_list_plot, lev_list_plot, itime_list_plot, model_str, preset_vrange, preset_str, season_str, auto_vrange, user_vrange,center_lat, center_lon, xlimL, xlimU, ylimL, ylimU, show_plot, save_plot, path_to_save_plot,misc_str, labelsize=10,orthographic=True,xticks=None,yticks=None):
    for var in var_list_plot:
        for lev_str in lev_list_plot:
            for itime in itime_list_plot:
                grand_plot_tic = time.time()
                
                print(f'{model_str}_{var}_{lev_str}_{ds1.time.isel(time=itime).values.item().strftime("%Y-%m-%d_%H:%M:%S")}')

                # ------------------------------------------------------------------------
                # SELECT DATA
                # ------------------------------------------------------------------------
                ds_plot = ds1[var].isel(time=itime).sel(lev=float(lev_str),method='nearest').sel(lat=slice(ylimL-15,ylimU+15),lon=slice(xlimL-15,xlimU+15))

                # ------------------------------------------------------------------------
                # PLOT DATA
                # ------------------------------------------------------------------------
                plot_tic = time.time()

                # -----------------------
                # Set-up options
                # -----------------------
                cmap = 'RdYlBu_r'
                if preset_vrange == True: # presets
                    # Get:
                    # range
                    # cbar_ticks
                    # title
                    # cbar_label
                    # colormap
                    # scaled dataset if applicable

                    vrangeL, vrangeU, cbar_ticks, ds_plot = get_preset_vrange_and_scale(var,lev_str,preset_str,season_str, ds_plot)

                    cbar_ticklabels = cbar_ticks
                    
                if auto_vrange == True: # automatic choice
                    # if var == 'ELECDEN':
                        # ds_plot = np.log10(ds_plot)
                        
                        
                    vrangeL = np.min(ds_plot.sel(lat=slice(ylimL-5,ylimU+5),lon=slice(xlimL-5,xlimU+5)).values)
                    vrangeU = np.max(ds_plot.sel(lat=slice(ylimL-5,ylimU+5),lon=slice(xlimL-5,xlimU+5)).values)
                    print(f'auto vrangeL {vrangeL:2e} vrangeU {vrangeU:.2e}')
                    cbar_ticks = np.linspace(vrangeL,vrangeU,5)
                    cbar_ticklabels = np.linspace(vrangeL,vrangeU,5)
                    cmap ='RdYlBu_r'

                    tick_format = mticker.FuncFormatter(auto_fmt)

                    # if var == 'ELECDEN':
                        # cbar_ticklabels = ([f'10^{tick:.2f}' for tick in cbar_ticks])


                if user_vrange == True: # choice by user
                    vrangeL = vrangeL
                    vrangeU = vrangeU
                    cbar_ticks = np.linspace(vrangeL,vrangeU,5)
                    cbar_ticklabels = np.linspace(vrangeL,vrangeU,5)

                    tick_format = mticker.FuncFormatter(user_fmt)
                    
                cmap, title, cbar_label = get_labels(var,lev_str)
                
                # ------------------------------------------------------------------------
                # CREATE PLOT
                # ------------------------------------------------------------------------
                    
                # Set up the figure and map projection
                fig = plt.figure(dpi=150)
                
                # Use Orthographic projection centered at lon=20, lat=70
                print("orthographic", orthographic)
                if orthographic:
                    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=center_lon, central_latitude=center_lat))
                else:
                    ax = plt.axes(projection=ccrs.PlateCarree())

                
                # Set the extent (this is more for setting up limits for visible data range)
                if orthographic:
                    ax.set_extent([xlimL, xlimU, ylimL, ylimU])
                else:
                    ax.set_xlim(xlimL,xlimU)
                    ax.set_ylim(ylimL,ylimU)
                # Plot Orthographic projection
                
                if orthographic:
                    p = ds_plot.plot(ax=ax, transform=ccrs.PlateCarree(), add_colorbar=False, vmin=vrangeL, vmax=vrangeU, cmap=cmap)
                else:
                    p = ds_plot.plot(ax=ax,add_colorbar=False, vmin=vrangeL, vmax=vrangeU, cmap=cmap)
                    
                # Add colorbar and control labels
                cb = plt.colorbar(p, pad=0.005)
                
                # if user_vrange or preset_vrange == True:
                cb.ax.set_yticks(cbar_ticks)      
                cb.ax.set_yticklabels(cbar_ticklabels) 
                if auto_vrange:
                    cb.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.2e}" if y in cbar_ticks else ""))
                cb.ax.set_ylabel(cbar_label,fontsize=labelsize)                
                cb.ax.yaxis.set_label_coords(1.5,0.5)                

                cb.ax.tick_params(labelsize=labelsize)
                                
                # Add coastlines
                ax.coastlines(resolution='50m', color='black', linewidth=0.8)
                
                # Add gridlines with x and y ticks and labels
                gl = ax.gridlines(draw_labels=True,linestyle=':', color='gray')
                gl.top_labels = False  # Turn off labels on the top axis
                gl.right_labels = False  # Turn off labels on the right axis
                gl.xlabel_style = {'size': labelsize, 'color': 'black'}  # Customize x-label style
                gl.ylabel_style = {'size': labelsize, 'color': 'black'}  # Customize y-label style
                # gl.set_yticks(xticks)
                # ax.set_yticks(yticks)
                if orthographic:
                    if xticks != None:
                        gl.xlocator = mticker.FixedLocator(xticks)
                        gl.yformatter = mticker.FuncFormatter(lambda y, _: f"{int(y)}°" if y in yticks else "")
                    if yticks != None:
                        gl.ylocator = mticker.FixedLocator(yticks)
                        gl.xformatter = mticker.FuncFormatter(lambda x, _: f"{int(x)}°" if x in xticks else "")
                else:
                    gl.top_labels = gl.right_labels = gl.bottom_labels = gl.left_labels = False
                    if xticks != None:
                        gl.xlocator = mticker.FixedLocator(xticks)
                        ax.set_xticks(xticks)
                        ax.set_xticklabels([f"{int(x)}°" for x in xticks],fontsize=labelsize)
                    if yticks != None:
                        gl.ylocator = mticker.FixedLocator(yticks)
                        ax.set_yticks(yticks)
                        ax.set_yticklabels([f"{int(y)}°" for y in yticks],fontsize=labelsize)
                    ax.set_xlabel('')
                    ax.set_ylabel('')
                # Add title

                title = title + f'\n{ds_plot.time.values}'
                plt.title(title)
                    
                # Show


                
                plot_toc = time.time()
                print(f'Plotting took {plot_toc - plot_tic:.2f} seconds')

                grand_plot_toc = time.time()
                print(f'The whole plotting procedure took {grand_plot_toc - grand_plot_tic:.2f} seconds')
                
                if show_plot == True:
                    plt.show()
                if save_plot == True:
                    fname = f'{misc_str}_{model_str}_{var}_{lev_str}_{ds_plot.time.values.item().strftime("%Y-%m-%d_%H:%M:%S")}.png'
                    plt.savefig(path_to_save_plot+fname, bbox_inches='tight')
                    plt.close(fig)
