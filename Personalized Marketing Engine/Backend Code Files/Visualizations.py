import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paths - update if needed
CSV_PATH = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\Raw_data\Dataset.csv'
JSON_PATH = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\P1\cluster_data.json'
VISUALS_ROOT = 'visuals'  # output folder for visuals
os.makedirs(VISUALS_ROOT, exist_ok=True)

def annotate_bars(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', (p.get_x() + p.get_width()/2, height), ha='center', va='bottom', fontsize=9)

def annotate_stacked_bars(ax):
    for bar_container in ax.containers:
        for bar in bar_container:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', (bar.get_x() + bar.get_width()/2, bar.get_y() + height/2),
                            ha='center', va='center', fontsize=8, color='white', fontweight='bold')

# Load dataset
df = pd.read_csv(CSV_PATH)

# Load cluster JSON
with open(JSON_PATH, 'r') as f:
    cluster_data = json.load(f)

# Iterate over clusters
for cluster_key, entry in cluster_data.items():
    customer_ids = entry.get('customer_ids', [])
    # Cast customer_ids to match df Customer_ID dtype
    dtype = df['Customer_ID'].dtype
    if dtype == object:
        customer_ids_casted = [str(x) for x in customer_ids]
    elif np.issubdtype(dtype, np.integer):
        customer_ids_casted = [int(x) for x in customer_ids]
    elif np.issubdtype(dtype, np.floating):
        customer_ids_casted = [float(x) for x in customer_ids]
    else:
        customer_ids_casted = customer_ids

    cluster_df = df[df['Customer_ID'].isin(customer_ids_casted)]
    n_rows = cluster_df.shape[0]

    if n_rows == 0:
        print(f"Cluster {cluster_key} has no matching customers in dataset, skipping.")
        continue

    cluster_folder = os.path.join(VISUALS_ROOT, f"cluster_{cluster_key}")
    os.makedirs(cluster_folder, exist_ok=True)

    # 1. Customer Overview
    # Gender Distribution (bar)
    if 'Gender' in cluster_df.columns:
        gender_counts = cluster_df['Gender'].fillna('Unknown').value_counts()
        fig, ax = plt.subplots(figsize=(6,4))
        gender_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Gender Distribution')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Number of Customers')
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'gender_distribution_bar.png'), bbox_inches='tight')
        plt.close(fig)

    # Age Distribution Histogram
    if 'Age' in cluster_df.columns:
        ages = cluster_df['Age'].dropna()
        if not ages.empty:
            fig, ax = plt.subplots(figsize=(6,4))
            counts, bins, patches = ax.hist(ages, bins=10, edgecolor='black', alpha=0.7)
            ax.set_title(f'Cluster {cluster_key} - Age Distribution')
            ax.set_xlabel('Age')
            ax.set_ylabel('Number of customers')
            for count, patch in zip(counts, patches):
                if count > 0:
                    ax.annotate(f'{int(count)}', (patch.get_x() + patch.get_width()/2, count), ha='center', va='bottom', fontsize=8)
            fig.savefig(os.path.join(cluster_folder, 'age_distribution_hist.png'), bbox_inches='tight')
            plt.close(fig)

    # 2. Purchasing Patterns
    # Most Purchased Categories (bar)
    if 'Category' in cluster_df.columns:
        category_counts = cluster_df['Category'].fillna('Unknown').value_counts()
        fig, ax = plt.subplots(figsize=(10,5))
        category_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Most Purchased Categories')
        ax.set_xlabel('Category')
        ax.set_ylabel('Count of Products')
        plt.xticks(rotation=45, ha='right')
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'most_purchased_categories_bar.png'), bbox_inches='tight')
        plt.close(fig)

    # 3. Sales and Revenue
    if ('Purchase_Amount_USD' in cluster_df.columns) and ('Category' in cluster_df.columns):
        revenue_by_cat = cluster_df.groupby('Category')['Purchase_Amount_USD'].sum().sort_values(ascending=False)*88.77
        fig, ax = plt.subplots(figsize=(10,6))
        revenue_by_cat.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Revenue by Category (INR)')
        ax.set_xlabel('Category')
        ax.set_ylabel('Revenue (INR)')
        plt.xticks(rotation=45, ha='right')
        for i, v in enumerate(revenue_by_cat):
            ax.annotate(f'{v:.2f}', (i, v), ha='center', va='bottom', fontsize=8)
        fig.savefig(os.path.join(cluster_folder, 'revenue_by_category_bar.png'), bbox_inches='tight')
        plt.close(fig)

    # 5. Customer Engagement & Loyalty
    if 'Subscription_Status' in cluster_df.columns:
        sub_counts = cluster_df['Subscription_Status'].fillna('none').value_counts()
        fig, ax = plt.subplots(figsize=(6,4))
        sub_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Subscription Status Distribution')
        ax.set_xlabel('Status')
        ax.set_ylabel('Count of Subscription')
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'subscription_status_bar.png'), bbox_inches='tight')
        plt.close(fig)

    if 'Frequency_of_Purchases' in cluster_df.columns:
        freq_counts = cluster_df['Frequency_of_Purchases'].fillna('Unknown').value_counts()
        fig, ax = plt.subplots(figsize=(8,5))
        freq_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Frequency of Purchases')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Number of Customers')
        plt.xticks(rotation=45, ha='right')
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'frequency_purchases_bar.png'), bbox_inches='tight')
        plt.close(fig)

    if 'Previous_Purchases' in cluster_df.columns:
        prev = pd.to_numeric(cluster_df['Previous_Purchases'], errors='coerce').fillna(0)
        repeat = (prev > 0).sum()
        one_time = (prev == 0).sum()
        fig, ax = plt.subplots(figsize=(6,4))
        bars = ax.bar(['Repeat','One-time'], [repeat, one_time])
        ax.set_title(f'Cluster {cluster_key} - Repeat vs One-time Buyers')
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}', (bar.get_x() + bar.get_width()/2, height), ha='center', va='bottom', fontsize=9)
        fig.savefig(os.path.join(cluster_folder, 'repeat_vs_one_time_buyers_hist.png'), bbox_inches='tight')
        plt.close(fig)

    # 6. Payment and Shipping Preferences
    if 'Payment_Method' in cluster_df.columns:
        pm_counts = cluster_df['Payment_Method'].fillna('Unknown').value_counts()
        fig, ax = plt.subplots(figsize=(10,5))
        pm_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Payment Method Popularity')
        ax.set_xlabel('Payment Method')
        ax.set_ylabel('Number of Customers')
        plt.xticks(rotation=45, ha='right')
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'payment_method_popularity_bar.png'), bbox_inches='tight')
        plt.close(fig)

    if 'Shipping_Type' in cluster_df.columns:
        ship_counts = cluster_df['Shipping_Type'].fillna('Unknown').value_counts()
        fig, ax = plt.subplots(figsize=(8,5))
        ship_counts.plot(kind='bar', ax=ax)
        ax.set_title(f'Cluster {cluster_key} - Shipping Type Distribution')
        ax.set_xlabel('Shipping Type')
        ax.set_ylabel('Count of Delivery Type')
        plt.xticks(rotation=45, ha='right')
        annotate_bars(ax)
        fig.savefig(os.path.join(cluster_folder, 'shipping_type_distribution_bar.png'), bbox_inches='tight')
        plt.close(fig)

    # 7. Customer Satisfaction
    if 'Review_Rating' in cluster_df.columns:
        ratings = pd.to_numeric(cluster_df['Review_Rating'], errors='coerce').dropna()
        if not ratings.empty:
            fig, ax = plt.subplots(figsize=(8,5))
            counts, bins, patches = ax.hist(ratings, bins=np.arange(0, 5.5, 0.5), edgecolor='black')
            ax.set_title(f'Cluster {cluster_key} - Review Rating Distribution')
            ax.set_xlabel('Review Rating')
            ax.set_ylabel('Count of Reviews')
            for count, patch in zip(counts, patches):
                if count > 0:
                    ax.annotate(f'{int(count)}', (patch.get_x() + patch.get_width()/2, count), ha='center', va='bottom', fontsize=8)
            fig.savefig(os.path.join(cluster_folder, 'review_rating_distribution_hist.png'), bbox_inches='tight')
            plt.close(fig)

    print(f"Completed visuals for Cluster {cluster_key} ({n_rows} customers)")

print("All cluster visuals generated under folder:", os.path.abspath(VISUALS_ROOT))


# Visualizations.py
import os
from tkinter import Tk, Canvas, Frame, Scrollbar, Label, BOTH, RIGHT, LEFT, Y, NW, PhotoImage
from PIL import Image, ImageTk

def show_visuals_scrollable(cluster_path):
    """
    Display all images in a folder using a scrollable Tkinter window.
    cluster_path: str - path to cluster folder (e.g., 'visuals/cluster_0')
    """
    if not os.path.exists(cluster_path):
        print(f"Folder {cluster_path} does not exist!")
        return

    root = Tk()
    root.title(f"Cluster Visuals: {os.path.basename(cluster_path)}")
    root.configure(bg='#FF7F0E')  # Orange background

    # Create scrollable frame
    canvas = Canvas(root, bg='#FF7F0E')
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg='#FF7F0E')
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0,0), window=scroll_frame, anchor=NW)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Load and display images
    images = []
    for filename in sorted(os.listdir(cluster_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(cluster_path, filename)
            img = Image.open(img_path)
            img = img.resize((600, 400))  # resize for display
            photo = ImageTk.PhotoImage(img)
            images.append(photo)  # keep reference
            label = Label(scroll_frame, image=photo, bg='#FF7F0E')
            label.pack(pady=10)

    root.mainloop()
