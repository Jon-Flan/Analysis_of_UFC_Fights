# An Analysis of UFC Fights
An analysis of Mixed Martial Arts fights taken place under the promotion of the Ultimate Fighting Championship (UFC).
<br><br>
<img src="https://piglordmma.com/wp-content/uploads/2020/04/ufc-octagon.jpg">
# Abstract

# Data Collection
Data for this analysis has been collected through http://www.ufcstats.com <br>
<br>

### Initial Data
In total 10,658 unique url's where processed for the initial Datasets. Using this program initially <br>
to collect the data can take several hours to complete depending on computer hardware and internet bandwidth.<br>
    
For my personal computer hardware / internet bandwidth combination it took:<br>
**_Approx 5hrs_** to retrieve all data.(this can be adjusted as sleep timer set at 1 second after each url)<br>
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
null values straight away, the data from each csv is merged into one complete dataset,<br>
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
<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/data_flow/data_flow_pt1.png" width=75% height=75%>

## Merging the Data
After the collection process has completed and csv files are created,<br>
run the following command in terminal/comman prompt
**python command may differ depending on your installation of python**

```Terminal
python Merge_Data.py
```
Running the above command will initiate the merging process.<br>
NOTE: No additional arguments are needed for running this script.<br>

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
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1',
                                                      'Fighter 2', 
                                                      'Event', 
                                                      'Win decided by'],keep='last')
        df_merged = pd.merge(df_merged, df_f2, on=['Fighter 2'], how='left')
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1', 
                                                      'Fighter 2', 
                                                      'Event', 
                                                      'Win decided by'], keep='last')
        
        # More merging methods inplace above and below this snippet
        
        data = get_merged_fighter_info()
    
    return data 
```

### Merged Data Info
The merged info below is before any initial visualization, cleaning, null handling, data type correction or feature creation<br>
Here we end up with 81 columns and 6350 rows. Each fight is broken out by the events basic details such as the event name and date,<br>
the winner/loser, and how the fight ended. Then each fight is broken down by each fighters details, denoted by (Fighter 1 / Fighter 2) and (F_1 / F_2),<br> 
details include the strikes landed and thrown per body section,as well as position, as well as personal info such as height, stance DOB and reach.<br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/merged_not_cleaned_dtypes.PNG" width=50% height=100%>

Table example: <br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/imgs/merged_not_cleaned_info.PNG" width=200% height=100% style="overflow-x:scroll">

## Data Cleaning
Data cleaning is carried out with Jupyter notebook in a scripting fashion. <br>
The goal is to take the merged dataset and remove any unneeded features as well as deal with <br>
the null/empty/missing values.

### Initial Feature Selection
Initially when first visually exploring the dataset there are certain features that are not needed<br>
Either because they have no bearing on analysis or they are duplicated else where. <br>
<br>
Initial Feature Removal:
- First Name F_1 (duplicated in Fighter 1)
- Last Name F_1 (duplicated in Fighter 1)
- Nickname F_1 (not needed)
- First Name F_2 (duplicated in Fighter 2)
- Last Name F_2 (duplicated in Fighter 2)
- Nickname F_2 (not needed)
<br>

```Python
# remove the initial uneeded features from the dataset
def remove_initial_features():
    # create dataframe 
    frame = import_and_create_df()
    df = frame.copy()
    
    # remove columns that aren't needed
    df.drop(['First Name F_1', 'First Name F_2',
             'Last Name F_1', 'Last Name F_2',
             'Nickname F_1', 'Nickname F_2'] , axis=1, inplace=True)
    
    return df
```

In the weight classes column there are two weight classes that are not needed. <br>
Open weight and Super heavyweight. The reason being is only one fight has ever occured in Super heavyweight <br>
and Open weight was from the initial tournaments held by the UFC. Both of these are before the Unified Rules implimentation. <br>
<br>
With these weight classes removed the below graph shows the weight classes and number of fights remaining. <br>
<br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/graphs/Weight%20Classes.jpg" width=50% height=50%>

### Initial Exploration & Null - Empty Values
After the first few features that can be removed from the analysis by visual inspection, the dataset is <br>
expllored column by column and Null/Empty values are dealt with along the way.
#### Win Types
Win types are the type of decision in the "Win decided by" column, some of these can be split out to make<br>
the features easier to clean up and analyse later.<br>
<br>

<img src="https://github.com/Jon-Flan/Analysis_of_UFC_Fights/blob/main/graphs/Win%20Types.jpg" width=50% height=50%>

Because the decisions types are seperated out by U-DEC, M-DEC and S-DEC, they can be combined into one level Decision and <br>
move the U(Unanimous), M(Majority) and S(Split) into the Win Method column <br>


Other Win decided types are:
- CNC (Could not continue)
- DQ (Disqualification)
- Other
- Overturned
<br>
These fights are fights that had no clear winner, CNC is where a fighter could not continue and no fighter was
declared the winner. DQ is where one fighter was disqualified. Other we can investigate and Overturned is
usually where a decision for the fight was overturned due to mitgating circumstances, usually a failed drug test
after the fight. CNC, Other and Overturned were declared a no contest and no winner was decided. Where as the DQ had a winner announced.
<br>
Adjusting Decision methods and removing CNC, Other and Overturned.
<br>
<br>

```Python
# Convert the Win decided by to Decision and make additions to the Win Method Column 

df_win_types['Win Method'] = np.where(df_win_types['Win decided by']=='M-DEC',
                                      'Majority Decision',
                                      df_win_types['Win Method'])

df_win_types['Win Method'] = np.where(df_win_types['Win decided by']=='S-DEC',
                                      'Split Decision',
                                      df_win_types['Win Method'])

df_win_types['Win Method'] = np.where(df_win_types['Win decided by']=='U-DEC',
                                      'Unanimous Decision',
                                      df_win_types['Win Method'])

df_win_types['Win decided by'] = np.where(df_win_types['Win decided by'].str.contains('DEC'),
                                          'Decision',
                                          df_win_types['Win decided by'])



# filtering out the unneeded Win by types
win_types_df_1 = df_win_types[~df_win_types['Win decided by'].str.contains('Other',na=False) & 
                        ~df_win_types['Win decided by'].str.contains('Overturned',na=False) &
                        ~df_win_types['Win decided by'].str.contains('CNC',na=False)]


```



### Clean Data set

# Knowledge Discovery

## Secondary Exploration

## Feature Creation

## Tertiary Exploration

# Insights

# Further Information

## Tools Used
### Python 
Spyder IDE from within the Anaconda3 framework <br>
Jupyter Notebook from within the Anaconda3 framework <br>

#### Prerequisites are:
- Python3 is instaled
- Anaconda3 is installed

##### Installing Anaconda Instructions: <br>
**For Windows:** https://docs.anaconda.com/anaconda/install/windows/ <br>
**For Mac**: https://docs.anaconda.com/anaconda/install/mac-os/ <br>
**For Linux:** https://docs.anaconda.com/anaconda/install/linux/ <br>

#### Packages Imported:

 <table>
  <tr>
    <th>Package</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>Pandas</td>
    <td>For URL scraping, Data manipulation and prepartion</td>
  </tr>
  <tr>
    <td>Numpy</td>
    <td>Data manipulation and preparation</td>
  </tr>
  <tr>
    <td>string</td>
    <td>Generating strings</td>
  </tr>
    <tr>
    <td>tqdm</td>
    <td>Console output for progress bar</td>
  </tr>
    <tr>
    <td>BeautifulSoup</td>
    <td>URL scraping</td>
  </tr>
  <tr>
    <td>requests</td>
    <td>html connectivity</td>
  </tr>
  <tr>
    <td>sys</td>
    <td>Exit and output to console</td>
  </tr>
  <tr>
    <td>time</td>
    <td>Setting sleep time between URL visits</td>
  </tr>
  <tr>
    <td>Matplotlib</td>
    <td>Visualization and data exploration</td>
  </tr>
  <tr>
    <td>Seaborn</td>
    <td>Visualization and data exploration</td>
  </tr>
  <tr>
      <td>Sklearn</td>
      <td>Random Forest Classification</td>
  </tr>
</table> 

