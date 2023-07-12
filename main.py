
import time
import os

import pandas as pd
import numpy as np
import datetime

from passenger_counter import clean_up, stops_routes, te5b_stops, dates
import logging
from send_email import send_email_with_attachment

from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

PATH="/home/tns/Dropbox/Family Room/2023 Stats"

engine = create_engine(os.getenv('DATABASE_URI'))


def formatter():
    for file in os.listdir():
        if file.endswith('.xlsx') and not file.startswith('~'):
            df = pd.read_excel(file)
            now = datetime.datetime.now() + datetime.timedelta(hours=2)
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Formatting {file}")
            df = stops_routes.get_stops_routes(df)
            df = df[df['Route'].notnull()]
            df['Alarm Time'] = pd.to_datetime(df['Alarm Time'])
            df['Date'] = df['Alarm Time']
            df['Year'] = df.Date.dt.year
            df['Year'] = df['Year'].astype(str)
            df['Month'] = df.Date.dt.month_name()
            df['Day'] = df.Date.dt.day
            df['Day'] = df['Day'].astype(str)
            df['DOW'] = df.Date.dt.day_name()
            df['MY'] = df.Month + ' ' + df.Year
            df['Date'] = df.Day + ' ' + df.Month + ' ' + df.Year
            df['Week'] = df.DOW.map(dates.add_week)
            df.sort_values(by=['Alarm Time'], inplace=True)
            df.reset_index(inplace=True, drop=True)
            df = df[
                ['Bus No', 'IN', 'Out', 'Number of people', 'Alarm Time', 'GNSS', 'Stop Name', 'Route', 'Date', 'DOW',
                 'MY',
                 'Week']]
            df = te5b_stops.get_te5b_stops(df)
            df = clean_up.clean_up(df)
            df['Run'] = np.NaN
            df['Run_id'] = np.NaN
            now = datetime.datetime.now() + datetime.timedelta(hours=2)
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Saving to excel")
            df.to_excel('updated v2 ' + file, index=False)
            df = df.reset_index(drop=True)
            now = datetime.datetime.now() + datetime.timedelta(hours=2)
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Exporting to database")
            df = df.loc[:, 'Bus No': 'Run_id']
            df.columns = [
                'bus_no',
                'in_count',
                'out_count',
                'number_of_people',
                'alarm_time',
                'gnss',
                'stop_name',
                'route',
                'date',
                'dow',
                'month',
                'week',
                'run',
                'run_id']
            df.to_sql('trips_v5', engine, if_exists='append', index=False)
            now = datetime.datetime.now() + datetime.timedelta(hours=2)
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Done formatting {file}")


def main():
    not_found = True
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    logging.info("Searching for none formatted files.")
    formated_files = []
    for root, dirs, files in os.walk(PATH, topdown=False):
        for name in dirs:
            if name.startswith('Passenger Counter Statistics') and name.find('(') == -1 and name.find(
                    '2022-02-24') == -1 and name.find('2022-02-14') == -1:
                folder = os.path.join(root, name)
                file_list = os.listdir(folder)
                if len(file_list) == 1 and file_list[0].endswith('.xlsx'):
                    file = file_list[0]
                    logging.info(f"Formatting file: {file}")
                    formated_files.append(file)
                    os.chdir(folder)
                    formatter()
                    print('\n')
                    not_found = False
                else:
                    continue
    if not_found:
        logging.info("No none formatted files found.")
    else:
        logging.info(f"Formated files: {', '.join(formated_files)}")
        file_path = os.path.join(os.getenv('DIR'),'log.txt')
        body = f"<p>Good day</p><p>Attached please find log file with Reformat script logging </p><p>Kind regards,<br>Reformat Automated Script</p>"
        subject = "Reformat passed!"
        to = 'mbudzeni@thenakedscientists.co.za'
        send_email_with_attachment(file_path,subject,body,to)
        


if __name__ == '__main__':
    main()
