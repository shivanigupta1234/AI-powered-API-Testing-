import requests
import json
import openai
import os
from transformers import pipeline

class APITestingAI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.model = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
        #openai.api_key = os.getenv('OPENAI_API_KEY')
        #print(openai.api_key)

    def interpret_command(self, command):
        try:
            print("command", command)
            response = self.model(command)[0]['generated_text']
            print("response", response)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        return response

    """
    def interpret_command(self, command):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": command}
                ]
            )
        except openai.error.RateLimitError:
            print("You have exceeded your OpenAI API quota. Please wait for it to reset or upgrade your plan.")
            return None
        interpreted_command = response['choices'][0]['message']['content']
        return interpreted_command
    """
    def execute_request(self, method, endpoint, data=None, params=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/json'}
        print(method, url, data, params)
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                response = requests.post(url, data=json.dumps(data), headers=headers)
            elif method == 'PUT':
                response = requests.put(url, data=json.dumps(data), headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError("Invalid HTTP method.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return response

    def analyze_response(self, response):
        response_data = response.json()
        # Analyze response data using AI (not implemented in this example)
        return "Success" if response_data.get('status') == 'success' else "Failure"

    def validate_response(self, response):
        return 200 <= response.status_code < 300

# Example usage:
if __name__ == "__main__":
    base_url = 'https://jsonplaceholder.typicode.com/todos/'
    api_ai = APITestingAI(base_url)

    # Test Case 1: GET all todo items
    command_1 = "GET all todo items"
    interpreted_command_1 = api_ai.interpret_command(command_1)
    method_1, endpoint_1 = interpreted_command_1.split(" ", 1)
    response_1 = api_ai.execute_request(method_1, endpoint_1)
    print("Test Case 1 - Response:", response_1.text)

    # Test Case 2: GET a specific todo item by ID
    command_2 = "GET a specific todo item by ID"
    interpreted_command_2 = api_ai.interpret_command(command_2)
    method_2, endpoint_2 = interpreted_command_2.split(" ", 1)
    response_2 = api_ai.execute_request(method_2, endpoint_2)
    print("Test Case 2 - Response:", response_2.text)

    # Test Case 3: GET all todo items for a specific user
    command_3 = "GET all todo items for user 1"
    interpreted_command_3 = api_ai.interpret_command(command_3)
    method_3, endpoint_3 = interpreted_command_3.split(" ", 1)
    response_3 = api_ai.execute_request(method_3, endpoint_3)
    print("Test Case 3 - Response:", response_3.text)

    # Test Case 4: GET all completed todo items for a specific user
    command_4 = "GET all completed todo items for user 1"
    interpreted_command_4 = api_ai.interpret_command(command_4)
    method_4, endpoint_4 = interpreted_command_4.split(" ", 1)
    response_4 = api_ai.execute_request(method_4, endpoint_4)
    print("Test Case 4 - Response:", response_4.text)

    # Test Case 5: GET all incomplete todo items for a specific user
    command_5 = "GET all incomplete todo items for user 1"
    interpreted_command_5 = api_ai.interpret_command(command_5)
    method_5, endpoint_5 = interpreted_command_5.split(" ", 1)
    response_5 = api_ai.execute_request(method_5, endpoint_5)
    print("Test Case 5 - Response:", response_5.text)

    # Validate responses
    responses = [response_1, response_2, response_3, response_4, response_5]
    for i, response in enumerate(responses, start=1):
        print(f"Test Case {i} - Validation:", "Success" if api_ai.validate_response(response) else "Failure")
