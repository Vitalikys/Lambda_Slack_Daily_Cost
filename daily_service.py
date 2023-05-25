# Создать на лямбде приложение, которое считает ежедневные затраты денег по аккаунту и шлет отчет в слак
import boto3


class DailyCostsBills:
    """
    Class to calculate AWS costs, using period of two time points
    """
    def __init__(self, region="us-east-1"):
        self._cloud_watch_client = None
        self.region = region

    @property
    def cloud_watch_client(self):
        if not self._cloud_watch_client:
            self._cloud_watch_client = boto3.client("cloudwatch", region_name=self.region)
        return self._cloud_watch_client

    def get_total_cost(self, start_time, end_time):
        """
        method to calculate AWS costs between two points
        :param start_time: start time point
        :param end_time: end time point
        :return: sum of all Datapoints
        """
        responce = self.cloud_watch_client.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[{
                'Name': 'Currency',
                'Value': 'USD'
            }],
            StartTime=start_time,
            EndTime=end_time,
            Period=1800,  # 0.5 hours  # in result would be maximum 4 points
            # Period=3600,  # 1 hours    # in result would be maximum 4 points
            # Period=21600,  # 6 hours
            # Period=43200, # 12 hours
            # Period=86400,  # 24 hours
            Statistics=['Maximum']  # ['Sum']
            # Statistics=['Average']
        )
        print('======================')
        print(responce)
        print('======================')
        day_costs = 0
        data_points = responce["Datapoints"]

        print('\n----start:', start_time, 'start printing Datapoints----')
        print('count of all points:', len(data_points)) # print for debugging

        # Main part to calculate /get one cost of Datapoints
        for item in data_points:
            print(item)  # print for debugging
        if len(data_points) == 0:
            return day_costs

        one_dp_max = max([item["Maximum"] for item in data_points])
        return round(one_dp_max, 2)
