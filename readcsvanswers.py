#! /usr/bin/python3
import pandas as pd
from secrets import *  # format von secrets.py: csv_link = r"[google.docs.link]"

dataframe = pd.read_csv(csv_link)
print(dataframe)
