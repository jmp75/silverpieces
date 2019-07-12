from enum import Enum


class Statistic(Enum):
    Sum = 1
    Mean = 2


class TimePeriod(Enum):
    Monthly = '1M'
    Yearly = '1y'
    Seasonal = 'Q-FEB'


class Utility:
    def __init__(self):
        pass

    @staticmethod
    def Apply_stat(ds, start_date, end_date, variable_name, statistic, time_period):
        result = ds.sel(time=slice(start_date, end_date))[variable_name] \
            .to_dataset().resample(time=time_period.value)

        if statistic == Statistic.Mean:
            result = result.mean()[variable_name]
        elif statistic == Statistic.Sum:
            result = result.Sum()[variable_name]

        return result

    @staticmethod
    def read_yml_params(args_file):
        product = args_file.get('Args').get('product')
        variable_name = args_file.get('Args').get('variablename')
        start_date = args_file.get('Args').get('timespan').get('startDate')
        end_date = args_file.get('Args').get('timespan').get('endDate')

        return product, start_date, end_date, variable_name
