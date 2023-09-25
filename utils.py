import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import json

def sales_prediction(csv_file, y, X, months):
    ''' This function takes in a csv file, dependent variable, independent variable, and duration in months.
    It returns a string object of json object with csv file and plot object.
    '''
    sales_df = pd.read_csv('Sales.csv')

    sales_df['Timestamp'] = pd.to_datetime(sales_df['Timestamp'])

    end_date = max(sales_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months)

    filtered_sales_df = sales_df[(sales_df['Timestamp'] >= start_date) & (sales_df['Timestamp'] <= end_date)]

    csv_name = 'sales_output.csv'
    # Write dataframe to csv file sales_output.csv
    filtered_sales_df.to_csv(csv_name, index=False)

    output = create_line_chart(csv_name, 'Timestamp', 'Sales', 'Sales Forecasting', 'Timestamp', 'Sales')

    return output

def price_prediction(csv_file, y, X, months):
    ''' This function takes in a csv file, dependent variable, independent variable, and duration in months.
    It returns a string object of json object with csv file and plot object.
    '''
    price_df = pd.read_csv('Price.csv')

    price_df['Timestamp'] = pd.to_datetime(price_df['Timestamp'])

    end_date = max(price_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months)

    filtered_price_df = price_df[(price_df['Timestamp'] >= start_date) & (price_df['Timestamp'] <= end_date)]
    csv_name = 'price_output.csv'
    # Write dataframe to csv file price_output.csv
    filtered_price_df.to_csv(csv_name, index=False)

    output = create_line_chart(csv_name, 'Timestamp', 'Price', 'Price Forecasting', 'Timestamp', 'Price')

    return output

def revenue_prediction(csv_file, y, X, months):
    ''' This function takes in a csv file, dependent variable, independent variable, and duration in months.
    It returns a string object of json object with csv file and plot object.
    '''
    revenue_df = pd.read_csv('Revenue.csv')

    revenue_df['Timestamp'] = pd.to_datetime(revenue_df['Timestamp'])

    end_date = max(revenue_df['Timestamp'])
    start_date = end_date - pd.DateOffset(months=months)

    filtered_revenue_df = revenue_df[(revenue_df['Timestamp'] >= start_date) & (revenue_df['Timestamp'] <= end_date)]

    csv_name = 'revenue_output.csv'
    # Write dataframe to csv file revenue_output.csv
    filtered_revenue_df.to_csv(csv_name, index=False)

    output = create_line_chart(csv_name, 'Timestamp', 'Revenue', 'Revenue Forecasting', 'Timestamp', 'Revenue')

    return output

def create_line_chart(csv_file, timestamp, data, title, xlabel, ylabel):
    ''' This function takes in a csv file, timestamp, data, title, xlabel, and ylabel.
    It returns a string object of json object with csv file and plot object.
    It creates a line chart and saves it to a binary stream.
    '''
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract timestamp and price columns
    timestamps = df[timestamp]
    datacol = df[data]

    # Create a line chart
    plt.figure(figsize=(10, 6))  # Set the figure size (optional)
    plt.plot(timestamps, datacol, marker='o', linestyle='-', color='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=90)  

    # Save the plot to a binary stream
    plot_binary_stream = io.BytesIO()
    plt.savefig(plot_binary_stream, format='png')
    
    # Reset the stream position and read it as binary data
    plot_binary_stream.seek(0)
    plot_binary_data = plot_binary_stream.read()
    
    # Close the plot and the binary stream
    plt.close()
    plot_binary_stream.close()
    
    # Convert the binary data to a string
    plot_string = plot_binary_data.hex()

    out_dict = {'csv': csv_file, 'plot': plot_string}

    out = json.dumps(out_dict)

    # Return the plot as a hexadecimal string
    return out