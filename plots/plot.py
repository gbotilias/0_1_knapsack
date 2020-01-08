import plotly.express as px
import pandas as pd
import numpy as np

# Select name of csv to read and plot
# 1. profit_plot.csv
# 2. weight_plot.csv
# 3. time_plot.csv
plot_df = pd.read_csv('profit_or_weight_or_time_plot.csv')
df_long=pd.melt(plot_df, id_vars=['Problem'], value_vars=['Greedy', 'BruteForce', 'Branch&Bound', 'Dynamic', 'Dynamic_ortools', 'Integer_ortools'])

# plotly
figure = px.line(df_long, x='Problem', y='value', color='variable')

# Show plot
figure.show()