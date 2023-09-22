import pandas as pd
import numpy as np

def sales_prediction(csv_file, y, X, months):
    sales_df = pd.read_csv('Sales.csv')

    sales_df['Timestamp'] = pd.to_datetime(sales_df['Timestamp'])

    end_date = max(sales_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months-1)

    filtered_sales_df = sales_df[(sales_df['Timestamp'] >= start_date) & (sales_df['Timestamp'] <= end_date)]

    csv_name = 'sales_output.csv'
    # Write dataframe to csv file sales_output.csv
    filtered_sales_df.to_csv(csv_name, index=False)

    return csv_name

def price_prediction(csv_file, y, X, months):
    price_df = pd.read_csv('Price.csv')

    price_df['Timestamp'] = pd.to_datetime(price_df['Timestamp'])

    end_date = max(price_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months-1)

    filtered_price_df = price_df[(price_df['Timestamp'] >= start_date) & (price_df['Timestamp'] <= end_date)]
    csv_name = 'price_output.csv'
    # Write dataframe to csv file price_output.csv
    filtered_price_df.to_csv(csv_name, index=False)

    return csv_name

def revenue_prediction(csv_file, y, X, months):
    revenue_df = pd.read_csv('Revenue.csv')

    revenue_df['Timestamp'] = pd.to_datetime(revenue_df['Timestamp'])

    end_date = max(revenue_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months-1)

    filtered_revenue_df = revenue_df[(revenue_df['Timestamp'] >= start_date) & (revenue_df['Timestamp'] <= end_date)]

    csv_name = 'revenue_output.csv'
    # Write dataframe to csv file revenue_output.csv
    filtered_revenue_df.to_csv(csv_name, index=False)

    return csv_name