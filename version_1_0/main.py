
from os.path import join
import numpy as np
import pandas as pd
'''
#####################
In this we want to use our functions to:
	1. Create clusters of stops (l-means clustering ?)
	2. Chain the breeze card data to the apc data to the gtfs data
			- 

#####################
'''
# print(pd.Timestamp(1474934134,unit = 's'))


# path = "../../MARTA_gtfs_12_08_2018"
# df = pd.read_csv(join(path, "stops.txt"))

# print(df.tail())
# print(len(df))




def main():
	import odx
	odx.main() # create new trips file 


if __name__ == "__main__":
	main()