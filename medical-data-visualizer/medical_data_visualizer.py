import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('./medical_examination.csv')

# Add 'overweight' column
bmi = lambda weight, height: weight / (height ** 2)
df['overweight'] = [1 if bmi(w, h) > 25 else 0 for w, h in zip(df['weight'].tolist(), df['height'].map(lambda x: x / 100).tolist())]

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
normalize = lambda x: 1 if x > 1 else 0
df[['cholesterol', 'gluc']] = df[['cholesterol', 'gluc']].map(normalize)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby('cardio').value_counts().to_frame('total').sort_values('variable')
    
    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(data=df_cat, x='variable', y='total', col='cardio', hue='value', kind='bar', errorbar=None)

    # Get the figure for the output
    fig = plot.figure

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    remove_extremes = lambda x, min, max: min <= x <= max
    correct_pressures = df['ap_hi'] >= df['ap_lo']
    correct_heights = df['height'].apply(remove_extremes, args=(df['height'].quantile(0.025), df['height'].quantile(0.975)))
    correct_weights = df['weight'].apply(remove_extremes, args=(df['weight'].quantile(0.025), df['weight'].quantile(0.975)))
    df_heat = df[correct_pressures & correct_heights & correct_weights]

    # Calculate the correlation matrix
    corr = df_heat.corr('pearson')

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, mask=mask, ax=ax, fmt='.1f', annot=corr)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
