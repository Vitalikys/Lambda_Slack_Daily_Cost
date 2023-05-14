import json
import requests
from daily_service import DailyCostsBills

day_bills = DailyCostsBills()


def lambda_handler(event, context):
    try:
        url_slack = "https://hooks.slack.com/services/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"
        day_cost = day_bills.get_total_daily_cost()

        payload = {"text": f"Total last 24 hours cost: {day_cost} USD"}
        requests.post(
            url=url_slack,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return str(e)

