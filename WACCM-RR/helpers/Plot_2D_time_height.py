
#!/usr/bin/env python
# coding: utf-8
# %%
'''
Plot_2D_time_height.py
this code is designed for plotting CESM output 
that has been reduced to dimensions of time and height.
TODO: Allow for Pressure and z
'''

### Module import ###
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import calendar
import matplotlib.colors as colors
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
# set the colormap and centre the colorbar

class MidpointNormalize(colors.Normalize):
 
    """
    Normalise the colorbar so that colorbar is centered on a prescribed midpoint value
    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip =False):
        self.midpoint=midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)
        
    def __call__(self, value, clip =None):
        # I'm ignoring masked values and all kinds of edge cases to make a simple example
        x, y=[self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))
    
def Plot_2D_time_height(ds=None, var=None, plot_one='both', z=False, log=False, concentration=False, diff_type=None, 
                       lat_r=[-90,90], y_r=None, nxticks=6, exp=None, qr=None,diffqr=None,
                       cont=True, ncont1=10,ncont2=10,fill=True, nfill=100, diffcont=10,
                       fontsize=10,cont_label_size=15,
                       savefig=False, filename=None,suptitle=None,x_size=6.5,y_size=8,
                       fmt1_cbar=2,fmt2_cbar=2,fmtdiff_cbar=2, override_fmt_cbar=True,format_cbar='e',
                       fmt1_cont=2,fmt2_cont=2,fmtdiff_cont=2, override_fmt_cont=True,format_cont='e',
                       cbar_annotation='',ax0_title='',ax1_title='',diff_title='',
                       path_to_save='',dpi=100, use_options='auto'):
    '''
    NAME:
           Plot_2D_time_height
    PURPOSE:
           2D plot of time vs height 
    INPUTS:
           ds: List of datasets (max 2) to be plotted 
           (must contain T in Kelvin if concentration=True, Z in km if z=true)
           
           var: Variable to plot

           plot_one: Which dataset (if only one is provided) or 'both'
           
           concentration=False (default - only applies to species variables) - no longer used!!
           
           z: False (default)
           log: True (default) - log plot for var
           
           diff_type: None (default), if 2 ds given difference type between ds[1] and ds[0]
           
           lat_r: [-90,90] (default)           
           
           y_r=None, (y axis range - default calculated below)
           
           cont=True (default) - switch cont for all plots
           
           ncont=10 (default) - number of cont on all plots
           
           labelsize=15 (default)
           
           savefig=False (default)
           
           fill=True (default) - plots filled contours on all plots, False plots raw data
           
           nfill=number of filled contours on all plots
           
    NOTES:
    2023-08-14 Mon: MMK - currently titles set to ds0 and ds1.
    
    '''
    print("WARNING - see notes")    
        
        
        
    #========================================================================
    #===== Error check and pass input values to class-accessible values=====
    #========================================================================
    print("Start error check")
    #Check length of ds
    if plot_one == 'both':
        assert len(ds)==2, "ATM must have 2 datasets for ds0 and ds1"
    ## ds check 
    
    ## Dimensions check
    
    ## xarray, lat, height check
    
    ## Assert no diff if size(ds)=1
    
    
    #=== End Error check and pass input values to class-accessible values===
    #========================================================================

    #=======================================================================
    #============================ Initial Setup ============================
    #=======================================================================      
    print("Start initial set-up")
    ## Set-up datasets
    if ds!=None:
        if len(ds)==2:
            ds0=ds[0]
            ds1=ds[1]
            # set_up_plot_data(ds0,ds1) todo
        else:
            ds0=ds[0]
            # set_up_plot_data(ds0) 

    #ds0=ds0[var]
    #ds1=ds1[var]
    
    ## Scale vars and other variable controls
             
    ds0=ds0*exp
    if len(ds) == 2:
        ds1=ds1*exp
    
    ## Compute diffs
    if diff_type!=None:
        if (diff_type=='abs'): 
            ds_diff=ds1 - ds0
            print("Calculating abs ds_diff")
        if (diff_type=='%'): 
            ds_diff=100*(ds1 - ds0)/ds0
        if (diff_type=='frac'):
            ds_diff=ds1/ds0
    else:
        ds_diff = None
        
    # Diff operation removes z if manually calculated.
    # Need to add again.  
    if diff_type!=None and z==True:
        print("\nWARNING: currently using arithmetic mean \n\
        of z between ds0['z'] and d1['z'] as ds_diff['z'] \n ")
        z_diff = 0.5*(ds0['z']+ds1['z'])
        ds_diff['z'] = z_diff.assign_coords(z=z_diff)
    
    
    ## Compute log of var if not T
    if log==True:
        ds0=np.log10(ds0)
        if len(ds) == 2:
            ds1=np.log10(ds1)

    ## Compute var range
    
    # default
    if y_r==None:
        if z==True:
            y_r=[0,150]
        else:
            y_r=[1e3,1e-6]    
            
    if qr==None:    
        if z==True: 
            v0_min=np.min(ds0.where((ds0['z']>=y_r[0]) & (ds0['z']<=y_r[1])))
            v0_max=np.max(ds0.where((ds0['z']>=y_r[0]) & (ds0['z']<=y_r[1])))
            if len(ds) == 2:
                v1_min=np.min(ds1.where((ds1['z']>=y_r[0]) & (ds1['z']<=y_r[1])))
                v1_max=np.max(ds1.where((ds1['z']>=y_r[0]) & (ds1['z']<=y_r[1])))
        else:
            v0_min=np.min(ds0.where((ds0['lev']<=y_r[0]) & (ds0['lev']>=y_r[1])))
            v0_max=np.max(ds0.where((ds0['lev']<=y_r[0]) & (ds0['lev']>=y_r[1])))
            if len(ds) == 2:
                v1_min=np.min(ds1.where((ds1['lev']<=y_r[0]) & (ds1['lev']>=y_r[1])))
                v1_max=np.max(ds1.where((ds1['lev']<=y_r[0]) & (ds1['lev']>=y_r[1])))

        v0_min=v0_min.values
        v0_max=v0_max.values
        if len(ds) == 2:
            v1_min=v1_min.values
            v1_max=v1_max.values  
        
        ## Choose max and min between datasets - set as limits for all plots
        if len(ds) == 2:
            v0_max=max(v0_max,v1_max)
            v0_min=min(v0_min,v1_min)
            v1_max=v0_max
            v1_min=v0_min
            
        
        qr=[]
        qr.append(v0_min)
        qr.append(v0_max)
        qr.append(diffcont)
        
    else:    
        v0_min=qr[0]
        v0_max=qr[1]
        if len(ds) == 2:
            v1_min=qr[0]
            v1_max=qr[1]
    print("v0_min, v0_max", v0_min,v0_max)
    ## Compute diff range
    if diff_type!=None:
        if diffqr==None:
            if z==True:
                diff_min=np.min(ds_diff.where((ds_diff['z']>=y_r[0]) & (ds_diff['z']<=y_r[1])))
                diff_max=np.max(ds_diff.where((ds_diff['z']>=y_r[0]) & (ds_diff['z']<=y_r[1])))
            else:
                diff_min=np.min(ds_diff.where((ds_diff['lev']<=y_r[0]) & (ds_diff['lev']>=y_r[1])))
                diff_max=np.max(ds_diff.where((ds_diff['lev']<=y_r[0]) & (ds_diff['lev']>=y_r[1])))
            diff_min=diff_min.values
            diff_max=diff_max.values
            diffqr=[]
            diffqr.append(diff_min)
            diffqr.append(diff_max)
            diffqr.append(diffcont)
        else:
            diff_min=diffqr[0]
            diff_max=diffqr[1]
           
        
        
    
    ### Debugging Initial Setup
    print("qr0 qr1 qr2", qr[0], qr[1], qr[2], "\n")
    if diff_type!=None:
        print("diff_min diff_max ", diff_min, diff_max,"\n")
    #========================== End Initial Setup ==========================
    #=======================================================================
    
    #=======================================================================
    #=============================== Plot===================================
    #=======================================================================      
    
    print("Start plotting script\n")
    
    ## Set-up axes - todo - currently not working as script requires diff - see set-up
    if len(ds) == 1:
        
        fig, ax=plt.subplots(figsize=(x_size,y_size)) 
        fig.set_dpi(dpi)
        
        if suptitle!=None:
            fig.suptitle(suptitle)
        
        # height coordinate
        if z==True:
            axis_types = {"y":"z", "x":"time"}
        else:
            axis_types = {"y":"lev","yscale":"log", "x":"time"}
        print("Finished setting up axes")
        
        
        ##########################################
        ## ds0 plot
        ##########################################
        
        print("Start plot")
        print(v0_min,v0_max)
        if fill==True:
            plot0=ds0.plot.contourf(ax=ax,
                                    ylim=[y_r[0],y_r[1]],
                                    cmap ="turbo",
                                    vmin=v0_min,vmax=v0_max,levels=nfill,
                                    add_colorbar=False,**axis_types)
        else:
            plot0=ds0.plot(ax=ax,
                           ylim=[y_r[0],y_r[1]],
                           cmap ="turbo",
                           vmin=v0_min,vmax=v0_max,
                           add_colorbar=False,**axis_types)
            
        
        # Create a colorbar
        print("Start colorbar")
        cbar0=plt.colorbar(plot0, ax=ax, aspect=40, pad=0.015)
        # Set cbar ticks
        custom_ticks=np.linspace(qr[0],qr[1],qr[2])
        cbar0.set_ticks(custom_ticks)
        if format_cbar == 'e':
            cbar0.set_ticklabels([f'{tick:.{fmt1_cbar}e}' for tick in custom_ticks])
        else:
            if override_fmt_cbar == True:
                cbar0.set_ticklabels([f'{tick:.{fmt1_cbar}f}' for tick in custom_ticks])
            else:
                cbar0.set_ticklabels([str(tick) for tick in custom_ticks])
        cbar0.ax.tick_params(labelsize=fontsize)
        cbar0.ax.tick_params(which="minor",length=0)
        
        # Plot cont    
        if cont:
            # lined cont
            cs_nonrr=ds0.plot.contour(vmin=v0_min,vmax=v0_max,
                                      ylim=[y_r[0],y_r[1]],
                                      levels=ncont1,
                                      colors="k",
                                      linewidths=1,
                                      ax=ax,
                                      **axis_types
                                     )
            # color label controls
            fmt={}
            if use_options != 'auto':
                for l in ncont1:
                    if format_cont == 'e':
                        fmt[l]=f"{l:.{fmt1_cont}e}"
                    else:
                        if override_fmt_cont == True:
                            fmt[l]=f"{l:.{fmt1_cont}f}"
                        else:
                            fmt[l]=str(l)
            else:
                for l in np.linspace(v0_min,v0_max,ncont1):
                    if format_cont == 'e':
                        fmt[l]=f"{l:.{fmt1_cont}e}"
                    else:
                        if override_fmt_cont == True:
                            fmt[l]=f"{l:.{fmt1_cont}f}"
                        else:
                            fmt[l]=str(l)
    
            clabels=ax.clabel(cs_nonrr, cs_nonrr.levels, inline=True, fmt=fmt, fontsize=cont_label_size,inline_spacing=5)
            [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0)) for txt in clabels]
        print("Finish plot")
        
        ##########################################
        ## End ds0 plot
        ##########################################    
        
        ##########################################
        ## Final plot controls
        ##########################################    
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.25)  # Adjust the value as needed
        
        # Axis labels 
        # x label   
        ax.set_xlabel("Month",fontsize=fontsize)
        
        # ylabel 
        if z==True:
            ylabel="z (km)"
        else:
            ylabel="Pressure (hPa)"
            
        ax.set_ylabel(ylabel,fontsize=fontsize)
        
        # Axis ticks
        # x ticks
        time_values0=ds0.time.values
        
        ax.set_xticks(time_values0)
        
        tick_labels=['J','F','M','A','M','J','J','A','S','O','N','D']
        
        ax.set_xticklabels(tick_labels,rotation=0)

        # y ticks
        if z==False:
            ax.tick_params(which="minor",length=3)
        else:
            ax.tick_params(which="minor",length=0)
            
        # Global tick params
        ax.tick_params(which="major",labelsize=fontsize,width=1,length=6,direction="out",right=False)

        # Plot titles
        if plot_one == 'RR':
            ax.set_title(ax1_title,fontsize=fontsize)
        else:
            ax.set_title(ax0_title,fontsize=fontsize)
        
        # Colorbar titles
        cbar0.ax.set_title(cbar_annotation,fontsize=fontsize-2,pad=35)
           
        fig.tight_layout(pad=0.1)
    #========================================================
    # END PLOTTING FOR ONLY ONE DATASET
    #========================================================
    else:
        if diff_type!=None:
            icols=3
        else:
            icols=len(ds)  
            
        fig, ax=plt.subplots(nrows=1,ncols=icols, figsize=(x_size*icols,y_size)) 
        fig.set_dpi(dpi)
        
        if suptitle!=None:
            fig.suptitle(suptitle)
        
        # height coordinate
        if z==True:
            axis_types = {"y":"z", "x":"time"}
        else:
            axis_types = {"y":"lev","yscale":"log", "x":"time"}
        print("Finished setting up axes")
        
        
        ##########################################
        ## ds0 plot
        ##########################################
        
        print("Start ds0 plot")
        print(v0_min,v0_max)
        if fill==True:
            plot0=ds0.plot.contourf(ax=ax[0],
                                    ylim=[y_r[0],y_r[1]],
                                    cmap ="turbo",
                                    vmin=v1_min,vmax=v1_max,levels=nfill,
                                    add_colorbar=False,**axis_types)
        else:
            plot0=ds0.plot(ax=ax[0],
                           ylim=[y_r[0],y_r[1]],
                           cmap ="turbo",
                           vmin=v1_min,vmax=v1_max,
                           add_colorbar=False,**axis_types)
            
        
        # Create a colorbar
        print("Start ds0 colorbar")
        cbar0=plt.colorbar(plot0, ax=ax[0], aspect=40, pad=0.015)
        # Set cbar ticks
        custom_ticks=np.linspace(qr[0],qr[1],qr[2])
        cbar0.set_ticks(custom_ticks)
        if format_cbar == 'e':
            cbar0.set_ticklabels([f'{tick:.{fmt1_cbar}e}' for tick in custom_ticks])
        else:
            if override_fmt_cbar == True:
                cbar0.set_ticklabels([f'{tick:.{fmt1_cbar}f}' for tick in custom_ticks])
            else:
                cbar0.set_ticklabels([str(tick) for tick in custom_ticks])
        cbar0.ax.tick_params(labelsize=fontsize)
        cbar0.ax.tick_params(which="minor",length=0)
        
        # Plot cont    
        if cont:
            # lined cont
            cs_nonrr=ds0.plot.contour(vmin=v0_min,vmax=v0_max,
                                      ylim=[y_r[0],y_r[1]],
                                      levels=ncont1,
                                      colors="k",
                                      linewidths=1,
                                      ax=ax[0],
                                      **axis_types
                                     )
            # color label controls
            fmt={}
            if use_options != 'auto':
                for l in ncont1:
                    if format_cont == 'e':
                        fmt[l]=f"{l:.{fmt1_cont}e}"
                    else:
                        if override_fmt_cont == True:
                            fmt[l]=f"{l:.{fmt1_cont}f}"
                        else:
                            fmt[l]=str(l)
            else:
                for l in np.linspace(v0_min,v0_max,ncont1):
                    if format_cont == 'e':
                        fmt[l]=f"{l:.{fmt1_cont}e}"
                    else:
                        if override_fmt_cont == True:
                            fmt[l]=f"{l:.{fmt1_cont}f}"
                        else:
                            fmt[l]=str(l)
    
            clabels=ax[0].clabel(cs_nonrr, cs_nonrr.levels, inline=True, fmt=fmt, fontsize=cont_label_size,inline_spacing=5)
            [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0)) for txt in clabels]
        print("Finish ds0 plot")
        
        ##########################################
        ## End ds0 plot
        ##########################################    
        
        
        ##########################################
        ## ds1 plot
        ########################################## 
        if fill==True:
            plot1=ds1.plot.contourf(ax=ax[1],
                                    ylim=[y_r[0],y_r[1]],
                                    cmap ="turbo",
                                    vmin=v1_min,vmax=v1_max,levels=nfill,
                                    add_colorbar=False,**axis_types)
        else:
            plot1=ds1.plot(ax=ax[1],
                           ylim=[y_r[0],y_r[1]],
                           cmap ="turbo",
                           vmin=v1_min,vmax=v1_max,
                           add_colorbar=False,**axis_types)
        # Create a colorbar
        cbar1=plt.colorbar(plot1, ax=ax[1], aspect=40,pad = 0.015)
        # Set cbar ticks
        custom_ticks=np.linspace(qr[0],qr[1],qr[2])
        cbar1.set_ticks(custom_ticks)
        if format_cbar == 'e':
            cbar1.set_ticklabels([f'{tick:.{fmt2_cbar}e}' for tick in custom_ticks])
        else:
            if override_fmt_cbar == True:
                cbar1.set_ticklabels([f'{tick:.{fmt2_cbar}f}' for tick in custom_ticks])
            else:
                cbar1.set_ticklabels([str(tick) for tick in custom_ticks])
        cbar1.ax.tick_params(labelsize=fontsize)    
        cbar1.ax.tick_params(which="minor",length=0)
        
        # Plot cont
        if cont:
            # lined cont
            cs_rr=ds1.plot.contour(vmin=v1_min,vmax=v1_max,
                                   ylim=[y_r[0],y_r[1]],
                                   levels=ncont2,
                                   colors="k",
                                   linewidths=1,
                                   ax=ax[1],
                                   **axis_types)
            # color label controls
            fmt={}
            for l in ncont2:
                if format_cont == 'e':
                    fmt[l]=f"{l:.{fmt1_cont}e}"
                else:
                    if override_fmt_cont == True:
                        fmt[l]=f"{l:.{fmt2_cont}f}"
                    else:
                        fmt[l]=str(l)
    
      
            clabels=ax[1].clabel(cs_rr, cs_rr.levels, inline=True, fmt=fmt, fontsize=cont_label_size, inline_spacing=15)
            [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0)) for txt in clabels]
        ##########################################
        ## End ds1 plot
        ##########################################
        
        
        ##########################################
        ## diff plot
        ##########################################
        if diff_type!=None:
            if diff_type=="%" or diff_type=="abs": 
                norm=MidpointNormalize(midpoint=0)
            if diff_type=="frac": 
                norm= MidpointNormalize(midpoint=1) 
            if fill==True:
                plot2=ds_diff.plot.contourf(ax=ax[2],
                                            ylim=[y_r[0],y_r[1]],
                                            cmap ="seismic",
                                            vmin=diff_min,vmax=diff_max,
                                            levels=nfill,
                                            add_colorbar=False,
                                            norm=norm,
                                            **axis_types)
            else:
                plot2=ds_diff.plot(ax=ax[2],
                                   ylim=[y_r[0],y_r[1]],
                                   cmap ="seismic",
                                   vmin=diff_min,vmax=diff_max,
                                   add_colorbar=False,
                                   norm=norm,
                                   **axis_types)
            # Create a colorbar
            cbar2=plt.colorbar(plot2, ax=ax[2],aspect=40, pad = 0.015)
            # Set cbar ticks
            custom_ticks=np.linspace(diffqr[0],diffqr[1],diffqr[2])
            cbar2.set_ticks(custom_ticks)
            if override_fmt_cbar == True:
                cbar2.set_ticklabels([f'{tick:.{fmtdiff_cbar}f}' for tick in custom_ticks])
            else:
                cbar2.set_ticklabels([str(tick) for tick in custom_ticks])   
            cbar2.ax.tick_params(labelsize=fontsize)
            cbar2.ax.tick_params(which="minor",length=0)
            # Plot cont
            if cont:
                # lined cont
                cs_diff=ds_diff.plot.contour(vmin=diff_min,vmax=diff_max,
                                             ylim=[y_r[0],y_r[1]],
                                             levels=diffcont,
                                             colors="k",
                                             linewidths=1,
                                             ax=ax[2],**axis_types,norm=norm)
                # color label controls
                fmt={}
                for l in diffcont:
                    if override_fmt_cont == True:
                        fmt[l]=f"{l:.{fmtdiff_cont}f}"
                    else:
                        fmt[l]=str(l)
                clabels=ax[2].clabel(cs_diff, cs_diff.levels, inline=True, fmt=fmt, fontsize=cont_label_size,inline_spacing=15)
                [txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=0)) for txt in clabels]
    
                # Plot contour at 0 value    
                # cs_diff_0=ds_diff.plot.contour(vmin=0,vmax=0,
                #                                ylim=[y_r[0],y_r[1]],
                #                                levels=1,
                #                                colors="white",
                #                                linewidths=2,
                #                                ax=ax[2],
                #                                **axis_types)
    
                # # color label controls
                # fmt={}
                # for l in cs_diff_0.levels:
                #     fmt[l]=f"{l:.0f}" 
                # clabels_0=ax[2].clabel(cs_diff_0, cs_diff_0.levels, inline=True, fmt=fmt, fontsize=cont_label_size)
                # [txt.set_bbox(dict(facecolor='k', edgecolor='none', pad=0)) for txt in clabels_0]
        ##########################################
        ## End diff plot
        ##########################################
    
        
        ##########################################
        ## Final plot controls
        ##########################################    
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.25)  # Adjust the value as needed
        
        # Axis labels 
        # x label   
        ax[0].set_xlabel("Month",fontsize=fontsize)
        ax[1].set_xlabel("Month",fontsize=fontsize)
        if diff_type!=None: ax[2].set_xlabel("Month",fontsize=fontsize)
        
        # ylabel 
        if z==True:
            ylabel="z (km)"
        else:
            ylabel="Pressure (hPa)"
            
        ax[0].set_ylabel(ylabel,fontsize=fontsize)
        ax[1].set_ylabel("",fontsize=fontsize)
        if diff_type!=None: ax[2].set_ylabel("",fontsize=fontsize)
        
        # Axis ticks
        # x ticks
        time_values0=ds0.time.values
        time_values1=ds1.time.values
        
        ax[0].set_xticks(time_values0)
        ax[1].set_xticks(time_values1)
        
        if diff_type!=None: ax[2].set_xticks(time_values1)
        
        tick_labels=['J','F','M','A','M','J','J','A','S','O','N','D']
        
        ax[0].set_xticklabels(tick_labels,rotation=0)
        ax[1].set_xticklabels(tick_labels,rotation=0)    
        if diff_type!=None: ax[2].set_xticklabels(tick_labels,rotation=0)
        # y ticks
        if z==False:
            ax[0].tick_params(which="minor",length=3)
            ax[1].tick_params(which="minor",length=3)
        else:
            ax[0].tick_params(which="minor",length=0)
            ax[1].tick_params(which="minor",length=0)
            
        # diff ticks
        if diff_type!=None: 
            ax[2].tick_params(which="major",labelsize=fontsize,width=1,length=6,direction="out",right=False)
            if z==False:
                ax[2].tick_params(which="minor",length=3)
            else:
                ax[2].tick_params(which="minor",length=0)
        
        # Global tick params
        ax[0].tick_params(which="major",labelsize=fontsize,width=1,length=6,direction="out",right=False)
        ax[1].tick_params(which="major",labelsize=fontsize,width=1,length=6,direction="out",right=False)
        if diff_type!=None:
            ax[2].tick_params(which="major",labelsize=fontsize,width=1,length=6,direction="out",right=False)
    
    
        # Plot titles
        ax[0].set_title(ax0_title,fontsize=fontsize)
        ax[1].set_title(ax1_title,fontsize=fontsize)
        if diff_type!=None:
            ax[2].set_title(diff_title,fontsize=fontsize)
        
        # Colorbar titles
        cbar0.ax.set_title(cbar_annotation,fontsize=fontsize-2,pad=35)
        cbar1.ax.set_title(cbar_annotation,fontsize=fontsize-2,pad=35)
           
        fig.tight_layout(pad=0.1)
        
    # savefig=False
    if savefig:
        plt.savefig(path_to_save+ filename + ".png",dpi=dpi)
        
    return ds_diff
    #============================= End Plot================================
    #=======================================================================
