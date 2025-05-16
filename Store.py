import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

# Load and clean data
df = pd.read_csv('/Users/eugenemonama/Downloads/EXCEL/store.csv')
df = df.rename(columns={'Amount': 'Price_usd'})
df['Price Per Box'] = ''
del df['Date']
df.loc[0, 'Customers'] = 456
df.loc[1, 'Product'] = "Lunch bar"
df['Price_usd'] = df['Price_usd'].str.replace(r'[$,]', '', regex=True).astype(int)
df['Price Per Box'] = (df['Price_usd'] / df['Boxes']).round(2)
# Metrics
sum_of_Boxes = df['Boxes'].sum()
sum_of_Customers = df['Customers'].sum()
total_revenue = df['Price_usd'].sum()

# Helper function to create metric cards
def create_metric_card(ax, value, title, color):
    ax.axis('off')
    rect = Rectangle((0.05, 0.05), 0.9, 0.9, fill=True, color=color, alpha=0.15, ec=color, lw=2, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(0.5, 0.6, f"{value}", fontsize=16, fontweight='bold', ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.3, title, fontsize=12, ha='center', va='center', transform=ax.transAxes)

# Set up subplot grid (2 rows x 3 columns)
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
fig.subplots_adjust(hspace=0.5, wspace=0.4)
fig.suptitle("\u25B2 Store Sales Dashboard", fontsize=20, fontweight='bold', y=0.95)

# Row 1: Metric cards
create_metric_card(axs[0, 0], f"${total_revenue:,.2f}", "Total Revenue", "green")
create_metric_card(axs[0, 1], sum_of_Boxes, "Total Boxes", "gold")
create_metric_card(axs[0, 2], sum_of_Customers, "Total Customers", "red")

# Row 2: Heatmap
correlation_matrix = df[['Price_usd', 'Boxes', 'Customers', 'Price Per Box']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=axs[1, 0])
axs[1, 0].set_title('Correlation Matrix')

# Row 2: Line Chart - Cumulative Revenue
df_sorted = df.sort_values('Price_usd', ascending=False)
df_sorted['Cumulative_Revenue'] = df_sorted['Price_usd'].cumsum()
axs[1, 1].plot(range(len(df_sorted)), df_sorted['Cumulative_Revenue'], marker='o', linestyle='-', linewidth=2)
axs[1, 1].set_title('Cumulative Revenue (Pareto Analysis)')
axs[1, 1].set_xlabel('Customer Count (sorted)')
axs[1, 1].set_ylabel('Cumulative Revenue (USD)')
axs[1, 1].grid(True, alpha=0.3)

# Row 2: Histogram - Distribution of Boxes
axs[1, 2].hist(df['Boxes'], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
axs[1, 2].set_title('Box Quantity Distribution')
axs[1, 2].set_xlabel('Number of Boxes')
axs[1, 2].set_ylabel('Frequency')
axs[1, 2].grid(True, alpha=0.3)

# Show full dashboard
plt.tight_layout(rect=[0, 0, 1, 0.94])  # Leave space for the top title
plt.show()
