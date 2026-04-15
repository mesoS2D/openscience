import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import gc
import time 

def get_preset_vrange_and_scale(var, lev_str, preset_str, season_str, xlimL, xlimU, ylimL, ylimU, ds_plot):
    
    # This is here in case you've not put in a preset for a given var/lev/preset/season combo
    vrangeL = np.min(ds_plot.sel(lat=slice(ylimL-1,ylimU+1),lon=slice(xlimL-1,xlimU+1)).dropna(dim='lat').dropna(dim='lon').values)                
    vrangeU = np.max(ds_plot.sel(lat=slice(ylimL-1,ylimU+1),lon=slice(xlimL-1,xlimU+1)).dropna(dim='lat').dropna(dim='lon').values)
    print(f'getting presets for var {var} lev_str {lev_str} preset_str {preset_str} season_str {season_str}')
    cbar_ticks=[vrangeL,vrangeU]
    
    # -------------------------------
    # Temp
    # -------------------------------     
    if var == 'temp':
        if lev_str == 'temp':
            if preset_str == 'temp':
                None
      
    cbar_ticks = [vrangeL,vrangeU]
    return vrangeL, vrangeU, cbar_ticks, ds_plot



# Main plotting function called from both notebook and script
def plot_maps(ds_plot, var, lev_str,preset_vrange, preset_str, season_str, auto_vrange, user_vrange,vrangeL,vrangeU, vrange_nticks, center_lat, center_lon, xlimL, xlimU, ylimL, ylimU, show_plot, save_plot, colorbar_fraction, colorbar_shrink, colorbar_pad, path_to_save_plot,labelsize=10,orthographic=True,xticks=None,yticks=None, persist=False, user_cmap=None, fname='map', plot_title='map'):
    if persist: persist_counter = 0
    grand_plot_tic = time.time()
    # ------------------------------------------------------------------------
    # Print controls
    # ------------------------------------------------------------------------
    print(ds_plot)
    print('dims', list(ds_plot.dims))
    print('var', var)
    print('lev_str', lev_str)
    print('preset_vrange', preset_vrange)
    print('preset_str', preset_str)
    print('season_str', season_str)
    print('auto_vrange', auto_vrange)
    print('user_vrange', user_vrange)
    print('vrangeL', vrangeL)
    print('vrangeU', vrangeU)
    print('center_lat', center_lat)
    print('center_lon', center_lon)
    print('xticks', xticks)
    print('yticks', yticks)
    print('colorbar_fraction', colorbar_fraction)
    print('colorbar_shrink', colorbar_shrink)
    print('colorbar_pad', colorbar_pad)
    print('labelsize', labelsize)
    print('save_plot', save_plot)
    print('path_to_save_plot', path_to_save_plot)
    print('orthographic', orthographic)
    print('persist', persist)
    if persist: 
        print('persist_counter', persist_counter)
    print('xlimL', xlimL)
    print('xlimU', xlimU)
    print('ylimL', ylimL)
    print('ylimU', ylimU)
    print('user_cmap', user_cmap)
    print('\n')

    fname = fname
    print(f'Plotting {fname}')
    print('The above will be the filename if save_plot is True')
    print('save_plot',save_plot)
    

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
        # scaled dataset if applicable
        print('Using preset vrange, currently no presets programmed')
        vrangeL, vrangeU, cbar_ticks, ds_plot = get_preset_vrange_and_scale(var,lev_str,preset_str,season_str, xlimL, xlimU, ylimL, ylimU, ds_plot)

        cbar_ticklabels = cbar_ticks
        
    if auto_vrange == True: # automatic choice
            
        vrangeL = np.min(ds_plot.sel(lat=slice(ylimL-1,ylimU+1),lon=slice(xlimL-1,xlimU+1)).dropna(dim='lat').dropna(dim='lon').values)
        vrangeU = np.max(ds_plot.sel(lat=slice(ylimL-1,ylimU+1),lon=slice(xlimL-1,xlimU+1)).dropna(dim='lat').dropna(dim='lon').values)
        print(ds_plot)
        if persist:
            if persist_counter == 0:
                print('persist True and counter 0: vranges saved')
                save_vrangeL = vrangeL
                save_vrangeU = vrangeU
                persist_counter += 1    
            else:
                print('Using persistent vrange')
                vrangeL = save_vrangeL
                vrangeU = save_vrangeU
                
        cbar_ticks = np.linspace(vrangeL,vrangeU,5)
        cbar_ticklabels = np.linspace(vrangeL,vrangeU,5)
        cmap ='RdYlBu_r'

    if user_vrange == True: # choice by user
        vrangeL = vrangeL
        vrangeU = vrangeU
        cbar_ticks = np.linspace(vrangeL,vrangeU,vrange_nticks)
        cbar_ticklabels = np.linspace(vrangeL,vrangeU,vrange_nticks)
                        
    if user_cmap!=None: cmap = user_cmap
    
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
    cb = plt.colorbar(p, fraction=colorbar_fraction, shrink=colorbar_shrink, pad=colorbar_pad,aspect=20)
    
    # if user_vrange or preset_vrange == True:
    cb.ax.set_yticks(cbar_ticks)      
    cb.ax.set_yticklabels(cbar_ticklabels) 
    if user_vrange:
        cb.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0f}" if y in cbar_ticks else ""))
    if auto_vrange:
        cb.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.2e}" if y in cbar_ticks else ""))
    # cb.ax.set_ylabel(cbar_label,fontsize=labelsize)                
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

    plt.title(plot_title)
        
    # Show
    
    plot_toc = time.time()
    print(f'Plotting took {plot_toc - plot_tic:.2f} seconds')

    grand_plot_toc = time.time()
    print(f'The whole plotting procedure took {grand_plot_toc - grand_plot_tic:.2f} seconds')
    

    if save_plot == True:
        print('save is true')
        plt.savefig(path_to_save_plot+fname+'.png', bbox_inches='tight')
    else:
        print('save is false')
    if show_plot == True:
        plt.show()                    
    
    plt.close(fig)
        
    gc.collect()  # Explicitly trigger garbage collection
    print('#########################################\n\n\n')
    return ds_plot