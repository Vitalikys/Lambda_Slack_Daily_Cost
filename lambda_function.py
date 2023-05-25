import json
from datetime import datetime, timedelta
import os
import requests
from dateutil.relativedelta import relativedelta

from daily_service import DailyCostsBills

day_bills = DailyCostsBills()
url_slack = os.environ['SLACK_URL']


def lambda_handler(event, context):
    try:
        # get account ID
        lambda_arn = context.invoked_function_arn.split(':')[-3]
        # definition timepoints for calc periods
        current_time       = datetime.now()
        start_time_last24h = current_time - timedelta(hours=24)
        yesterday_start    = (current_time - relativedelta(days=1)).replace(hour=0, minute=0, second=0)
        yesterday_ends     = current_time.replace(hour=0, minute=0, second=0)

        start_of_prev_month= (current_time - relativedelta(months=1)).replace(day=1, hour=0, minute=0)
        end_of_prev_month  = start_of_prev_month.replace(day=1, hour=0, minute=0) + relativedelta(months=1)

        # calculate costs in USD
        # today_cost      = day_bills.get_total_cost(start_time_last24h, current_time)
        # yesterd_cost    = day_bills.get_total_cost(yesterday_start, yesterday_ends)
        # prev_month_cost = 0 # day_bills.get_total_cost(start_of_prev_month, end_of_prev_month)
        current_month   = day_bills.get_total_cost(current_time-timedelta(hours=5), current_time)

        payload = {"text": f" Execution Time: {current_time.strftime('%d %B %Y  %H:%M:%S')}\
        \n account ID: {lambda_arn}\n\
        \nCurrent month  ({current_time.strftime('%B')}): {current_month} USD\
        "
                }
        # Print timePoints LOCALLY
        print('--------- Printing DATES - TimePoints: -------------')
        print('current time: ', current_time)
        print('start prev month:', start_of_prev_month)
        print('End prev month  :', end_of_prev_month)
        print('yesterday starts : ', yesterday_start)
        print('yesterday ends at: ', yesterday_ends)
        print('----------- END Printing  TimePoints ---------------')
        # Sending to Slack group
        requests.post(
            url=url_slack,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return str(e)
