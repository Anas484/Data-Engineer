import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Handle both JSON string or dict in 'body'
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        # Extract card info
        card_number = body.get("card_number")
        cvv = body.get("cvv")
        expiry = body.get("expiry")
        amount = body.get("amount")

        # Parse expiry: MM/YY → datetime
        expiry_date = datetime.strptime(expiry, "%m/%y")
        now = datetime.now()

        # Simulate basic card validation
        if (
            card_number.startswith("4") and
            len(cvv) == 3 and  # Corrected: 3-digit CVV for Visa
            (expiry_date.year > now.year or (expiry_date.year == now.year and expiry_date.month >= now.month))
        ):
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "valid": True,
                    "message": "Card Valid",
                    "card_number": card_number,
                    "amount": amount
                })
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "valid": False,
                    "message": "Please Enter a Visa",
                    "error": "Invalid Card"
                })
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

