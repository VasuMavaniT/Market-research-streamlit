import json

from semantic_kernel.kernel import Kernel
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.planning.plan import Plan

PROMPT = """

NOTE: CSVForecasting has only 3 functions: sales, price and revenue.

[GOAL]
Predict or forecast the value of sales based on dependent and independent variables with csv file for a given period
[OUTPUT]
{
  "input": "Predict or forecast the value of sales based on dependent and independent variables with csv file for a given period",
  "subtasks":
  {
    "function": "CSVForecasting.sales",
    "args":
    {
        "csv_path": "Temp_file.csv",
        "dependent_variable": "Your dependent variable here in a list [A, B, C]",
        "independent_variable": "Your independent variable here",
        "duration": "Your duration here in months (Integer)"
    }
  }
}

[GOAL]
Predict or forecast the value of price for different time periods based on dependent and independent variables with csv file
[OUTPUT]
{
  "input": "Predict or forecast the value of price for different time periods based on dependent and independent variables with csv file",
  "subtasks":
    {
      "function": "CSVForecasting.price",
      "args":
      {
        "csv_path": "Temp_file.csv",
        "dependent_variable": "Your dependent variable here in a list [A, B, C]",
        "independent_variable": "Your independent variable here",
        "duration": "Your duration here in months (Integer)"
      }
    }
}

[GOAL]
Predict or forecast the value of revenue based on dependent and independent variables with csv file for a given time period
[OUTPUT]
{
  "input": "Predict or forecast the value of revenue based on dependent and independent variables with csv file for a given time period",
  "subtasks":
    {
      "function": "CSVForecasting.revenue",
      "args":
      {
        "csv_path": "Temp_file.csv",
        "dependent_variable": "Your dependent variable here in a list [A, B, C]",
        "independent_variable": "Your independent variable here",
        "duration": "Your duration here in months (Integer)"
      }
    }
}

[GOAL]
{{$goal}}
[OUTPUT]
"""


class ForecastingPlanner:
  async def create_plan_async(
    self,
    goal: str,
    kernel: Kernel,
    prompt: str = PROMPT,
  ) -> Plan:
    ''' Generate a plan for the given goal using the given kernel.
    Generated plan is a JSON string as shown in the example.
    '''
    
    # Create the semantic function for planner
    planner = kernel.create_semantic_function(
      prompt, max_tokens=1024, temperature=0.0
    )

    # Create the context for the planner
    context = ContextVariables()

    context["goal"] = goal

    # Invoke and create plan !
    generated_plan = await planner.invoke_async(variables=context)
    plan = str(generated_plan.variables)
    return plan
    # return Plan(prompt=prompt, goal=goal, plan=generated_plan)

  async def plan_executor_async(self, plan, kernel: Kernel) -> str:
    ''' It returns the result of the plan execution by calling
    parse_task function and passing the task to it.
    '''
    generated_plan = json.loads(plan)
    task = generated_plan["subtasks"]
    result = await self.parse_task_break_even(task, kernel)
    return result
  
  async def parse_task_break_even(self, tasks, kernel) -> str:
    ''' Parse the task and execute it using the given kernel.
    It returns the result of the task execution. 
    Skill name and function are extracted from the task and
    the function is invoked using the kernel.
    '''
    try:
      task = json.loads(tasks)
    except:
      task = tasks


    skill_name, function_name = task["function"].split(".")
    sk_function = kernel.skills.get_function(skill_name, function_name)

    args = task.get("args", None)
    context = ContextVariables()
    if args:
      for key, value in args.items():
        context[key] = value

    output = await sk_function.invoke_async(variables=context)
    return output.result