import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


### Function to Create Colormap
def custom_div_cmap(numcolors=256, name='custom_div_cmap',colors=['black','dimgrey','lightgrey','white','palegreen','forestgreen', 'darkgreen']):
    """ Create a custom colormap
 	Colors can be specified in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
 	-> https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    """
    cmap = LinearSegmentedColormap.from_list(name=name, colors=colors, N=numcolors)
    return cmap


fig, axs = plt.subplots(figsize=(15,15), sharex=True)
plt.axis('off')
files = sorted(glob('day*.json'))
for idx, file in enumerate(files):
    year = int(file[-9:-5])
    #year=2011
    #read data
    data = pd.read_json(file)
    #create list of dates available (important for current year)
    min_day = data.values[1,:][11,][0][0]
    print(min_day)
    max_day = data.values[1,:][11,][-1][0]
    date = pd.period_range(pd.Timestamp(day=int(min_day[0:2]),month=int(min_day[3:5]),year=year), pd.Timestamp(day=int(max_day[0:2]),month=int(max_day[3:5]),year=year))
    #create pandas Data Frames of needed data from conventional sources and solar/wind
    wasser_data = pd.DataFrame(data.values[1,:][11,])[1]
    biomasse_data = pd.DataFrame(data.values[2,:][11,])[1]
    kernenergie_data = pd.DataFrame(data.values[3,:][11,])[1]
    braunkohle_data = pd.DataFrame(data.values[4,:][11,])[1]
    steinkohle_data = pd.DataFrame(data.values[5,:][11,])[1]
    oel_data = pd.DataFrame(data.values[6,:][11,])[1]
    gas_data = pd.DataFrame(data.values[7,:][11,])[1]
    andere_data = pd.DataFrame(data.values[8,:][11,])[1]
    wind_data = pd.DataFrame(data.values[9,:][11,])[1]
    solar_data = pd.DataFrame(data.values[10,:][11,])[1]

    #sum of renewable energy and conventional energy
    renewable_data = wind_data+solar_data+wasser_data+ biomasse_data
    conventional_data = kernenergie_data+braunkohle_data+steinkohle_data+oel_data+gas_data+andere_data
    #create common dataframe
    energyprod = pd.concat([renewable_data, conventional_data], axis=1, keys = ['renewable','conventional'])
    #turn conventional energy into negative value (for later visualisation)
    energyprod.loc[(energyprod['conventional'] > energyprod['renewable']), 'max_values'] = energyprod['conventional']*(-1)
    energyprod.loc[(energyprod['conventional'] <= energyprod['renewable']), 'max_values'] = energyprod['renewable']
    #extend data frame with missing days of current year
    energyprod = energyprod.set_index(date)
    date_dummy =  pd.period_range(pd.Timestamp(day=1,month=1,year=year), pd.Timestamp(day=31,month=12,year=year))
    energyprod = energyprod.reindex(date_dummy, fill_value=np.nan)
    #turn data indo numpy array
    energy_array = energyprod['max_values'].values
    #determine vmin and vmax for plot in TWh (energyproduction varies for each day but 1.5 is a value that is rarely reached)
    vmin = -1.7  #TWh per day
    vmax = 1.7 #TWh per day
    #create color map
    cmap = custom_div_cmap()
    #stack numpy array to plot with imshow
    stacked_energy = np.stack((energy_array, energy_array))

    ###PLotting each year into subplots
    fig.add_subplot(10, 1, idx+1)
    plt.imshow(stacked_energy, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax, interpolation='none')
    plt.axis('off')
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    t = plt.text(320,1,s=year, fontsize=30, alpha=1, weight = 'bold')
    t.set_bbox(dict(facecolor='w', alpha=0.5, edgecolor='w'))

plt.savefig('Energystripes_2011-2020.jpg', bbox_inches = 'tight', pad_inches = 0, dpi=150)
