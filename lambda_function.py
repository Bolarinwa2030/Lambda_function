import json
import math
import urllib.request

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return sum(digit ** power for digit in digits) == n

# Function to check if a number is a perfect number
def is_perfect(n):
    if n < 1:
        return False
    return sum(i for i in range(1, n // 2 + 1) if n % i == 0) == n

# Function to get a fun fact about the number using urllib
def get_fun_fact(n):
    if n < 0:
        return "Fun fact not available for negative numbers."
    try:
        url = f"http://numbersapi.com/{n}/math"
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.read().decode("utf-8")
    except Exception:
        return "Fun fact not available."

# AWS Lambda Handler
def lambda_handler(event, context):
    query_params = event.get("queryStringParameters", {})
    number_str = query_params.get("number") if query_params else None

    if not number_str:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "No number provided."})
        }

    try:
        number = int(float(number_str))
    except ValueError:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "error": "Invalid number format",
                "invalid_input": number_str  # Include the invalid input in the response
            })
        }

    properties = ["odd" if number % 2 else "even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")

    response_body = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(number))),
        "fun_fact": get_fun_fact(number)
    }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(response_body)
    }
