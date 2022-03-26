from oauth2client.service_account import ServiceAccountCredentials
import gspread
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as ipy
import pandas as pd
import numpy as np

# sagt der google api wo sie suchen soll
scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

#dies hier bestätigt google, dass das program auch wirklich auf die tabelle zugreifen darf
GOOGLE_SHEETS_KEY_FILE = 'the-fooprojekt-1c98624c8370.json' # pls ask admin for file
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_FILE, scope)
gc = gspread.authorize(credentials)

# wählt die richtige Tabelle aus
sheet = gc.open("Umfragedaten").sheet1
dataframe0 = pd.DataFrame(sheet.get_all_records())
#clean
dataframe0["Zeitstempel"] = pd.to_datetime(dataframe0["Zeitstempel"])
dataframe0.set_index("Zeitstempel", inplace=True)
dataframe0["Identifikation"] = dataframe0["Identifikation"].astype(object)
dataframe0.dropna(axis=1, how="all", inplace=True) #delete empty columns

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
def plot_0(axis_0, axis_1, code):
    try:
        global xticklabels
        global yticklabels
        
        #identifikation
        #viel viel if
        code_foo = str(code)
        if code == "Identifikationscode":
            print("Gib deinen Indentifikationscode ein!")
        else:
            dataframe = dataframe0.loc[dataframe0["Identifikation"] == str(code)]
            
            if len(dataframe) == 0:
                dataframe = dataframe0.loc[dataframe0["Identifikation"] == int(code)]
                
                if len(dataframe) == 0:
                    print("Der angegebene Indentifikationscode ist nicht korrekt \noder du hast nicht an der Umfrage teilgenommen.")
            if len(dataframe) != 0:
                
                
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
                #durch sharey müssen ticks für ax1 nicht neu gesetzt werden
                fig, (ax, ax1) = plt.subplots(2, 1, figsize=(16, 20), sharey=True)
                plt.suptitle("Mind The Difference Between Correlation And Causation", y=0.9, fontsize=15)
                ax11 = plt.twinx(ax1) #twinx


                sns.scatterplot(data=dataframe, x=axis_0_numeric, y=axis_1_numeric, ax=ax, alpha=.7, edgecolor=None)
                sns.lineplot(data=dataframe, x=dataframe.index, y=axis_1_numeric, color="r", marker="^",
                            markevery=10, ax=ax1, label="axis_0", legend=None)
                sns.lineplot(data=dataframe, x=dataframe.index, y=axis_0_numeric, ax=ax11, color="maroon", linestyle="--",
                            label="axis_1, rechts", legend=None)


                #label
                ax.set(xlabel=str(axis_0), ylabel=str(axis_1))
                ax1.set(xlabel="Date", ylabel=str(axis_1))
                ax11.set(ylabel=str(axis_0))

                #legend
                h1, l1 = ax1.get_legend_handles_labels()
                h2, l2 = ax11.get_legend_handles_labels()
                ax1.legend(h1+h2, l1+l2, loc="lower center")

                #set ticks
                ax.set_xticks(range(len(xticklabels)))
                ax.set_xticklabels(xticklabels)

                ax.set_yticks(range(len(yticklabels)))
                ax.set_yticklabels(yticklabels)
                ax11.set_yticks(range(len(xticklabels)))
                ax11.set_yticklabels(xticklabels)


                #correlation
                corr = round(pd.Series(axis_0_numeric).corr(pd.Series(axis_1_numeric)),2)

                #textbox
                ax.text(0.0, -0.08, f"Correlation: {corr}", transform=ax.transAxes, fontsize=10,
                           verticalalignment='top', bbox={"boxstyle":'round', "facecolor":'wheat', "alpha":0.2})

    except Exception as e:
        print(f"""Ups, something went wrong \n
        Woran hats gelegen? \n
        {e, type(e), e.args}""")
        

#plot interactiv
parameter = [c for c in dataframe0.columns]
parameter.remove("Identifikation")
ipy.interact(plot_0, axis_0=parameter, axis_1=parameter, 
             code="Identifikationscode")
