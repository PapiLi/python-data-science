
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[4]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    df = pd.DataFrame(columns=["State", "RegionName"])
    file = open('university_towns.txt','r')
    for line in file:
        line = line.rstrip()
        if(len(line)==0):
            continue
        if line.endswith("[edit]"):
            state = line[:-6]
            #print(state)
        else:
            index = line.find(' (')
            if(index!=-1):
                city = line[:index]
            else:
                city = line
            #print(city)
            df.loc[len(df)] = [state,city]
    return df
get_list_of_university_towns().head()


# In[5]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=[0,1,2,3,4]+([temp for temp in range(6,220)]),usecols=[4,6],keep_default_na=False,names=['Season','GDP'])
    recessionStart = []
    for i in range(1,len(GDP)-1):
        if (GDP.iloc[i-1]["GDP"]>GDP.iloc[i]["GDP"]) and (GDP.iloc[i]["GDP"]>GDP.iloc[i+1]["GDP"]):
            recessionStart.append(GDP.iloc[i]["Season"])
    return recessionStart[0]
get_recession_start()


# In[6]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=[0,1,2,3,4]+([temp for temp in range(6,220)]),usecols=[4,6],keep_default_na=False,names=['Season','GDP'])
    recessionEnd = []
    for i in range(2,len(GDP)):
        if (GDP.iloc[i-2]["GDP"]<GDP.iloc[i-1]["GDP"]) and (GDP.iloc[i-1]["GDP"]<GDP.iloc[i]["GDP"]):
            recessionEnd.append(GDP.iloc[i]["Season"])
    for season in recessionEnd:
        if season>get_recession_start():
            answer = season
            break
    return answer
get_recession_end()


# In[10]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=[0,1,2,3,4]+([temp for temp in range(6,220)]),usecols=[4,6],keep_default_na=False,names=['Season','GDP'])
    gdp = GDP[(GDP["Season"]>=get_recession_start()) & (GDP["Season"]<=get_recession_end())]
    gdp = gdp[gdp["GDP"]==min(gdp["GDP"])]
    return gdp["Season"].values[0]
get_recession_bottom()


# In[7]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housingDataRaw = pd.read_csv('City_Zhvi_AllHomes.csv')
    housingDataRaw['State'] = housingDataRaw['State'].map(states)
    housingDataRaw.set_index(['State','RegionName'],inplace=True)
    dateRange = pd.date_range('2000-01','2016-9',freq='M').strftime('%Y-%m').tolist()
    housingData = housingDataRaw[dateRange]
    result = pd.DataFrame(index=housingData.index)
    for year in range(2000,2017):
        for season in range(4):
            seasons = []
            for month in range(1,4):
                m= str(year)+'-'+str(season*3+month).zfill(2)
                seasons.append(m)
            if year==2016 and season==2:
                seasons = seasons[:-1]
            columnName = str(year)+'q'+str(season+1)
            #print('Year'+str(year)+' season'+str(season+1)+' started')
            if(columnName<'2016q4'):
                cols = housingData[seasons]
                result[columnName] = np.mean(cols,axis=1)
                    
            #print('Year'+str(year)+' season'+str(season+1)+' finished')     
    return result
convert_housing_data_to_quarters().head()


# In[16]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    recessionStart = get_recession_start()
    recessionBottom = get_recession_bottom()
    data = convert_housing_data_to_quarters()
    data = data.loc[:,recessionStart:recessionBottom]
    data = data.reset_index()
    def calculateRatio(row):
        return (row[recessionStart] - row[recessionBottom])/row[recessionStart]
    
    data['ratio'] = data.apply(calculateRatio,axis=1)
    
    universityTown = get_list_of_university_towns()['RegionName']
    universityTown = set(universityTown)

    def isUniversityTown(row):
        #check if the town is a university towns or not.
        if row['RegionName'] in universityTown:
            return 1
        else:
            return 0
    data['isUniversityTown'] = data.apply(isUniversityTown,axis=1)
    
    
    notUniversity = data[data['isUniversityTown']==0].loc[:,'ratio'].dropna()
    isUniversity  = data[data['isUniversityTown']==1].loc[:,'ratio'].dropna()
    if notUniversity.mean() < isUniversity.mean():
        temp =  'non-university town'
    else:
        temp = 'university town'
    p = list(ttest_ind(notUniversity, isUniversity))[1]
    result = (p<0.01,p,temp)
    return result
run_ttest()


# In[ ]:



