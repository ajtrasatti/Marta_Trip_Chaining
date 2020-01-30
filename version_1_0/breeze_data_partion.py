"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0

# This file partitions the breeze_transactions.csv into daily files
# Each one goes from 3am to 3am the next day
"""
import datetime as dt
import pandas as pd
from os import mkdir
from os.path import join

import time

t0 = time.time()

# ###################
# start_date = dt.datetime(2018,1,30)
# end_date = dt.datetime(2018,1,31)
# ###################

# start_time = start_date + dt.timedelta(hours=3)
# end_time = start_time + dt.timedelta(days=1)

# df = pd.read_csv("../Data/apc_test.csv")#,parse_dates=["ARRIVAL_DTM"])

def mk_path(path):
	try: 
		mkdir(path)
	except:
		pass
	return path

def to_csv(date,df_temp):
	print(date)
	path = mk_path(mypath)
	path = mk_path(path + str(date.year)
			+ "_" + str(date.month)  
			+ "_" + str(date.day) )

	df_temp.sort_values("Transaction_dtm").to_csv(join(path,"breeze_test.csv"))


mypath = "../Data/partitioned2/"
# load dataframe (1 min - 22M rows)
filename = "/Users/anthonytrasatti/Desktop/Research/Marta/data/breeze_transactions.csv"
df = pd.read_csv(filename)#, nrows = 10000)

print("TEST: loded df", time.time()-t0)
t0 = time.time()


print(df.columns)
before_len = len(df)
print("len of df: ", len(df))



temp_col = pd.to_datetime(df.Transaction_dtm, format = "%Y-%m-%d %H:%M:%S")
print(temp_col[0:10])
print("in date time format : ", time.time()-t0)
t0 = time.time()

temp_col = temp_col - pd.Timedelta(hours=3)
print("adjusted time to marta day : ",time.time()-t0) # this part took 4 mins
t0 = time.time()

groups = df.groupby(temp_col.dt.date)
print("TEST: grouped", time.time()-t0)
t0 = time.time()

data_list = [to_csv(date,df_temp) for date, df_temp in groups]
