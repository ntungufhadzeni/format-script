
import numpy as np
import requests
import warnings
import json
import os
import sys

from . import location
import logging
from send_email  import send_email_with_attachment

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s", filemode="w")

def get_stops_routes(arg_df):
    warnings.filterwarnings('ignore')
    arg_df['Stop Name'] = np.NaN
    arg_df['Route'] = np.NaN
    stops_dict = {
        'F1 - Flora Park': ['316', '300', '301', '301A', '302', '302A', '303', '304', '304A', '304A2','305', '306', '307', '307A', '308', '309',
                            '310', '310-1', '311', '311A','312', '312A','313', '313A','314', '315',],
        'TE4 - Seshego - Madiba Park': ['500', '200', '202', '204', '206', '207', '207A','208', '209', '211', '212','205', '203',
                                        '201', '501', '503', '505', '507', '508', '509'],
        'TE5B - Seshego': ['506', '504', '502', '101', '100', '100A', '102', '102A', '103', '104', '104A', '105', '105A', ],
        'F4B - Westernburg': ['409', '400', '401', '402', '403', '403A', '404', '405', '405A', '406A', '406B','407', '408',]
    }
    
    


    for index in arg_df.index:
        v = arg_df.loc[index, 'GNSS']

        if not str(v).startswith('-'):
            continue

        try:
            cords = v.split(',')
        except AttributeError:
            continue

        cords_lat = cords[0]
        cords_lon = cords[1]
        if cords_lat.find('.') != -1:
            lat = cords_lat
            lon = cords_lon
        else:
            lat = cords_lat[:3] + '.' + cords_lat[3:]
            lon = cords_lon[:2] + '.' + cords_lon[2:]

        if location.is_layover(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'LayOver'
            continue
        elif location.is_fuel_wise(lat, lon):
            arg_df.loc[index, 'Stop Name'] = 'Fuel Wise'
            continue

        url = 'http://46.101.72.176:8080/otp/routers/default/index/stops'
        params = {'lat': lat, 'lon': lon, 'radius': 300}

        try:
            response = requests.get(url, params=params)
        except:
            logging.error("Error formatting the file")
            file_path = os.path.join(os.getenv('DIR'),'log.txt')
            body = f"<p>Good day</p><p>Attached please find log file with Reformat script logging </p><p>Kind regards,<br>Reformat Automated Script</p>"
            subject = "Reformat failed!"
            to = 'mbudzeni@thenakedscientists.co.za'
            send_email_with_attachment(file_path,subject,body,to)
            sys.exit()

        if response.status_code == 200:
            data_res = json.loads(response.text)
            if len(data_res) > 1:
                dist_list = []
                for i in range(len(data_res)):
                    dist_list.append(data_res[i]['dist'])
                min_dist = min(dist_list)
                min_index = dist_list.index(min_dist)
                stop_name = data_res[min_index]['name']
            elif len(data_res) == 1:
                stop_name = data_res[0]['name']
            elif len(data_res) == 0:
                stop_name = location.get_new_stop(lat, lon)
                if stop_name == '':
                    continue
            else:
                continue
        else:
            continue

        church = {'410': "F4B - Westernburg", '316': "F1 - Flora Park", '409': "TE4 - Seshego - Madiba Park",
                  '509': "TE5B - Seshego", }
        stop = stop_name


        if stop in church.keys():
            stop_name = 'Church Street'
            route = church[stop]
            arg_df.loc[index, 'Stop Name'] = stop_name
            arg_df.loc[index, 'Route'] = route
        else:
            for key in stops_dict.keys():
                if stop_name in stops_dict[key]:
                    route = key
                    arg_df.loc[index, 'Stop Name'] = stop_name
                    arg_df.loc[index, 'Route'] = route
                    break

    return arg_df
