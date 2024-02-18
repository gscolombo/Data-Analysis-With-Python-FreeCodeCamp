import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df[df.map(lambda x, min, max: min <= x <= max, min=df['value'].quantile(0.025), max=df['value'].quantile(0.975))].dropna()


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=[16, 5])
    ax.plot(df.index, df['value'], color='firebrick')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    to_month_name = lambda m: pd.to_datetime(m, format="%m").month_name()
    months = df.index.map(lambda x: x.month).unique().sort_values().map(to_month_name)
    years = df.index.map(lambda x: x.year).unique().sort_values()
    
    fill_na = lambda x, d: d[x] if x in d.index else 0
    
    months_and_years = zip(df.index.map(lambda x: x.year), df.index.map(lambda x: x.month_name()))
    df_bar = pd.Series(df['value'].tolist(), index=pd.MultiIndex.from_tuples(months_and_years, names=['year', 'month']), name='value')
    df_bar = df_bar.groupby(level=[0,1], sort=False).mean()
    months_and_years = [(year, month) for year in years for month in months]
    df_bar = pd.Series([fill_na(x, df_bar) for x in months_and_years], 
                       index=pd.MultiIndex.from_tuples(months_and_years, names=['year', 'month']),
                       name='value')

    # Draw bar plot 
    fig, ax = plt.subplots(figsize=[8,7])

    width = 0.5
    ticks_locations = [width * (6 + 12*n) + 6*n for n in range(len(years)) ]

    to_month_int = lambda m: pd.Timestamp(m).month
    for month in months:
        month_int = to_month_int(month)
        values = df_bar.loc[:, month]
        x = [width*(12*y + month_int - 1) + 6*y for y in range(len(years))]
        ax.bar(x, values, width, label=month, align='edge')
    
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    ax.set_xticks(ticks_locations, years)
    ax.legend(title='Months', labels=months)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (year_boxplot, month_boxplot) = plt.subplots(ncols=2, figsize=[16, 5], layout='tight')
    bp_cargs = {
        'flierprops': {'marker': 'd', 'markerfacecolor': 'black', 'markersize': 2},
        'linewidth': 0.5,
    }
    
    equal = lambda x, y: x == y
    
    # Year plot
    years = df_box['year'].unique().tolist()
    df_years = pd.DataFrame([[v for v in df_box[df_box['year'].apply(equal, y=year)]['value']] for year in years], index=years).T
    
    sns.boxplot(data=df_years, ax=year_boxplot, **bp_cargs)
    year_boxplot.set_xlabel('Year')
    year_boxplot.set_ylabel('Page Views')
    year_boxplot.set_title('Year-wise Box Plot (Trend)')
        
    # Month plot
    to_month_int = lambda m: pd.to_datetime(m, format='%b').month
    to_month_name = lambda m: pd.to_datetime(m, format="%m").month_name()
    
    df_months = df_box[['month', 'value']]
    df_months.loc[:,'month'] = df_months['month'].map(to_month_int)
    df_months = df_months.sort_values(by='month', axis=0)
    df_months.loc[:,'month'] = df_months['month'].map(to_month_name)
    
    sns.boxplot(data=df_months, x='month', y='value', ax=month_boxplot, hue='month', formatter=lambda s: s[:3], legend=False, **bp_cargs)
    month_boxplot.set_xlabel('Month')
    month_boxplot.set_ylabel('Page Views')
    month_boxplot.set_title('Month-wise Box Plot (Seasonality)')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
