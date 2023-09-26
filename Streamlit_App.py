import streamlit as st
import openai
import datetime
import asyncio
import pandas as pd
import numpy as np
from Kernel import make_kernel
from Planner import ForecastingPlanner
from MarketResearchSkill import CSVForecasting
import matplotlib.pyplot as plt
import io
import json

def get_plot(plot_string):
    ''' It Converts the hexadecimal string to binary data, then 
    creates a BytesIO stream from the binary data, then
    reads the plot from the stream and shows it.
    '''
    # Convert the hexadecimal string back to binary data
    plot_binary_data = bytes.fromhex(plot_string)

    # Create a BytesIO stream from the binary data
    plot_binary_stream = io.BytesIO(plot_binary_data)
    
    # Read the plot from the stream and show it
    plot = plt.imread(plot_binary_stream)
    plt.imshow(plot)
    plt.axis('off')  # Turn off axis labels and ticks
    return plt

async def main():

    # Streamlit App Title
    st.title("CSV Analysis App")

    # File Upload Section
    st.sidebar.header("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    # Check if a file is uploaded
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Check if the CSV file has headers
        if not df.columns.any():
            st.warning("Please add headers to the CSV file.")
        else:
            # Independent Variables Selection (Checkbox)
            st.sidebar.header("Select Independent Variables (X)")
            independent_variables = st.sidebar.multiselect("Select one or more independent variables", df.columns)

            # Check if at least one independent variable is selected
            if not independent_variables:
                st.warning("Please select at least one independent variable.")
            else:
                # Display selected independent variables
                st.write(f"Independent Variables (X): {', '.join(independent_variables)}")

                # User Questions and Responses
                st.sidebar.header("Ask Questions")
                user_question = st.sidebar.text_input("Enter your question:")
                
                # Check if the user has entered a question
                if user_question:
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.read())

                    ask = f'''{user_question} \n
                    Independent Variables (X): {independent_variables} \n
                    CSV file: {uploaded_file.name}
                    '''

                    print(ask) 

                    kernel = await make_kernel() 
                    kernel.import_skill(CSVForecasting(), "CSVForecasting")

                    planner = ForecastingPlanner()
                    generated_plan = await planner.create_plan_async(ask, kernel)
                    output = await planner.plan_executor_async(generated_plan, kernel)

                    try:
                        dictionary = json.loads(output)

                        plot_string = dictionary['plot']
                        plot_obj = get_plot(plot_string)

                        # Check if csv key exists in the dictionary
                        if 'csv' in dictionary:
                            response_csv_data = dictionary['csv']
                            # Display the CSV data in a scrollable window
                            st.subheader("Response (CSV Data)")

                            with open(response_csv_data, "rb") as file:
                                st.download_button(
                                    label="Download CSV",
                                    data=file,
                                    file_name=response_csv_data,
                                    key="download-file"
                                )

                            df = pd.read_csv(response_csv_data)
                            st.dataframe(df)

                        # Show the graph using st.pyplot()
                        st.subheader("Graph")
                        st.pyplot(plot_obj)

                        # Hide the data summary
                        st.markdown("---")  # Add a horizontal line to separate sections
                    except:
                        # Show output as text
                        st.subheader("Response")
                        st.write(output)
                else:
                    st.warning("Please enter a question to proceed.")
    else:
        st.warning("Please upload a CSV file and select independent variables to proceed.")

if __name__ == "__main__":
    asyncio.run(main())
