import pandas as pd
import re 

data = pd.read_csv('asset-v1-data.csv')

df1 = data[0:3]
df2 = data[4:]

df1['Treatment'] = 0
df2['Treatment'] = 1

df = pd.concat([df1, df2]).reset_index()

df.drop(columns =['index','Treatment A'], inplace = True)

df = df.replace(['?','unknown', 'nan'], pd.NA)

df['Complications?'] = df['Complications?'].replace(to_replace = '[yYes]', value = 1, regex = True) 

df['Complications?'] = df['Complications?'].replace(to_replace = '[nNo]', value = 0, regex = True) 

df['Patient gender'] = df['Patient gender'].replace(regex = ['f','F','emale'], value = 1)
df['Patient gender'] = df['Patient gender'].replace(regex = ['M','m', 'male'], value = 0)

df['Tumor stage'] = df["Tumor stage"].replace(['II', 'III','IV'],[2,3,4])

df['Tumor stage'] = (df["Tumor stage"]).astype(int)

start_date = pd.to_datetime('1-1-1999')

df['Date enrolled'] = pd.to_datetime(df['Date enrolled'])

df['Date enrolled'] = df['Date enrolled'] - start_date

df["Height"]= df["Height"].astype(str)

df["Height"]= df["Height"].str.strip('cm')

#Function to convert pie or inches into cm

def pie_to_cm(string):
    str_lst = re.split("['\"]", string)
    if len(str_lst) == 3:
        result = (int(str_lst[0])* 30.48) +  int(str_lst[1]) * 2.54
    elif len(str_lst) == 2:
        result = int(str_lst[0]) * 2.54
    else:
        result = str_lst[0]
    return result

df['Height'] = df['Height'].apply(pie_to_cm)

df['Date enrolled']= df['Date enrolled'].fillna(pd.Timedelta(seconds=0))

df = df.fillna(-9)
