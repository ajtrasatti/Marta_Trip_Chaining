import pandas as pd
from collections import defaultdict

filename = "Data/trips.csv"

stop_count = defaultdict(lambda : 0)

def count(stop,df):
    stop_count[stop] += len(df)



df = pd.read_csv(filename)#, index_col=0)


# Find the counts for how many times each stop was used as a origin or destination
groups = df.groupby("start_stop")
[count(stop,df) for stop,df in groups if stop != -1]
groups = df.groupby("end_stop")
[count(stop,df) for stop,df in groups if stop != -1]

stop_counts_arr = [(stop,count) for stop, count in stop_count.items()]
pd.DataFrame(stop_counts_arr,columns = ["start_stop","count"]).to_csv("Data/StopCounts_April1-10.csv",index=False)
# pd.DataFrame(dests, columns = ["end_stop","count"]).to_csv("destinations_April1-10.csv",index=False)



# OD matrix 
groups = df.groupby(["start_stop","end_stop"])
odx = [(stop[0],stop[1],len(df)) for stop,df in groups if stop[0] != -1 and stop[1] != -1]
pd.DataFrame(odx, columns = ["start_stop","end_stop","count"]).to_csv("Data/odx_April1-10.csv", index=False)
print(len(odx))
