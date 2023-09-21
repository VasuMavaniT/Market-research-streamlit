from semantic_kernel.skill_definition import sk_function
import semantic_kernel as sk
from utils import sales_prediction, price_prediction, revenue_prediction
from semantic_kernel.kernel import Kernel

class CSVForecasting:
    # def __init__(self, kernel: Kernel):
    #     self.kernel = kernel
    # Required if memory search is used
    # Initialize the skill with the kernel as a parameter

    @sk_function(
    description="Forecast the value of sales based on dependent and independent variables with csv file",
    name="sales"
    )
    def sales(self, context: sk.SKContext) -> str:
        csv_path = context.variables.get("csv_path")
        dependent_variable = context.variables.get("dependent_variable")
        independent_variable = context.variables.get("independent_variable")
        duration = context.variables.get("duration")
        csv = csv_path[1]
        dependent = dependent_variable[1]
        independent = independent_variable[1]
        time = duration[1]

        output = sales_prediction(csv, dependent, independent, time)
        return output
    
    @sk_function(
        description="Predict the value of price for different time periods based on dependent and independent variables with csv file",
        name="price"
    )
    def price(self, context: sk.SKContext) -> str:
        csv_path = context.variables.get("csv_path")
        dependent_variable = context.variables.get("dependent_variable")
        independent_variable = context.variables.get("independent_variable")
        duration = context.variables.get("duration")
        csv = csv_path[1]
        dependent = dependent_variable[1]
        independent = independent_variable[1]
        time = duration[1]

        output = price_prediction(csv, dependent, independent, time)
        return output
    
    @sk_function(
        description="Forecast the value of revenue based on dependent and independent variables with csv file",
        name="revenue"
    )
    def revenue(self, context: sk.SKContext) -> str:
        csv_path = context.variables.get("csv_path")
        dependent_variable = context.variables.get("dependent_variable")
        independent_variable = context.variables.get("independent_variable")
        duration = context.variables.get("duration")
        csv = csv_path[1]
        dependent = dependent_variable[1]
        independent = independent_variable[1]
        time = duration[1]

        output = revenue_prediction(csv, dependent, independent, time)
        return output