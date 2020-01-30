"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0

# This file partitions the APC.csv into daily files
# Each one goes from 3am to 3am the next day
"""

import datetime as dt
import pandas as pd
from os import mkdir
from os.path import join

import time

'''
# This file partitions the APC.csv into daily files
# Each one goes from 3am to 3am the next day

'''

t0 = time.time()

# ###################
# start_date = dt.datetime(2018,1,30)
# end_date = dt.datetime(2018,1,31)
# ###################

# start_time = start_date + dt.timedelta(hours=3)
# end_time = start_time + dt.timedelta(days=1)

# apc_df = pd.read_csv("../Data/apc_test.csv")#,parse_dates=["ARRIVAL_DTM"])

def mk_path(path):
	try: 
		mkdir(path)
	except:
		pass
	return path

def to_csv(date,df):
	print(date)
	path = mk_path("../Data/partitioned2/")
	path = mk_path(path + str(date.year)
			+ "_" + str(date.month)  
			+ "_" + str(date.day) )


	df.sort_values("ARRIVAL_DTM").to_csv(join(path,"apc_test.csv"))


# load dataframe (1 min - 22M rows)
filename = "/Users/anthonytrasatti/Desktop/Research/Marta/data/APC.csv"
apc_df = pd.read_csv(filename, nrows = 10000)

print("TEST: loded apc", time.time()-t0)
t0 = time.time()


print(apc_df.columns)
before_len = len(apc_df)
print("len before: ", len(apc_df))
apc_df = apc_df[apc_df.ARRIVAL_TM_HM != ":"] # get rid of rows without a time
per_remaining = round(len(apc_df)/ before_len * 100,2) # percent remaining
print("len after: ", len(apc_df), per_remaining)


print("test: removed empty rows", time.time()-t0)
t0 = time.time()

dates = pd.to_datetime(apc_df.CALENDAR_ID, format = "%Y-%m-%d %H:%M:%S")
print("test date conversion : ", time.time()-t0)
t0 = time.time()

arrival_times = apc_df.ARRIVAL_TM_HM.apply(
	lambda x: dt.timedelta(hours = int(x[0:2]),minutes = int(x[3:5])))
print("test arrival times : ", time.time()-t0)
t0 = time.time()
exit()

departure_times = apc_df.DEPARTURE_TM_HM.apply(
	lambda x: dt.timedelta(hours = int(x[0:2]),minutes = int(x[3:5])))
print("test departure times : ", time.time()-t0)
t0 = time.time()



apc_df["ARRIVAL_DTM"] = dates + arrival_times
apc_df["DEPARTURE_DTM"] = dates + departure_times

print("test: create time columns", time.time()-t0)
t0 = time.time()

# apc_

apc_df.drop(["CALENDAR_ID","ARRIVAL_TIME","ARRIVAL_TM_HM","DEPARTURE_TIME","DEPARTURE_TM_HM"], axis=1, inplace=True)
apc_df = apc_df[["ARRIVAL_DTM", "DEPARTURE_DTM", 'ROUTE_ABBR', 'ROUTE_NAME', 
		'VECHILE_TAG', 'LATITUDE', 'LONGITUDE', 'BOARD', 'ALIGHT',
		'SERVICE_TYPE_TEXT', 'ROUTE_DIRECTION_NAME', 'RUN_NUM', 
        'TRIP_SEQUENCE', 'TRIP_SERIAL_NUMBER', 'BLOCK_ABBR',
        'BLOCK_NUM','BLOCK_TRIP_SEQ','BLOCK_STOP_ORDER' ]]
       
print("TEST: prepped columns : ", time.time()-t0)
t0 = time.time()

temp_col = pd.to_datetime(apc_df.ARRIVAL_DTM, format = "%Y-%m-%d %H:%M:%S")
print("in date time format : ", time.time()-t0)
t0 = time.time()

temp_col = temp_col - pd.Timedelta(hours=3)
print("adjusted time to marta day : ",time.time()-t0)
t0 = time.time()

groups = apc_df.groupby(temp_col.dt.date)
print("TEST: grouped", time.time()-t0)
t0 = time.time()

data_list = [to_csv(date,df) for date, df in groups]

## Old code below -- not fully functional
# while start_time < end_date:
# 	# filter dataframe to day
# 	df = apc_df[(apc_df.ARRIVAL_DTM > start_time) & 
# 				(apc_df.ARRIVAL_DTM < end_time)]
# 	# output csv to a folder
# 	path1 = "../Data/partitioned/" 
# 	path = (path1 + str(start_time.year)
# 			+ "_" + str(start_time.month)  
# 			+ "_" + str(start_time.day) )
	
# 	try: 
# 		mkdir(path1)
# 	except: 
# 		pass
# 	try:	mkdir(path)
# 	except:	pass


# 	df.to_csv(join(path,"apc_test.csv"))

# 	start_time = end_time
# 	end_time += dt.timedelta(days=1)