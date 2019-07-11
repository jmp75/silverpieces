class Utility: 
    def __init__(self): 
        pass

    @staticmethod
    def read_yml_params(args_file):
        product = args_file.get('Args').get('product')
        variable_name = args_file.get('Args').get('variablename')   
        start_date = args_file.get('Args').get('timespan').get('startDate')
        end_date = args_file.get('Args').get('timespan').get('endDate')

        return product, start_date, end_date, variable_name