
import json
import os

import matplotlib.pyplot as plt

from fun_grav import gz_poly
from load_profile import load_profile


def main():
    """
    Main code for my implementation of Won and Bevis (1987) gravitational
    anomaly solution due to an n-sided polygon in a two dimensional space

    IMPORTANT
    The last vertice in the modelfile.json should be equal to the first vectice
    """
    # profile
    fname = '{}/perfil.XYZ'.format(os.path.dirname(os.path.abspath(__file__)))
    f0, (xs, ys, zs), d, gz_data = load_profile(fname)
    # remove regional anomaly
    z_regional = (-2.55*10**-3)*d+92
    gz_data = gz_data - z_regional

    # #######################################################################
    # Load, calculate and plot the model ####################################
    # figure ax1: Regional
    # figure ax2: gravitational anomaly
    # figure ax3: polygons
    # ######################################################################
    # load model data
    with open('modelfile.json') as f:
        mydata = json.load(f)
    # define plot objects
    f1, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(15, 8))
    # plot 1
    ax1.set_title('Regional')
    ax1.plot(d, z_regional, label='Regional')
    # loop over all the bodies
    gzt = 0  # variable to save the gravity
    for b in mydata["List of rectangular bodies"]:
        gzt += gz_poly(d, -zs, mydata[b]["xvertice"],
                       mydata[b]["zvertice"],
                       mydata[b]["density"])  # density in kg/m^3
        # anomaly a body with density 2.7 g/cc
        gzt -= gz_poly(d, -zs, mydata[b]["xvertice"],
                       mydata[b]["zvertice"], 2760)  # density in kg/m^3
        # plot model polygons
        ax3.plot(mydata[b]["xvertice"], mydata[b]["zvertice"], 'o-', label=b)
    ax3.plot(d, -zs, 'k-', alpha=0.5, label='Topography')  # topo

    # figure 3 format
    ax3.set_ylabel('m')
    ax3.set_xlabel('m')
    ax3.invert_yaxis()
    ax3.set_title('Model')

    # Plot to compare the data and the model predicted anomaly
    ax2.axhline(0, color='#9D9D9D', linestyle='--', linewidth=0.5)

    # figure 2
    ax2.plot(d, gz_data, 'bo-', label='Data')  # gravitation anomaly data
    ax2.plot(d, gzt, 'ro-', label='Model')  # grav anomaly predicted
    ax2.set_ylabel('mGal')
    ax2.set_title('Gravitational Anomaly')

    # add legend and plot
    ax1.legend()
    ax2.legend()
    ax3.legend()
    plt.show()


main()
