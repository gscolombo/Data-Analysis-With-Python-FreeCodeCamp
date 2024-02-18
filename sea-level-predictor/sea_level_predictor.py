import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df_sl = pd.read_csv('./epa-sea-level.csv', index_col='Year')
    years = df_sl.index
    sea_level = df_sl['CSIRO Adjusted Sea Level']

    # Create scatter plot
    cp = np.linspace(sea_level.min(), sea_level.max(), sea_level.size)
    plt.scatter(years, sea_level, abs(sea_level), cmap=plt.colormaps.get_cmap('winter'), c=[n for n in cp])
    
    # Create first line of best fit
    line = lambda x, a, b: x*a + b
    linregress_result = linregress(years, sea_level)
    slope, intercept = linregress_result.slope, linregress_result.intercept
    years_to_2050 = np.array(years.to_list() + [y for y in range(years[-1] + 1, 2051)])
    plt.plot(years_to_2050, line(years_to_2050, slope, intercept), color='red')    

    # Create second line of best fit
    years_since_2000, sea_level_since_2000 = df_sl.loc[2000:].index, df_sl.loc[2000:]['CSIRO Adjusted Sea Level']
    linregress_result = linregress(years_since_2000, sea_level_since_2000)
    slope, intercept = linregress_result.slope, linregress_result.intercept
    years_to_2050 = np.array(years_since_2000.to_list() + [y for y in range(years_since_2000[-1] + 1, 2051)])
    plt.plot(years_to_2050, line(years_to_2050, slope, intercept), color='orange')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()