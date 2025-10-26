import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import json
import os

# Load raw data
raw_customer_data_df = pd.read_csv(
    r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\Raw_data\Dataset.csv'
)

# Currency conversion
USD_TO_INR_RATE = 88.77
raw_customer_data_df['Purchase_Amount_INR'] = raw_customer_data_df['Purchase_Amount_USD'] * USD_TO_INR_RATE

# Map purchase frequency to days
frequency_map_days = {
    'Weekly': 7,
    'Annually': 365,
    'Every Three Months': 90,
    'Monthly': 30,
    'Fortnightly': 14,
    'Quarterly': 90,
    'Bi-Weekly': 14
}
raw_customer_data_df['Frequency_into_Days'] = raw_customer_data_df['Frequency_of_Purchases'].map(frequency_map_days)

# Scaling
robust_features = ['Age', 'Frequency_into_Days', 'Purchase_Amount_INR', 'Previous_Purchases']
minmax_features = ['Review_Rating']

robust_scaler = RobustScaler()
minmax_scaler = MinMaxScaler()

robust_scaled_df = pd.DataFrame(
    robust_scaler.fit_transform(raw_customer_data_df[robust_features]),
    columns=robust_features, index=raw_customer_data_df.index
)
minmax_scaled_df = pd.DataFrame(
    minmax_scaler.fit_transform(raw_customer_data_df[minmax_features]),
    columns=minmax_features, index=raw_customer_data_df.index
)

# One-hot encode Gender
gender_encoded = pd.get_dummies(raw_customer_data_df['Gender'], drop_first=True)
if 'Male' in gender_encoded.columns:
    gender_encoded.columns = ['Gender_Male']

# Combine features
X_scaled = pd.concat([robust_scaled_df, minmax_scaled_df, gender_encoded], axis=1)

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_final = imputer.fit_transform(X_scaled)

# Run DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan.fit(X_final)
raw_customer_data_df['Cluster'] = dbscan.labels_

# Prepare data to save in JSON
clusters = {}
for cluster_label in raw_customer_data_df['Cluster'].unique():
    cluster_df = raw_customer_data_df[raw_customer_data_df['Cluster'] == cluster_label]
    customer_ids = cluster_df['Customer_ID'].tolist()
    clusters[str(cluster_label)] = {
        'customer_ids': customer_ids,
        'num_customers': len(customer_ids)
    }

# Save JSON
json_file_path = os.path.join(os.path.dirname(__file__), 'cluster_data.json')
with open(json_file_path, 'w') as f:
    json.dump(clusters, f, indent=4)

print(f"\n✅ Cluster data saved to JSON at: {json_file_path}")
print(json.dumps(clusters, indent=4))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np
from matplotlib.colors import ListedColormap 

# Column indices based on X_final order: 0=Age, 1=Frequency, 2=Amount, 3=Prev_Purchases, 4=Rating
FREQUENCY_INDEX = 1  
AMOUNT_INDEX = 2     
RATING_INDEX = 4     


X_plot = X_final[:, FREQUENCY_INDEX] # X-axis: Purchase Frequency
Y_plot = X_final[:, AMOUNT_INDEX]    # Y-axis: Purchase Amount
Z_plot = X_final[:, RATING_INDEX]    # Z-axis: Review Rating
bubble_size = (X_final[:, RATING_INDEX] + 1) * 200 # Using Rating for size is now redundant, but kept for visual weight


color_map_dict = {
    -1: '#000000',       # Noise/Outliers
    0: '#1f77b4',     # Core Loyal Buyers (e.g., a strong blue)
    1: '#ff7f0e',     # Infrequent Explorers (e.g., an attention-grabbing orange)
    2: '#2ca02c',     # Mid-Frequency Shoppers (e.g., a stable green)
    3: '#d62728',     # High-Value/At-Risk (e.g., a critical red)
    4: '#9467bd',     # Highest Spenders (e.g., a premium purple)
    5: '#8c564b',     # Positive Reviewers 
}

# Create an array of colors corresponding to each point's cluster label
point_colors = np.array([color_map_dict.get(label, 'black') for label in dbscan.labels_])


# Set up the 3D figure
fig = plt.figure(figsize=(14, 10)) 
ax = fig.add_subplot(111, projection='3d') 


scatter = ax.scatter(
    X_plot, Z_plot, Y_plot, 
    c=point_colors,         
    s=bubble_size,
    alpha=0.7, 
    edgecolors='black', 
    linewidths=0.8
)


ax.set_title('3D Customer Segmentation: Value, Loyalty, and Satisfaction', fontsize=18, pad=20)
ax.set_xlabel('Purchase Frequency (X-axis) - Loyalty', fontsize=12, labelpad=10)
ax.set_zlabel('Purchase Amount (Z-axis) - Value', fontsize=12, labelpad=10)
ax.set_ylabel('Review Rating (Y-axis) - Satisfaction', fontsize=12, labelpad=10) 



raw_cluster_ids = np.unique(dbscan.labels_)
cluster_labels = [f"Cluster {l}" if l != -1 else "Noise (Cluster -1)" for l in raw_cluster_ids]

cluster_handles = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                            markerfacecolor=color_map_dict.get(raw_cluster_ids[i], 'black'), markersize=10) 
                   for i, label in enumerate(cluster_labels)]


# fig.legend for better placement in 3D plots
fig.legend(cluster_handles, cluster_labels,
           loc="lower left", 
           bbox_to_anchor=(0.05, 0.05),
           title="Identified Segments (Color)", 
           title_fontsize=12,
           fontsize=10)

handles_size, labels_size = scatter.legend_elements(prop="sizes", alpha=0.7, num=[0.01, 0.45, 0.95])
fig.legend(handles_size,
           ['Low Size', 'Mid Size', 'High Size'], 
           loc="upper right", 
           bbox_to_anchor=(0.95, 0.95),
           title="Bubble Size (Rating Redundant)",
           title_fontsize=12,
           fontsize=10)

plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.show()