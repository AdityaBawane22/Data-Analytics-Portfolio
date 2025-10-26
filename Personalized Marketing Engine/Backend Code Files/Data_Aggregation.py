import json
import pandas as pd

def get_cluster_summary(json_path, csv_path):
    with open(json_path, 'r') as f:
        cluster_json = json.load(f)

    df = pd.read_csv(csv_path)

    summary = {}
    for cluster_id, data in cluster_json.items():
        customer_ids = data.get('customer_ids', [])
        cluster_customers = df[df['Customer_ID'].isin(customer_ids)]

        num_customers = cluster_customers['Customer_ID'].nunique()
        total_revenue_usd = cluster_customers['Purchase_Amount_USD'].sum()

        # Convert USD revenue to INR here
        total_revenue_inr = total_revenue_usd * 88.77

        # Cast keys and values properly
        summary[int(cluster_id)] = {
            'num_customers': int(num_customers),
            'total_revenue_inr': float(total_revenue_inr)
        }

    return summary


if __name__ == "__main__":
    json_path = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\P1\cluster_data.json'
    csv_path = r'C:\Aditya Lenovo\HDD storage (E)\Data Science Preparation\Projects\Datasets\Practice Project 1\Customer_Seg\Raw_data\Dataset.csv'

    cluster_summary = get_cluster_summary(json_path, csv_path)

    print(type(cluster_summary))  
    print(cluster_summary)        

    for cluster_id, stats in cluster_summary.items():
        print(f"Cluster {cluster_id}: Customers = {stats['num_customers']}, Revenue (INR) = {stats['total_revenue_inr']:.2f}")
