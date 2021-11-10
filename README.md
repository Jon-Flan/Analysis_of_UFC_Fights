# An Analysis of UFC Fights
An analysis of Mixed Martial Arts fights taken place under the promotion of the Ultimate Fighting Championship (UFC).
<br><br>
<img src="https://piglordmma.com/wp-content/uploads/2020/04/ufc-octagon.jpg">

# Data Collection
Data for this analysis has been collected through http://www.ufcstats.com <br>
<br>

### Initial Data
In total 10,658 unique url's where processed for the initial Datasets. Using this program initially <br>
to collect the data can take several hours to complete depending on computer hardware and internet bandwidth.<br>
    
For my personal computer hardware / internet bandwidth combination it took:<br>
**_Approx 5hrs_** to retrieve all data.<br>
<br>
Tech information on machine used to collect data is:<br>
 <table>
  <tr>
    <th>CPU</th>
    <th>Memory</th>
    <th>Connection Speed (Down)</th>
    <th>Connection Speed (Up)</th>
  </tr>
  <tr>
    <td>AMD Ryzen 5 3600X</td>
    <td>128GB @ 3600mhz</td>
    <td>60Mbps</td>
    <td>40Mbps</td>
  </tr>
</table> 
    
### Collecting the Data
To collect the Data, Get_Data.py can be ran which will update the data contained in the csv files.<br>
Get_Data.py is to be ran directly from the terminal/Command Line. <br>
Usage is:<br>
```
python Get_Data.py [options]
```
**python command may differ depending on your installation of python**
<br>
<br>
Options are:<br>
- option 1: All
- option 2: Fighters
- option 3: Events
<br>
Be careful not to run the program DURING a live a event.<br>
Your data will be skewed. <br>
<br>

**Running the Get_Data.py script will initiate these methods:**

<br>

#### 1. Getting the fighter info & normalizing
```python
def get_fighters():
    
    # Get the Fighter Basic Information
    fighters_df = scrp.get_fighters()
    
    # Get additional Fighter details
    fighter_details_df = scrp.get_further_fighter_details()
    
    if len(fighter_details_df) < 1:
        return 
    else:
        # Add a blank DOB column to the end of the DataFrame
        columns = len(fighters_df.columns)
        fighters_df.insert(columns,'DOB','')
        
        # Append DOB info to the fighters Dataframe
        for i in range(len(fighters_df)):
            fighters_df.loc[i, 'DOB'] = fighter_details_df['DOB'].loc[i]
    
    # More code below here for normalization......
    
    return fighters_df
    
# If no new fighters to get info on print msg and do nothing
if fighters_df == None:
    print('Done checking Fighters.')
# Otherwise print the info and append to existing csv
else:
    fighters_df.to_csv('../data/fighters.csv', mode='a', index=False, header=False)
```
#### 2. Getting the Events & normalizing
```Python
# Get the events and their details
def get_events():
    
    # Scrape for events
    event_details_df = scrp.get_event_details()
    
    if len(event_details_df) < 1:
        event_details_df = pd.DataFrame()
        
        return event_details_df
    else:
        #--------------------------------------------------------------------------------------------
        
        # Get the names of each fighter in the fight
        fighters = fighter_names(event_details_df.copy())
        event_details_df['Fighter 1'] = fighters[0]
        event_details_df['Fighter 2'] = fighters[1]
        
        #--------------------------------------------------------------------------------------------
        
        # Convert the control times in seconds for better calculations
        def round_times(frame, x):
            frame[[x+'_min', x+'_sec']] = frame[x].str.split(':', expand=True)
            frame[x+'_min'] = frame[x+'_min'].apply(pd.to_numeric, errors='coerce')
            frame[x+'_min'] = frame[x+'_min']*60
            frame[x+'_sec'] = frame[x+'_sec'].apply(pd.to_numeric, errors='coerce')
            frame[x] = frame[x+'_min'] + frame[x+'_sec']
            
            return frame[x]
            
        # More code below for naormalization .........
        
        
        # Reset the columns to what is needed
        event_details_df = event_details_df.reindex(columns=['W/L', 
                                                             'Fighter 1', 
                                                             'Fighter 2',
                                                             'Weight class', 
                                                             'Method',
                                                             'Round', 
                                                             'Time', 
                                                             'Event',
                                                             'Date'])
        
        return event_details_df
```
#### 3. Getting the Fight information from each event & normalizing
```Python
# Get the details of each fight at each event
def get_fights():
    
    # Scrape for the fight details
    fight_details_df = scrp.get_event_fight_details()
    
    if len(fight_details_df) < 1:
        fight_details_df = pd.DataFrame()
        
        return fight_details_df
    
    else:        
        #--------------------------------------------------------------------------------------------
               
        # Get the knockdowns for each fighter
        knock_downs_split = split(fight_details_df.copy(), 'KD')
        fight_details_df['KD F_1'] = knock_downs_split[0].apply(pd.to_numeric, errors='coerce')
        fight_details_df['KD F_2'] = knock_downs_split[1].apply(pd.to_numeric, errors='coerce')
        
        # Get the submission attempts by each fighter
        submissions_split = split(fight_details_df.copy(), 'Sub. att')
        fight_details_df['Sub. att F_1'] = submissions_split[0].apply(pd.to_numeric, errors='coerce')
        fight_details_df['Sub. att F_2'] = submissions_split[1].apply(pd.to_numeric, errors='coerce')
        
        # Get the reversals for each fighter
        reversals_split = split(fight_details_df.copy(), 'Rev.')
        fight_details_df['Rev. F_1'] = reversals_split[0].apply(pd.to_numeric, errors='coerce')
        fight_details_df['Rev. F_2'] = reversals_split[1].apply(pd.to_numeric, errors='coerce')
        
        # More Normalization code here ...................................
        
        # Final column cleaning and export completed dataframe
        frame = clean_dataframe(fight_details_df)    
        fight_details_df = frame
    
        return fight_details_df
```

# Data Info
There are 3 initial Datasets contained in the Data folder. <br>
- Fighter Information (fighters.csv)
- Events Information (events.csv)
- Fights Information (fight_data.csv)

### The Fighter information
This is the data information in the fighters.csv file <br>
*_(After normalization and export but before cleaning and dealing with null/missing values)_*<br><br>
![Fighter CSV Info](https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/fighter_dtypes_info%20copy.png)

### The Event Informaton
This is the data information in the events.csv file<br>
*_(After normalization and export but before cleaning and dealing with null/missing values)_*<br><br>
![Event CSV Info](https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/event_dtypes_info.png)

### The Fight Informaton
This is the data information in the fight_detaisl.csv file<br>
*_(After normalization and export but before cleaning and dealing with null/missing values)_*<br><br>
<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/fights_dtypes.png" width=30% height=30%>
<br><br>
![Fight CSV Info](https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/fights_info.png)

# Preprocessing
Once the data has been collected preprocessing can be begin. For this project instead of dealing with<br> 
null values in the fighter.csv straight away, the data from each csv is merged into one complete dataset,<br>
as this is where the analysis will take place and some figthers present in the figther information<br> 
may not have been in a UFC fight. Meaning some null information may not be part of the main dataset anyway.<br>
<br>
For the fight details, in early UFC events not all information is available as well as weight classes differ<br>
dramtically from what is used in Mixed Martial Arts promotions now, such as the Open Weight Class<br>
<br>
For these reasons all null, empty data as well as feature creation will be dealt with after merging.<br>

## Data Merging
The Data flow below shows from the website to a merged dataset before cleaning and feature creation. <br>
**Note:** Not all attributes from each dataset are used but are still taken during initial scraping and normalisation, <br>
to be used in the merging process and for data validation compared to the website during the data retreival.<br>
<br>
<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/data_flow/data_flow_pt1.png" width=100% height=100%>

## Merging the Data
To merge the data. After the collection process has completed and csv files are created,<br>
run the following command in terminal/comman prompt
**python command may differ depending on your installation of python**

```Terminal
python Merge_Data.py
```
Will initiate the process, NOTE: No additional arguments are needed for running this script.

```Python
def main():
    # get the final merged output
    data = merge_data()
    data
    print_and_export_data(data)
    
# merge the fighter info onto the fight info
    def get_merged_fighter_info():
        # copies of needed dataframes
        df_1 = events_and_fights.copy()
        df_f1 = fighter_1.copy()
        df_f2 = fighter_2.copy()
      
        # merge and drop dupliactes due to rematches and duplicate fighter info
        df_merged = pd.merge(df_1, df_f1, on=['Fighter 1'], how='left')
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event', 'Win decided by'], 
                                                keep='last')
        df_merged = pd.merge(df_merged, df_f2, on=['Fighter 2'], how='left')
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event', 'Win decided by'], 
                                                keep='last')
        
        # More merging methods inplace above and below this snippet
        
        data = get_merged_fighter_info()
    
    return data 
```

### Merged Data Info
The merged info is below before any initial visualization, cleaning, null handling, data type correction or feature creation<br>
Here we end up with 81 columns and 6350 rows. Each fight is broken out by the event basic details such as the event name and date,<br>
the winner/loser and how the fight ended. Then the each fighter details (Fighter 1 / Fighter 2) %& (F_1 / F_2) in the fight such as the<br> 
strikes landed and thrown per body section,as well as position. Then the personal info such as height, stance DOB and reach.<br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/merged_not_cleaned_dtypes.PNG" width=50% height=100%>

Table example: <br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/merged_not_cleaned_info.PNG" width=200% height=100% style="overflow-x:scroll">

# Tools Used
All tools and languages used, including packages from within each language <br>
<br>
#### Prerequisites are:
- Python3 is instaled
- R and R Studio are installed
- Anaconda3 is installed (Optional, any IDE capable of editing python is useable)

##### Installing Anaconda Instructions: <br>
**For Windows:** https://docs.anaconda.com/anaconda/install/windows/ <br>
**For Mac**: https://docs.anaconda.com/anaconda/install/mac-os/ <br>
**For Linux:** https://docs.anaconda.com/anaconda/install/linux/ <br>

##### Installing R & R Studio: <br>
Instructions here: https://rstudio-education.github.io/hopr/starting.html <br>

## Python 
Spyder IDE from within the Anaconda3 framework
#### Packages Imported:
- Pandas<br>
- Numpy <br>
- string<br>
- tqdm<br>
- BeautifulSoup<br>
- requests<br>
- sys<br>
- time<br>

## R
R Studio

