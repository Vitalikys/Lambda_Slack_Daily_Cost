import json
from datetime import datetime, timedelta
import os
import requests
from dateutil.relativedelta import relativedelta

from daily_service import DailyCostsBills

# Environment variables (we set them on AWS_UI->Lambda->Functions->Configurations
url_slack  = os.environ['SLACK_URL']
period     = int(os.environ['PERIOD_DATA_POINTS'])
DELTA_TIME = timedelta(hours=int(os.environ['DELTA_TIME_HOURS'])) # Delta time period. For this period we take/Gather all Datapoints

day_bills = DailyCostsBills()


def calculate(end_time_point, cls_obj=day_bills, delta_time=DELTA_TIME, dp_period=period):
    cost = cls_obj.get_total_cost(end_time_point - delta_time, end_time_point, dp_period)
    return round(cost, 2)


def lambda_handler(event, context):
    try:
        # get account ID
        lambda_arn = context.invoked_function_arn.split(':')[-3]

        # definition timepoints for calc periods
        current_time          = datetime.now()
        yesterday_ends_time   = current_time.replace(hour=0, minute=0, second=0) - relativedelta(seconds=3)
        two_days_ago_end_time = (current_time - relativedelta(days=1)).replace(hour=0, minute=0, second=0)
        end_for_prev_month    = current_time.replace(day=1, hour=0, minute=0, second=0) - relativedelta(minutes=1)

        # calculate costs in USD.
        # Get bills for ENDs of the day, then we calculate difference between this day bills.
        today_cost_end        = calculate(current_time)
        yesterd_cost_end      = calculate(yesterday_ends_time)
        two_days_ago_cost_end = calculate(two_days_ago_end_time)

        prev_month_cost = calculate(end_for_prev_month)
        current_month   = calculate(current_time)

        payload = {"text": f" Execution Time: {current_time.strftime('%d %B %Y  %H:%M:%S')}\
        \nAccount ID: {lambda_arn}\n\
        \nToday spent ({current_time.strftime('%d %B')}): {today_cost_end-yesterd_cost_end} USD\
        \nYesterday spent({yesterday_ends_time.strftime('%d %B')}) : {yesterd_cost_end-two_days_ago_cost_end} USD\
        \nCurrent month  ({current_time.strftime('%B')}): {current_month} USD\
        \nPrevious month ({end_for_prev_month.strftime('%B')}): {prev_month_cost} USD\
        "}

        # Print timePoints LOCALLY
        print('--------- Printing DATES - TimePoints: -------------')
        print('current time: ', current_time)
        print('yesterday_ends_time : ', yesterday_ends_time)
        print('two_days_ago_end_time: ', two_days_ago_end_time)
        print('End prev month  :', end_for_prev_month)
        print('costs three costs - day by day', two_days_ago_cost_end, yesterd_cost_end, today_cost_end)
        print('----------- END Printing  TimePoints ---------------')
        # Sending to Slack group
        requests.post(
            url=url_slack,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        print(str(e))
        return str(e)
