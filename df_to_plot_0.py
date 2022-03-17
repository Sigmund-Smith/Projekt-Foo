#! /usr/bin/python3
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as ipy
import pandas as pd
import numpy as np


#load dataframe google api
#dataframe = pd.read_csv("data.csv", parse_dates=["Zeitstempel"], index_col=0)
dataframe.dropna(axis=1, how="all", inplace=True) #delete empty columns

#numerical version of data
übersetzer = {"Zufrieden":5,
"Eher zufrieden":4,
"Eher Zufrieden":4,
"Neutral":3,
"Eher unzufrieden":2,
"Eher Unzufrieden":2,
"Unzufrieden":1,
"Stark gefühlt":3,
"Merkbar gefühlt":2,
"Schwach gefühlt":1,
"Entspannt":5,
"Eher Entspannt":4,
"Neutral":3,
"Eher Angespannt":2,
"Gestresst":1,
np.nan:np.nan}

xticklabels = []
yticklabels = []

#plot func
def plot_0(axis_0, axis_1):
    try:
        global xticklabels
        global yticklabels

        #Lösungsansatz des Problems der uneinheitlichen Beschriftung und der Reihenfolge beim plotten
        #Nachteil: hängt von den einträgen "Zufrieden", "Merkbar gefühlt" ab. 
        #sollte irgendwann verbessert werden
        if dataframe[str(axis_0)].isin(["Zufrieden"]).any():
            xticklabels = ["Unzufrieden", "Eher unzufrieden", "Neutral", "Eher zufrieden", "Zufrieden"]
        elif dataframe[str(axis_0)].isin(["Merkbar gefühlt"]).any():
            xticklabels = ["Nicht gefühlt", "Schwach gefühlt", "Merkbar gefühlt", "Stark gefühlt"]

        if dataframe[str(axis_1)].isin(["Zufrieden"]).any():
            yticklabels = ["Unzufrieden", "Eher unzufrieden", "Neutral", "Eher zufrieden", "Zufrieden"]
        elif dataframe[str(axis_1)].isin(["Merkbar gefühlt"]).any():
            yticklabels = ["Nicht gefühlt", "Schwach gefühlt", "Merkbar gefühlt", "Stark gefühlt"]

        #Lösungsansatz des Problems der uneinheitlichen Beschriftung und der Reihenfolge beim plotten
        #numerische umwandlung
        axis_0_numeric = []
        axis_1_numeric = []
        for i in range(len(dataframe)):
            axis_0_numeric.append(übersetzer[dataframe.iloc[i, :][axis_0]]-1)
            axis_1_numeric.append(übersetzer[dataframe.iloc[i, :][axis_1]]-1)


        #plot
        fig, ax = plt.subplots(figsize=(12,8))
        sns.scatterplot(data=dataframe, x=axis_0_numeric, y=axis_1_numeric, ax=ax, alpha=.7)
        
        #label
        ax.set(xlabel=str(axis_0), ylabel=str(axis_1))

        #set ticks
        ax.set_xticks(range(len(xticklabels)))
        ax.set_xticklabels(xticklabels)

        ax.set_yticks(range(len(yticklabels)))
        ax.set_yticklabels(yticklabels)
        
        
        #correlation
        corr = round(pd.Series(axis_0_numeric).corr(pd.Series(axis_1_numeric)),2)
        
        #textbox
        ax.text(0.0, -0.08, f"Correlation: {corr}.", transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', bbox={"boxstyle":'round', "facecolor":'wheat', "alpha":0.2})
        
    except Exception as e:
        print(f"""Ups, something went wrong \n
        Woran hats gelegen? \n
        {e, type(e)}""")
        

#plot interactiv
ipy.interact(plot_0, axis_0=[c for c in dataframe.columns], axis_1=[c for c in dataframe.columns])
