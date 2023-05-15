import json
from datetime import datetime, timedelta

import requests
from dateutil.relativedelta import relativedelta

from daily_service import DailyCostsBills

day_bills = DailyCostsBills()


def lambda_handler(event, context):
    try:
        url_slack = "https://hooks.slack.com/services/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"

        # definition timepoints for calc periods
        current_time = datetime.now()
        start_time_last24h = current_time - timedelta(hours=24)
        start_of_prev_month = (current_time - relativedelta(months=1)).replace(day=1, hour=0, minute=0)
        end_of_prev_month = start_of_prev_month.replace(day=1, hour=0, minute=0) + relativedelta(months=1)

        # calculate costs in USD
        today_cost = day_bills.get_total_cost(start_time_last24h, current_time)
        prev_month = day_bills.get_total_cost(start_of_prev_month, end_of_prev_month)

        payload = {"text": f"Total (last 24 hours) cost: {today_cost} USD \n \
                            Previous month: {start_of_prev_month.strftime('%B')} - {prev_month} USD"
                   }
        # Print results LOCALLY
        print('Printing PAYLOAD: ')
        print(payload['text'])

        # Sending to Slack group
        requests.post(
            url=url_slack,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return str(e)
