# Создать на лямбде приложение, которое считает ежедневные затраты денег по аккаунту и шлет отчет в слак
import boto3


class DailyCostsBills:
    def __init__(self, region="us-east-1"):
        self._cloud_watch_client = None
        self.region = region

    @property
    def cloud_watch_client(self):
        if not self._cloud_watch_client:
            self._cloud_watch_client = boto3.client("cloudwatch", region_name=self.region)
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
            # Period=1800,  # 0.5 hours
            Period=3600,  # 1 hours
            # Period=21600,  # 6 hours
            # Period=43200, # 12 hours
            # Period=86400,  # 24 hours
            Statistics=['Maximum']  # ['Sum']
            # Statistics=['Average']
        )
        day_costs = 0

        data_points = responce["Datapoints"]
        print('\n--'*10, 'start:', start_time, 'start printing Datapoints----')
        print('count all points:', len(data_points))
        if len(data_points) == 0:
            return day_costs
        for item in data_points:
            print(item["Average"], end=', ')
            day_costs += item["Average"]
        print('--'*10, 'END Datapoints------')
        return round(day_costs, 2)
