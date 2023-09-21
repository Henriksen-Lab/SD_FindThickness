import sys, os, time
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit
import numpy as np

fontsize = 12
# Font
font = {'family': "Helvetica",
        "weight": 'normal',
        "size": fontsize}
mpl.rc("font", **font)
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['mathtext.bf'] = 'sans:italic:bold'
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['figure.autolayout'] = True

# Linewidth
linewidth = 0.5
mpl.rcParams['axes.linewidth'] = linewidth
mpl.rcParams['axes.labelweight'] = 'normal'
mpl.rcParams['lines.linewidth'] = linewidth
mpl.rcParams['xtick.major.width'] = linewidth
mpl.rcParams['xtick.major.size'] = 3
mpl.rcParams['ytick.major.width'] = linewidth
mpl.rcParams['ytick.major.size'] = 3
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['axes.formatter.limits'] = -2, 4
mpl.rcParams['axes.formatter.useoffset'] = False
mpl.rcParams['axes.spines.top'] = True
mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['axes.spines.right'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['axes.xmargin'] = 0.0 # x margin.  See `axes.Axes.margins`
mpl.rcParams['axes.ymargin'] = 0.1  # y margin.  See `axes.Axes.margins`
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.borderpad'] = 0
# layout
fig_size = np.asarray([12, 8.5])
fig_size = fig_size / 2.54


folder_path = r'/Users/chellybone/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/wustl/HLab/HLab_git/SD_FindThickness/AFM_measurements/hBN_50X'

def get_color_cycle(NUM_COLORS, cmap='twilight_shifted'):
    cm = plt.get_cmap(cmap)
    custom_cycler = [cm(1. * x / NUM_COLORS) for x in range(NUM_COLORS)]
    return custom_cycler
i = 0
x = []
y = []

fig_size = np.asarray([12, 8])
fig_size = fig_size / 2.54
fg = plt.figure(figsize=fig_size)
for root, dirs, files in os.walk(folder_path, topdown=False):
    n = len(files)
    for name in files:
        real_t_list = []
        wavelength_list = []
        if ".DS_Store" not in name and ".png" not in name and "Cali" not in name:
            file_path = os.path.join(folder_path,name)
            with open(file_path, 'rb') as f:
                measurement = pickle.load(f)
            for point in measurement['Point_info'].keys():
                data = measurement['Point_info'][point]
                try:
                    real_t = float(data['real_t'])
                    wavelength = float(data['wavelength'])
                except:
                    break
                wavelength_list += [wavelength]
                real_t_list += [real_t]
#           wavelength_list = np.array(wavelength_list) - min(wavelength_list)
            wavelength_list = np.array(wavelength_list)
            real_t_list = np.array(real_t_list)
        plt.scatter(wavelength_list,real_t_list, color = get_color_cycle(n)[i])
        i += 1
        x.extend(wavelength_list)
        y.extend(real_t_list)
x = np.array(x)
y = np.array(y)
print(x,y)
def function(x,a,b,c):
    return a*x**2 + b*x +c
popt, pcov = curve_fit(function, x, y)
x_fit = np.linspace(min(x),max(x),1001)
y_fit = function(x_fit, *popt)
yerr = np.std(y-function(x, *popt))
plt.plot(x_fit,y_fit,ls='--')
plt.fill_between(x_fit, y_fit - yerr, y_fit + yerr, alpha=0.4, ls='--')
plt.xlim(min(x)-10,max(x)+10)
plt.ylim(min(y)-10,max(y)+10)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Measured length (nm)')
title = f'091923 fit: {popt[0]:.2e} x^2+{popt[1]:.2e} x+{popt[2]:.2e}\n yerr={yerr:.2e}'
#plt.title(title)
dataToSave = {}
dataToSave.update({'popt': popt})
dataToSave.update({'sigma': yerr})
filename = 'Cali_' + 'hBN_on300nmSiO2_50X'
file_path = os.path.join(folder_path, filename)
with open(file_path,'wb') as f:
    pickle.dump(dataToSave, f)
plt.tight_layout()
fig_name = filename + '.png'
fig_path = os.path.join(folder_path, fig_name)
plt.savefig(fig_path, transparent=True, dpi=600)
plt.show()

