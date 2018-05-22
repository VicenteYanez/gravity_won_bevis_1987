
import numpy as np

"""
# #########################################################################
Documentacion original de Won and Bevis 1987
# #########################################################################
subrutine gz_poly(xs, zs, xv, zv, den)

Computes the vertical component of gravitational acceleration fue to a polygon
in a two-dimensional space (X, Z), or equivalently, fue to an infinitely-long
polygonal cylinder strinkin in the y-direction in a three-dimensional space
(X, Y, Z)

ARGUMENTS
    xs, zs  Vecters containing the station coordinates (first station is at
            [xs[0], zs[0], etc])
    xv, zv  Vectors containing the coordinates of the polygon vertices in
            clockwise sequence
    den     the polygon density (kg/m^3)

RETURNS
    grav_z  vector containing z-component of gravitational acceleration due to
            the polygon at each of the stations (mGal)

SIGN CONVENTION
The z-axis is positive downwards, the x-axis is positive to the right.
"""


def gz_poly(xs, zs, xv, zv, den):
    # variables
    G = 2.67408*10**-11  # m^3/(kg*s^2)
    twogro = 2*G*den
    nvert = len(xv)

    # variable to save the data
    gz = []

    # loop in the stations coordinates
    for stationx, stationz in zip(xs, zs):
        gz_i = 0  # initial value of gz_i

        # loop in the polygon vertices
        for j in range(nvert-1):
            # vertice 1 and vertice 2
            xvert1 = xv[j] - stationx  # put i-station on (0, 0)
            zvert1 = zv[j] - stationz
            xvert2 = xv[j+1] - stationx
            zvert2 = zv[j+1] - stationz

            r2 = np.sqrt(xvert2**2+zvert2**2)
            r1 = np.sqrt(xvert1**2+zvert1**2)

            # theta values
            theta1 = np.arctan2(zvert1, xvert1)
            theta2 = np.arctan2(zvert2, xvert2)

            # Conditional for the three cases in Won and Bevis 1987
            # case 1
            # conditional for theta values if z1 different sign than z2
            if (zvert1 < 0 and zvert2 > 0) or (zvert1 > 0 and zvert2 < 0):
                if xvert1*zvert2 < xvert2*zvert1 and zvert2 >= 0:
                    theta1 = theta1 + 2*np.pi
                elif xvert1*zvert2 > xvert2*zvert1 and zvert1 >= 0:
                    theta2 = theta2 + 2*np.pi
                elif xvert1*zvert2 == xvert2*zvert1:
                    continue
            # case 2
            if (xvert1 == 0 and zvert1 == 0) or (xvert2 == 0 and zvert2 == 0):
                continue
            # case 3
            if xvert1 == xvert2:
                gz_i += xvert1*np.log(r2/r1)
                continue

            # if all the cases have passed
            A = (xvert2-xvert1)*(xvert1*zvert2-xvert2*zvert1)/(
                ((xvert2-xvert1)**2)+(zvert2-zvert1)**2)
            B = (zvert2 - zvert1)/(xvert2-xvert1)
            gz_i += A*(theta1 - theta2 + B*np.log(r2/r1))

        gz.append(gz_i)
    # multiply element-wise the values of gz with 2*G*rho
    gz = np.array(gz)*twogro*10**5  # 10^5 to transform it to mgal

    return gz
