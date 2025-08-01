# Import required libraries
import json                          # For parsing and generating JSON
import boto3                         # AWS SDK to interact with DynamoDB
import string                        # To generate random string for short URL
import random                        # Random character selection

# Initialize DynamoDB resource and reference the 'ShortUrls' table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

# -----------------------
# Function: generate_short_id
# Description: Generates a random alphanumeric short ID
# Length: Default is 6 characters
# -----------------------
def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# -----------------------
# Function: lambda_handler
# Description: Main entry point for Lambda
# Handles POST for creating short URLs, GET for redirection, and OPTIONS for CORS
# -----------------------
def lambda_handler(event, context):
    method = event['requestContext']['http']['method']

    # --- Handle CORS preflight request (OPTIONS method) ---
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    # --- Handle POST request to create a short URL ---
    if method == "POST":
        try:
            body = json.loads(event['body'])           # Parse JSON body
            long_url = body.get('long_url')            # Get the long URL field

            # Validate input
            if not long_url:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"error": "Missing long_url"})
                }

            # Generate short ID and store in DynamoDB
            short_id = generate_short_id()
            table.put_item(Item={"id": short_id, "url": long_url})

            # Respond with generated short URL using domain from request context
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "short_url": f"{event['requestContext']['domainName']}/{short_id}"
                })
            }

        except Exception as e:
            # Catch unexpected errors and return error message
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": str(e)})
            }

    # --- Handle GET request to redirect to the original URL ---
    elif method == "GET":
        short_id = event['rawPath'].lstrip("/")         # Extract short ID from the path
        result = table.get_item(Key={"id": short_id})   # Query DynamoDB

        # If short URL exists, redirect to the original long URL
        if 'Item' in result:
            return {
                "statusCode": 302,
                "headers": {
                    "Location": result['Item']['url'],  # Redirect location
                    "Access-Control-Allow-Origin": "*"
                },
                "body": ""
            }
        else:
            # Handle case where short URL is not found
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Short URL not found"})
            }

    # --- Handle unsupported HTTP methods ---
    return {
        "statusCode": 405,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"error": "Method not allowed"})
    }