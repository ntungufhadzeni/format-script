
def clean_up(arg_df):
    stations = ['506', '504', '502', '101', '102', '103', '104', '105', '500', '200', '202', '204', '206', '207', '208', '209', '205', '203','201', '501', '503', '505', '507', '508', '509']
    routes = ['TE5B - Seshego', 'TE4 - Seshego - Madiba Park']


    for i in arg_df.index:
        route = arg_df.loc[i, 'Route']
        stop = arg_df.loc[i, 'Stop Name']
        if stop in stations and not route in routes:
             arg_df.loc[i, 'Stop Name'] = 'Church Street'

    return arg_df
