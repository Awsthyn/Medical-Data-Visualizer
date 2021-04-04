import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = df.apply(lambda row: 1 if ((row.weight / (row['height'] * row['height']) *10000) > 25) else 0, axis= 1)

#df.apply(bmi_to_bool, axis="columns")

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
def normalize_data(row):
  if row.cholesterol == 1:
    row.cholesterol = 0
  elif row.cholesterol > 1:
    row.cholesterol = 1
  if row.gluc == 1:
    row.gluc = 0
  elif row.gluc > 1:
    row.gluc = 1
  return row
df = df.apply(normalize_data, axis=1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars=["cardio"], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active','overweight'])
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    # Draw the catplot with 'sns.catplot()'
    sns.color_palette("tab10")
    fig = sns.catplot(x="variable", order=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], hue="value", kind="count", col="cardio",  data=df_cat)
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    fig.axes[0,0].set_ylabel('total')
    
    
    return fig.fig
   

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[df['ap_lo'] <= df['ap_hi']]
    df_heat = df_heat[df['height'] >= df['height'].quantile(0.025)]
    df_heat = df_heat[df["height"] <= df["height"].quantile(0.975)]
    df_heat = df_heat[df['weight'] >= df['weight'].quantile(0.025)]
    df_heat = df_heat[df['weight'] <= df['weight'].quantile(0.975)]
    # Calculate the correlation matrix
    corr = df_heat.corr()
    corr = corr.round(1)
    # Generate a mask for the upper triangle
    mask = corr.mask(np.triu(np.ones(corr.shape)).astype(np.bool))
    sns.color_palette("tab10")


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(mask, annot=True, square=True, fmt='.1f')


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
