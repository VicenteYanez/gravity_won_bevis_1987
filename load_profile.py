
import cartopy.crs as ccrs
from cartopy.io.img_tiles import StamenTerrain
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def recta(x, m, c):
    return x*m+c


def load_profile(fname):
    """
    Load the data in the file "fname"

    RETURNS
    xy:     x and y coordinates of the profile (longitude and latitude)
    d   :   Acumulated distance between points in the profile
    z   :   Gravitacional anomaly
    """
    # load data
    data = np.loadtxt(fname, skiprows=4).T

    # perfil representatitvo
    popt, pcov = curve_fit(recta, data[0], data[1])
    xyz = (data[0], recta(data[0], popt[0], popt[1]), data[3])

    # calculates the distance between points
    d = [np.sqrt(((xyz[0][x]-xyz[0][x+1])**2)+((xyz[1][x]-xyz[1][x+1])**2))
         for x in range(len(xyz[1])-1)]
    d = np.hstack(([0], d))

    # calculate the acumulated distnace between points
    for di in range(len(d)-1):
        d[di+1] = d[di] + d[di+1]

    # #################################################################
    # Figures:
    # 01. Map with the profile from the data and the new
    # 02. Topography profile
    # 03. Regional Map with the position of the profile
    # #################################################################
    tiler = StamenTerrain()
    f0 = plt.subplots(figsize=(15, 15))
    grid = plt.GridSpec(2, 3, wspace=0.4, hspace=0.3)
    ax01 = plt.subplot(grid[0, :2],
                       projection=ccrs.UTM(zone=19, southern_hemisphere=True))
    ax01.plot(data[0], data[1], 'bo-', label='data and stations position')
    ax01.plot(xyz[0], xyz[1], 'ro-',
              label='my profile and stations projection')

    ax01_latmin_m = data[1].min() - 500
    ax01_latmax_m = data[1].max() + 500
    ax01_lonmin_m = data[0].min() - 1000
    ax01_lonmax_m = data[0].max() + 1000
    ax01.set_extent((ax01_lonmin_m, ax01_lonmax_m,
                     ax01_latmin_m, ax01_latmax_m),
                    crs=ccrs.UTM(zone=19, southern_hemisphere=True))

    plt.tick_params(bottom=True, top=True, left=True, right=True,
                    labelbottom=True, labeltop=False, labelleft=True,
                    labelright=False)

    ax01.xaxis.set_visible(True)
    ax01.yaxis.set_visible(True)
    ax01.grid(True)
    ax01.set_title('')
    ax01.set_xlabel('meters')
    ax01.set_ylabel('meters')

    ax02 = plt.subplot(grid[1, :2])
    ax02.plot(d, xyz[2], 'k-')
    ax02.plot(d, xyz[2], 'ko')
    ax02.set_xlabel('distance from the start of the profile (meters)')
    ax02.set_ylabel('altitude (meters)')

    ax02.set_title('Topography through the profile')

    ax03 = plt.subplot(grid[:, 2],
                       projection=ccrs.UTM(zone=19, southern_hemisphere=True))
    ax03_latmin_m = data[1].min() - 700000
    ax03_latmax_m = data[1].max() + 700000
    ax03_lonmin_m = data[0].min() - 300000
    ax03_lonmax_m = data[0].max() + 300000
    ax03.set_extent((ax03_lonmin_m, ax03_lonmax_m,
                     ax03_latmin_m, ax03_latmax_m),
                    crs=ccrs.UTM(zone=19, southern_hemisphere=True))
    ax03.plot(data[0][0], data[1][0], 'ko', label='Ubication')
    ax03.coastlines(resolution='10m')
    ax03.add_image(tiler, 6)

    plt.tick_params(bottom=True, top=True, left=True, right=True,
                    labelbottom=True, labeltop=False, labelleft=True,
                    labelright=False)
    ax03.xaxis.set_visible(True)
    ax03.yaxis.set_visible(True)
    ax03.grid(True)

    ax01.legend()
    ax02.legend()
    ax03.legend()

    return f0, xyz, d, data[4]
