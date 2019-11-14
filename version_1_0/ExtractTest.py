
"""
This file takes the APC and Breeze and makes it into a faster single data file to speed up the testing

"""

import pandas as pd
import os
import datetime as dt


def load_apc(path, start, end):
    """
    This function loads the whole apc data file into a single data frame
    :return:
    """
    df = pd.read_pickle(path)
    df = df[(df['CALENDAR_ID'] >= start) & (df['CALENDAR_ID'] <= end)]
    df = df[pd.notnull(df['ARRIVAL_TM_HM'])]
    df.loc[:, "ARRIVAL_TM_HM"] = df["ARRIVAL_TM_HM"].str.split(':')
    df.insert(len(df.columns), 'ARRIVAL_DTM', df.apply(
        lambda x: x.CALENDAR_ID + dt.timedelta(hours=int(x.ARRIVAL_TM_HM[0]), minutes=int(x.ARRIVAL_TM_HM[1])), axis=1))
    return df[
        ['ROUTE_ABBR', 'SERVICE_TYPE_TEXT', 'VECHILE_TAG', 'LATITUDE', 'LONGITUDE', 'BOARD', 'ALIGHT', 'ARRIVAL_DTM']]

def load_breeze(path, start, end):
    """
    This function loads the whole breeze data file into a single data frame
    :return:
    """
    breeze_df = pd.read_pickle(path)
    breeze_df = breeze_df[(breeze_df['Transaction_dtm'] >= start) & (breeze_df['Transaction_dtm'] <= end)]
    return breeze_df

def clean_breeze(file_path, start, end):
    """
    This function takes the breeze_card file in the form of a csv file  and cleans it before merging.
    It will also export single day files pickled and stored in the file_path in a dictionary
    :param file_path: str, the input path
    :param out_path: str, the directory where the files will be stored
    :return: tuple, containing a
    """
    print('cleaning breeze data')
    breeze_df = pd.read_pickle(file_path)
    breeze_df = breeze_df[(breeze_df['Transaction_dtm'] >= start) & (breeze_df['Transaction_dtm'] <= end)]
    breeze_df = breeze_df[(breeze_df['Dev_Operator'].str.contains('MARTA'))]
    breeze_df = breeze_df[~((breeze_df['use_type_desc'].str.contains('Tag Off')) &(breeze_df['Dev_Operator'].str.contains('MARTA Bus')))]
    # remove this line once GTRA data and cobb county data has been added in
    bus_df = breeze_df[pd.notnull(breeze_df['bus_id'])]
    rail_df = breeze_df[breeze_df['Dev_Operator'].str.contains('MARTA Rail')]
    rail_df.insert(len(rail_df.columns),'stop_name',rail_df['ctl_grp_short_desc'].str.split('-').apply(lambda x: x[1]))
    rail_df.update(rail_df['stop_name'].str.lower())
    rail_df.update(rail_df['stop_name'].str.strip())
    indexes = []
    rail_df.sort_values(by='Transaction_dtm')
    for group, frame in rail_df.groupby('Serial_Nbr'):
        frame.sort_values(by='Transaction_dtm')
        frame.insert(len(frame.columns),'Lag', (frame['Transaction_dtm'] - frame['Transaction_dtm'].shift()).apply(lambda x: x.seconds))
        frame.insert(len(frame.columns),'Lag_Stop', frame['stop_name'] == frame['stop_name'].shift())
        threshold = 120
        indexes.extend(list(frame[(frame['Lag'] <= threshold) & (frame['Lag_Stop'])].index))
    rail_df.drop(index=indexes,inplace=True)
    indexes = []
    for group, frame in bus_df.groupby("Serial_Nbr"):
        frame.sort_values(by='Transaction_dtm')
        frame.insert(len(frame.columns),'Lag', (frame['Transaction_dtm'] - frame['Transaction_dtm'].shift()).apply(lambda x: x.seconds))
        #frame.insert(len(frame.columns),'Lag_Stop', frame['bus_id'] == frame['bus_id'].shift())
        threshold = 300
        indexes.extend(list(frame[(frame['Lag'] <= threshold) & (frame['bus_id'] == frame['bus_id'].shift())].index))
    bus_df.drop(index=indexes,inplace=True)
    # add in line to merge the two into a single data frame
    return bus_df.append(rail_df)


if __name__ == '__main__':
    fileDir = os.path.realpath(__file__).split('/version_1_0')[0]
    start = dt.datetime.strptime("01/30/18 00:00", "%m/%d/%y %H:%M")
    end = dt.datetime.strptime("01/31/18 00:00", "%m/%d/%y %H:%M")
    data_path = os.path.join(fileDir, 'Data')
    apc_path = os.path.join(data_path,'apc.pick')
    breeze_path = os.path.join(data_path,'breeze.pick')
    #load_apc(apc_path,start,end).to_pickle(os.path.join(data_path,'apc_test.pick'))]
    load_breeze(breeze_path, start, end).to_pickle(os.path.join(data_path,'breeze_test.pick'))