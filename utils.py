import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import json
import matplotlib.dates as mdates
from datetime import datetime
import csv

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

# Estimate the meet point using linear interpolation
def estimate_meet_point(timestamps, revenue, initial_investment):
    for i in range(len(timestamps) - 1):
        if (revenue[i] < initial_investment <= revenue[i + 1]) or (revenue[i] > initial_investment >= revenue[i + 1]):
            x1, x2 = mdates.date2num(timestamps[i]), mdates.date2num(timestamps[i + 1])
            y1, y2 = revenue[i], revenue[i + 1]
            meet_point = x1 + (initial_investment - y1) * (x2 - x1) / (y2 - y1)
            meet_date = mdates.num2date(meet_point)
            return meet_date
    return None

def create_line_chart_breakevenpoint(csv_path, initial_investment, X):
    ''' This function takes in a csv file, initial investment, and independent variable.
    It returns a string object of json object with csv file and plot object.
    It creates a line chart and saves it to a binary stream.
    '''

    print("Inside create_line_chart_breakevenpoint function...")
    timestamps = []
    cumulative_revenue = []
    csv_path = "Revenue.csv"

    with open(csv_path) as csvfile:
        csvreader = csv.reader(csvfile)
    
        # Skip the header row if it exists
        next(csvreader, None)
        
        # Initialize a variable to keep track of cumulative revenue
        total_revenue = 0

        for row in csvreader:
            # Extract the timestamp and revenue from the row
            timestamp_str, revenue_str = row
            revenue = float(revenue_str)
            
            # Append the timestamp to the timestamps list
            timestamps.append(timestamp_str)
            
            # Calculate the cumulative revenue and append it to the cumulative_revenue list
            total_revenue += revenue
            cumulative_revenue.append(total_revenue)

    timestamps = [datetime.strptime(ts, '%Y-%m-%d') for ts in timestamps]
    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the revenue data as a line chart
    ax.plot(timestamps, cumulative_revenue, marker='o', linestyle='-', color='b', label='Revenue')

    # Highlight the initial investment
    ax.axhline(y=initial_investment, color='r', linestyle='--', label='Initial Investment')

    meet_date = estimate_meet_point(timestamps, cumulative_revenue, initial_investment)

    # Annotate the estimated meet point
    if meet_date:
        ax.annotate(f'Estimated Meet Point ({initial_investment}, {meet_date:%b %Y})', 
                    xy=(meet_date, initial_investment), 
                    xytext=(meet_date, initial_investment + 1000), 
                    arrowprops=dict(arrowstyle='->', color='g'))
        break_even_point_msg = f'Break-even point date: {meet_date:%d-%m-%Y}'

    else:
        ax.annotate('Lines do not intersect', 
                    xy=(timestamps[-1], initial_investment), 
                    xytext=(timestamps[-1], initial_investment + 1000), 
                    arrowprops=dict(arrowstyle='->', color='g'))
        break_even_point_msg = 'No break-even point'

    # Formatting the x-axis date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)

    # Add labels and title
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Revenue')
    ax.set_title('Revenue vs. Timestamp')

    # Add a legend
    ax.legend()

    # Display the plot
    plt.tight_layout()

    print("Plotting the graph...")

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

    out_dict = {'msg': break_even_point_msg, 'plot': plot_string}

    out = json.dumps(out_dict)
    print(out)

    # Return the plot as a hexadecimal string
    return out