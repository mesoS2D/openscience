import xarray as xr 
import numpy as np
from numpy.fft import fft2
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import time


def fft2_of_ds(ds_for_fft,dr_resolution):
    
    fft = fft2(ds_for_fft.values)
    print('performed fft')
    freq_x = np.fft.fftfreq(len(ds_for_fft.lat),dr_resolution)
    freq_y = freq_x
    ds_fft = xr.DataArray(np.abs(fft)**2, dims=['ly','lx'], coords={'ly':freq_y,'lx':freq_x})
    
    ds_fft.loc[{'lx':0,'ly':0}] = 0 # Remove DC component
    ds_fft_sorted = ds_fft.sortby(ds_fft.lx).sortby(ds_fft.ly)
    return ds_fft_sorted

def horizontal_wavenumber_spectrum_1d(ds):
    ds_fft_sorted_sel = ds

    # Define radial bins
    L = np.sqrt(ds_fft_sorted_sel.ly**2 + ds_fft_sorted_sel.lx**2).values.flatten() # ly and lx need to be ordered like this, so the order of the list is the same as ds_fft_sorted_sel.values.flatten() below
    l_bins = np.arange(0, np.max(L) + np.diff(ds_fft_sorted_sel.lx)[0], np.diff(ds_fft_sorted_sel.lx)[0])  # Adjust bin spacing as needed - NOTE THIS ACTS AS BIN EDGES IN np.digitize

    # Radial binning
    bin_indices = np.digitize(L, l_bins) # Find which bin each point belongs to

    # # Print diagnostics
    # print(np.max(l_bins)) 
    # print(np.diff(l_bins)[0])
    # print(len(l_bins))
    
    # Compute binned power spectrum
    print('Computing binned 1D horizontal wavenumber power spectrum')
    tic = time.time()
    binned_power = np.zeros(len(l_bins)-1) # l_bins is the number of bin edges, we want bin centers = nr edges - 1, and binned power to align 
    bin_counts = np.zeros(len(l_bins)-1)

    for i in range(len(L)):
        idx = bin_indices[i]
        binned_power[idx-1] += ds_fft_sorted_sel.values.flatten()[i] # min index in bin_indices starts at 1
        bin_counts[idx-1] += 1

    print('Binned power spectrum computed')
    toc = time.time()
    print(f'That took: {toc-tic:.2f} seconds')
    
    # Normalize by number of elements per bin to get average power
    binned_power /= np.maximum(bin_counts, 1)  # Avoid division by zero
    
    bin_centers = l_bins[1:] - np.diff(l_bins)[0] / 2 # Center of each bin
    
    print('len(binned_power)',len(binned_power))
    print('len(bin_centers)',len(bin_centers))
    
    # Convert bin values to cycles per meter
    deg_to_m = 6400e3*2*np.pi/360
    cyc_p_m = bin_centers/deg_to_m
    
    # Create DataArray for the 1D spectrum
    ds_1d_spec = xr.DataArray(binned_power, dims=['h'], coords={'h': bin_centers})  
    ds_1d_spec['h'].attrs['name'] = 'Horizontal Wavenumber (cycles/meter)'
    
    # Plot the 1D spectrum
    # fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    # ds_1d_spec.plot(yscale='log',xscale='log',ax=ax)
    # plt.xlabel('Horizontal Wavenumber (cyc/m)')
    # plt.ylabel('Power')
    
    # plt.show()
    # fig.clear()
    # plt.close(fig)
    # del(fig)
    # del(ax)
    
    return ds_1d_spec
    

def plot_spec(ds_for_fft,var, ds_spec, height,save_spec=False):

    fig = plt.figure(figsize=(16,5),dpi=100)
        
    #
    # Plot map
    #
    ax0 = fig.add_subplot(1,2,1,projection=ccrs.PlateCarree())
    # fig, ax1 = plt.subplots(ncols=1,figsize=(3,3),dpi=150)
    
    # r = np.sqrt(ds_spec.lx**2 + ds_spec.ly**2)
    # ds_spec = ds_spec.where(r>0.4,other=1e-10)
    if var in ['T','KE','ELECDEN']:
        limLmap = np.sort(ds_for_fft.values.flatten())[int(0.7*len(ds_for_fft.values.flatten()))]
    else:
        limLmap=None
    p0 = ds_for_fft.plot(ax=ax0, add_colorbar=False,vmin=limLmap, cmap='seismic')
    ax0.coastlines()
    ax0.gridlines(draw_labels=True,linewidth=0.5,alpha=0.5)  
    if var in ['U','V','w']:
        units = 'm/s'  
    if var == 'T':
        units = 'K'
    if var == 'ELECDEN':
        units = 'cm$^{-3}$'    
    if var == 'KE':
        units = 'J/g(?)'
    c = plt.colorbar(p0,pad=0.15)
    c.ax.set_ylabel(f'{var}'+' (' + units +')')
    
    # 
    # Plot spectrum
    # 
    
    ds_spec = np.log10(ds_spec)
    limL = np.sort(ds_spec.values.flatten())[int(0.2*len(ds_spec.values.flatten()))] 
    limU = np.sort(ds_spec.values.flatten())[int(0.95*len(ds_spec.values.flatten()))] + 3
    
    print(f'Limits chosen for spectrum plot: {limL:2f} {limU:.2f}')
    
    ax1 = fig.add_subplot(1,2,2)
    p = ds_spec.plot(ax=ax1, add_colorbar=False, cmap='magma')#, vmin=limL, vmax=limU)
    time = ds_for_fft.time.values.item().strftime("%Y-%m-%d_%H:%M:%S")
    
    ax0.set_title(f'{var} at {height} km at time {time}')

    # ax1.set_xticks(np.arange(-5,6,1))
    # ax1.set_xticklabels(np.concatenate((np.arange(5,0,-1), np.arange(0,6,1))))
    # ax1.set_yticks(np.arange(-5,6,1))
    # ax1.set_yticklabels(np.concatenate((np.arange(5,0,-1), np.arange(0,6,1))))
    
    xlimL = -0.5
    xlimU = 0.5
    ylimL = -0.5
    ylimU = 0.5
    
    ax1.set_xlim(xlimL,xlimU)
    ax1.set_ylim(ylimL,ylimU)


    ax1.set_xlabel(r'k/2$\pi$ ($1/\lambda_x$ cyc/deg)')
    ax1.set_ylabel(r'l/2$\pi$ ($1/\lambda_y$ cyc/deg)')
    
    
    # ax1.annotate('N', xy=(0.48, 1.05), xycoords='axes fraction', fontsize=15,color='red')
    # ax1.annotate('S', xy=(0.48, 0.02), xycoords='axes fraction', fontsize=15,color='white')
    # ax1.annotate('E', xy=(1.05, 0.48), xycoords='axes fraction', fontsize=15,color='red')
    # ax1.annotate('W', xy=(0.02, 0.48), xycoords='axes fraction', fontsize=15,color='white')

    # ----------------------
    # Plot presentation
    # ----------------------

    # ticks = np.arange(-5,6,1)
    # labels = [f'{x:.1f}' for x in 11/(0.1*np.concatenate((np.arange(5,0,-1), np.arange(0,6,1))))]
    # labels[5] = ''

    # # Right y axis labels
    # ax2 = ax1.twinx()
    # ax2.set_yticks(ticks)
    # ax2.set_yticklabels(labels)
    # ax2.set_ylabel(r'$\lambda_y$ (km)')
    # ax2.set_ylim(ylimL,ylimU)

    # # Top x axis labels
    # ax3 = ax1.twiny()
    # ax3.set_xticks(ticks)
    # ax3.set_xticklabels(labels,rotation=45)
    # ax3.set_xlabel(r'$\lambda_x$ (km)')

    # ax3.set_xlim(xlimL,xlimU)

    # Colorbar 

    cb = plt.colorbar(p,pad=0.15)
    cb.ax.set_ylabel(r'Power')
    # cb.ax.set_ylim(,np.max(ds_spec.where(r>0.4).values)))
    if save_spec: plt.savefig(f'./media/{var}_{time}_{height}km.png',bbox_inches='tight',dpi=100)
    plt.show()
    
    fig.clear()
    plt.close(fig)
    del(fig)
    del(ax1)
    # del(ax2)
    
    # fig, ax1 = plt.subplots(nrows=2, ncols=2,figsize=(5,5),dpi=75)
    
    # ds_pxpy = ds_spec.where((ds_spec.lx>0) & (ds_spec.ly>0),drop=True)
    
    # ds_pxny = ds_spec.where((ds_spec.lx>0) & (ds_spec.ly<0),drop=True)
    # ds_pxny['ly'] = ds_pxny['ly']*-1
    
    # ds_nxpy = ds_spec.where((ds_spec.lx<0) & (ds_spec.ly>0),drop=True)
    # ds_nxpy['lx'] = ds_nxpy['lx']*-1
    
    # ds_nxny = ds_spec.where((ds_spec.lx<0) & (ds_spec.ly<0),drop=True)
    # ds_nxny['lx'] = ds_nxny['lx']*-1
    # ds_nxny['ly'] = ds_nxny['ly']*-1

    # limU = limU+3
    # ds_pxpy.plot(ax=ax1[0,1],add_colorbar=False,cmap='magma',vmin=limL,vmax=limU,xscale='log',yscale='log',xlim=[1.4e-2,5e0],ylim=[1.4e-2,5e0])
    # ds_pxny.plot(ax=ax1[1,1],add_colorbar=False,yscale='log',cmap='magma',xscale='log',vmin=limL,vmax=limU,ylim=[5e0,1.4e-2])
    # ds_nxpy.plot(ax=ax1[0,0],add_colorbar=False,yscale='log',cmap='magma',xscale='log',vmin=limL,vmax=limU,xlim=[5e0,1.4e-2])
    # ds_nxny.plot(ax=ax1[1,0],add_colorbar=False,yscale='log',cmap='magma',xscale='log',vmin=limL,vmax=limU, ylim=[5e0,1.4e-2], xlim=[5e0,1.4e-2])
    # ax1[0,1].annotate(f"min={limL:.2f}\nmax={limU:.2f}",xy=(5.1,2))

    # ax1[0,1].spines['left'].set_visible(False)
    # ax1[0,1].spines['bottom'].set_visible(False)
    # ax1[0,0].spines['bottom'].set_visible(False)
    # ax1[1,0].spines['top'].set_visible(False)
    # ax1[1,1].spines['top'].set_visible(False)
    # ax1[1,1].spines['left'].set_visible(False)

    # ax1[0,1].get_yaxis().set_visible(False)
    # ax1[1,1].get_yaxis().set_visible(False)
    
    # ax1[1,0].set_xlabel('')
    # ax1[1,0].set_ylabel('')
    # ax1[1,1].set_xlabel('')
    
    # ax1[1,1].set_xlabel(r'k/2$\pi$ ($1/\lambda_x$ cyc/deg)',x=0)
    # ax1[0,0].set_ylabel(r'l/2$\pi$ ($1/\lambda_y$ cyc/deg)',y=0)
    # ax1.set_xlabel(r'k/2$\pi$ ($1/\lambda_x$ cyc/deg)')
    # ax1.set_ylabel(r'l/2$\pi$ ($1/\lambda_y$ cyc/deg)')

    # plt.subplots_adjust(wspace=0,hspace=0)
    
    # plt.show()
    # fig.clear()
    # plt.close(fig)
    # del(fig)
    # del(ax1)
    
    return ds_spec
    
