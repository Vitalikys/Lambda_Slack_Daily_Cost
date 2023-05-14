# Создать на лямбде приложение, которое считает ежедневные затраты денег по аккаунту и шлет отчет в слак
from datetime import datetime, timedelta
from dateutil import relativedelta
import boto3


# import pytz


class DailyCostsBills:
    def __init__(self):
        self._cloud_watch_client = None

    @property
    def cloud_watch_client(self):
        if not self._cloud_watch_client:
            self._cloud_watch_client = boto3.client("cloudwatch")
        return self._cloud_watch_client

    def get_total_cost(self, start_time, end_time):
        responce = self.cloud_watch_client.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[{
                'Name': 'Currency',
                'Value': 'USD'
            }],
            StartTime=start_time,
            EndTime=end_time,
            Period=48660,
            # Statistics= ['Sum']# ['Maximum'] # Average
            Statistics=['Maximum']  # Average
        )
        day_costs = 0
        print('responce', responce)

        data_points = responce["Datapoints"]
        if len(data_points) == 0:
            return day_costs
        for item in data_points:
            day_costs += item["Maximum"]
        return day_costs
