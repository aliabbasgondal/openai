from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv ,dotenv_values
import requests
import time
import os
from typing import Any
import requests
from PIL import Image
from IPython.display import Image, display
_ : bool = load_dotenv(find_dotenv()) # read local .env file

load_dotenv(find_dotenv())
FMP_API_KEY: str = os.environ.get("FMP_API_KEY")
OPENAI_KEY: str = os.environ.get("OPENAI_API_KEY")

client : OpenAI = OpenAI()


# Define financial statement functions
def get_income_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_balance_sheet(ticker, period, limit):

    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_cash_flow_statement(ticker, period, limit):

    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_key_metrics(ticker, period, limit):
    
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_financial_ratios(ticker, period, limit):
 
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_financial_growth(ticker, period, limit):

    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

# Map available functions
available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_financial_ratios,
    "get_financial_growth": get_financial_growth
}


financial_tools = [
    {"type": "code_interpreter"},
            {"type": "function",
             "function": {
                 "name": "get_income_statement",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
           {"type": "function",
             "function": {
                 "name": "get_balance_sheet",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
           
           {"type": "function",
             "function": {
                 "name": "get_cash_flow_statement",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
           
           {"type": "function",
             "function": {
                 "name": "get_key_metrics",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
           {"type": "function",
             "function": {
                 "name": "get_financial_ratios",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
            {"type": "function",
             "function": {
                 "name": "get_financial_growth",
                 "parameters": {"type": "object",
                                "properties": 
                                    {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
]

INSTRUCTIONS = "Act as a financial analyst by accessing detailed financial data through the Financial Modeling Prep API. Your capabilities include analyzing key metrics, comprehensive financial statements, vital financial ratios, and tracking financial growth trends. "



# A Class to Manage All Open API Assistant Calls and Functions
from openai.types.beta.threads import Run, ThreadMessage
from openai.types.beta.thread import Thread
from openai.types.beta.assistant_create_params import Tool
import time

class FinancialAssitantManager:
    def __init__(self, model: str = "gpt-3.5-turbo-1106", tools : list[Tool] = financial_tools, instructions : str = INSTRUCTIONS ):
        self.client = OpenAI()
        self.model = model
        self.tools = tools
        self.instructions = instructions
        self.assistant = None
        self.thread = None
        self.run = None

    def create_assistant(self, name: str)->Any:
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model
        )
        return self.assistant
    def create_thread(self)->Thread:
        self.thread = self.client.beta.threads.create()
        return self.thread
    
    def add_message_to_thread(self, role: str, content: str) -> None:
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )
        
    def create_message(self,role:str,content:str)->None:
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )
    
    def run_assistant(self, instructions: str) -> Run:
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )
        return self.run

    def wait_for_completion(self, run: Run, thread: Thread) -> Run:
        # Loop until the run completes or requires action
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Add run steps retrieval here
            run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
            print("Run Steps:", run_steps)

            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        output = function_to_call(**function_args)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": output,
                        })

                # Submit tool outputs and update the run
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            elif run.status == "completed":
                # List the messages to get the response
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                return messages
                break  # Exit the loop after processing the completed run

            elif run.status == "failed":
                return "Something went wrong, please try again."
                break

            elif run.status in ["in_progress", "queued"]:
                print(f"Run is {run.status}. Waiting...")
                time.sleep(5)  # Wait for 5 seconds before checking again

            else:
                return f"Unexpected Error: {run.status}"
                break
        
# Show Messages and Plot Images in Financial Analysis If ANY
             
                
def fmp_financial_analyst(prompt: str):
    fmp_analyst = FinancialAssitantManager()

    fmp_analyst.create_assistant(
        name="Financial Analyst"
    )

    fmp_analyst.create_thread()

    fmp_analyst.add_message_to_thread(
        role="user",
        content=prompt
    )

    run = fmp_analyst.run_assistant(
        instructions=INSTRUCTIONS
    )

    final_res = fmp_analyst.wait_for_completion(
        run=run,
        thread=fmp_analyst.thread
    )

    return final_res
    
