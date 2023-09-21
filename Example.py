import streamlit as st
import openai
import datetime
import asyncio
import pandas as pd
import numpy as np
from Kernel import make_kernel
from Planner import ForecastingPlanner
from MarketResearchSkill import CSVForecasting

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
                    response = await planner.plan_executor_async(generated_plan, kernel)

                    # response = "This is a sample response to your question."
                    st.subheader("Response")
                    st.write(response)

                    # Hide the data summary
                    st.markdown("---")  # Add a horizontal line to separate sections
                else:
                    st.warning("Please enter a question to proceed.")
    else:
        st.warning("Please upload a CSV file and select independent variables to proceed.")

if __name__ == "__main__":
    asyncio.run(main())
