import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import sys


def WoodsFunction(x, a, b, c, d):
    return a/(x+b)+c*x+d


def fit_Wood( x_array, y_array ):

        popt, pcov = curve_fit(WoodsFunction, x_array, y_array, p0=[10., 15., -1.5e-3, 2.])
        x = np.linspace(min(x_array), max(x_array), len(x_array)*100 )
        y = WoodsFunction( x, *popt )
        return x, y, popt, np.sqrt(np.diag(pcov))


def FitWoodsToBandFile( bandFile ):


    #read in band file
    bandlines = [line.rstrip() for line in open(bandFile)]

    binCenters, means, widths, widths2 = [], [], [], []
    print( "Fitting the Woods Function to %s" % bandFile )
    print( "---> A/(X+B) + C*X + D " )
    
    try:
       for i in range(1, len(bandlines)):
            info = bandlines[i].split()
            binCenters.append( float( info[0] ) )
            means.append( float( info[1] ) )
            width_lo = float( info[2][1:] )
            width_hi = float( info[3][:-1] )
            widths.append( width_lo )
            widths2.append( width_hi )

       plt.plot( binCenters, means, 'k', label='Resultant Band' )
       plt.plot( binCenters, np.array(means)+np.array(widths2), 'k--')
       plt.plot( binCenters, np.array(means)-np.array(widths), 'k--')
       plt.xlabel(r'S1$_c$ [phd]', fontsize=18, family='serif')
       fitX_mean, fitY_mean, meanParams, meanParamErrs = fit_Wood( binCenters, means )
       plt.plot( fitX_mean, fitY_mean, 'r', label='Woods Function Fit' )
       print( 'The Woods Function Fit Parameters for the Band Mean are: ', meanParams )
       fitX_lo, fitY_lo, loParams, loParamErrs = fit_Wood( binCenters, np.array(means)-np.array(widths) )
       plt.plot( fitX_lo, fitY_lo, 'r--' )
       print( 'The Woods Function Fit Parameters for the Lower-Width Line are: ', loParams )
       fitX_hi, fitY_hi, hiParams, hiParamErrs = fit_Wood(binCenters, np.array(means)+np.array(widths) )
       plt.plot( fitX_hi, fitY_hi, 'r--' )
       print( 'The Woods Function Fit Parameters for the Higher-Width Line are: ', hiParams )

    except:
        for i in range(1, len(bandlines)):
            info = bandlines[i].split()
            binCenters.append( float( info[0] ) )
            means.append( float( info[1] ) )
            widths.append( float( info[2] ) )

        plt.plot( binCenters, means, 'k', label='Resultant Band' )
        plt.plot( binCenters, np.array(means)+np.array(widths), 'k--')
        plt.plot( binCenters, np.array(means)-np.array(widths), 'k--')
        plt.xlabel(r'S1$_c$ [phd]', fontsize=18, family='serif')
        fitX_mean, fitY_mean, meanParams, meanParamErrs = fit_Wood( binCenters, means )
        plt.plot( fitX_mean, fitY_mean, 'r', label='Woods Function Fit' )
        print( 'The Woods Function Fit Parameters for the Band Mean are: ', meanParams )
        fitX_lo, fitY_lo, loParams, loParamErrs = fit_Wood( binCenters, np.array(means)-np.array(widths[:,0]) )
        plt.plot( fitX_lo, fitY_lo, 'r--' )
        print( 'The Woods Function Fit Parameters for the Lower-Width Line are: ', loParams )
        fitX_hi, fitY_hi, hiParams, hiParamErrs = fit_Wood(binCenters, np.array(means)+np.array(widths[:,1]) )
        plt.plot( fitX_hi, fitY_hi, 'r--' )
        print( 'The Woods Function Fit Parameters for the Higher-Width Line are: ', hiParams )
    
    plt.legend(loc='best' )
    plt.show()
   


def main():
    try: 
        bandFile = sys.argv[1]
    except:
        print("This script takes only one argument -- the path to a band file from BandMaker\n")
        return 1

    FitWoodsToBandFile( bandFile )
    return 0

if __name__ == "__main__":
         main()



