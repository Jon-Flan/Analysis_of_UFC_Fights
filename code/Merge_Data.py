# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:38:01 2021

@author: jonathan.flanagan

    This script is used to merge the datasets into one dataset for analysis. 
        - Taking the Fight details for each fighter in each fight and left joining onto each Fight Event
        - Taking the Fighters personal details such as height, weight, stance etc from fighter info
          and left join to get a the full data set. 

"""
# imports
import pandas as pd
import numpy as np


#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


def main():
    # get the final merged output
    data = merge_data()
    data
    print_and_export_data(data)


#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


def merge_data():
    
    # get the files needed and create the data frames
    def get_dataframes():
    
        file1 = ('../data/fighters.csv')
        file2 = ('../data/events.csv')
        file3 = ('../data/fights.csv')
        
        fighters = pd.read_csv(file1)
        events = pd.read_csv(file2)
        fights = pd.read_csv(file3)
        
        return fighters, events, fights
    
    
    # assign the datframes 
    dataframes = get_dataframes()
    fighters = dataframes[0].copy()
    events = dataframes[1].copy()
    fights = dataframes[2].copy()
    
    
    #--------------------------------------------------------------------------------------------------------------------
    
    
    # reverse fight info for fighter 1 and fighter 2 to fill in blanks when merging
    def reverse_fight_info():
        frame = fights.copy()
        
        frame_map = {'Fighter 1':'Fighter 2', 'KD F_1':'KD F_2', 'Sig. str. landed F_1':'Sig. str. landed F_2',
           'Sig. str. thrown F_1':'Sig. str. thrown F_2', 'Sig. str. % F_1':'Sig. str. % F_2', 'Total str. landed F_1':'Total str. landed F_2',
           'Total str. thrown F_1':'Total str. thrown F_2', 'Td completed F_1':'Td completed F_2', 'Td attempted F_1':'Td attempted F_2',
           'Td % F_1':'Td % F_2', 'Sub. att F_1':'Sub. att F_2', 'Rev. F_1':'Rev. F_2', 'Ctrl F_1':'Ctrl F_2', 'Head landed F_1':'Head landed F_2',
           'Head thrown F_1':'Head thrown F_2', 'Body landed F_1':'Body landed F_2', 'Body thrown F_1':'Body thrown F_2',
           'Leg landed F_1':'Leg landed F_2', 'Leg thrown F_1':'Leg thrown F_2', 'Distance landed F_1':'Distance landed F_2',
           'Distance thrown F_1':'Distance thrown F_2', 'Clinch landed F_1':'Clinch landed F_2', 'Clinch thrown F_1':'Clinch thrown F_2',
           'Ground landed F_1':'Ground landed F_2', 'Ground thrown F_1':'Ground thrown F_2' }
        
        frame.columns = [{**frame_map, **{v:k for k,v in frame_map.items()}}.get(x, x) for x in frame.columns]
        
        return frame
     
    
    #--------------------------------------------------------------------------------------------------------------------
    
    
    # complete the fight details merge of the data frames
    def get_merged_fights():
        # set the fights to opposite criteria for merging variable
        fights_reversed_info = reverse_fight_info()
        
        
        # merge fight details onto event (twice, once as normal, second time with fighter info reversed)
        df = pd.merge(events, fights, on=['Fighter 1', 'Fighter 2', 'Event'], how='left')
        df = pd.merge(df, fights_reversed_info, on=['Fighter 1', 'Fighter 2', 'Event'], how='left')
        
        # Columns for fight info that are wanted, (x and y versions are the merged versions)
        fight_cols = ['KD F_1', 'Sig. str. landed F_1',
                      'Sig. str. thrown F_1', 'Sig. str. % F_1', 
                      'Total str. landed F_1','Total str. thrown F_1', 
                      'Td completed F_1', 'Td attempted F_1',
                      'Td % F_1', 'Sub. att F_1', 'Rev. F_1', 'Ctrl F_1',
                      'Head landed F_1', 'Head thrown F_1', 'Body landed F_1', 
                      'Body thrown F_1','Leg landed F_1', 'Leg thrown F_1',
                      'Distance landed F_1', 'Distance thrown F_1', 'Clinch landed F_1', 
                      'Clinch thrown F_1','Ground landed F_1','Ground thrown F_1', 
                      'KD F_2','Sig. str. landed F_2','Sig. str. thrown F_2', 
                      'Sig. str. % F_2','Total str. landed F_2', 'Total str. thrown F_2', 
                      'Td completed F_2','Td attempted F_2', 'Td % F_2', 'Sub. att F_2', 
                      'Rev. F_2', 'Ctrl F_2','Head landed F_2', 'Head thrown F_2', 
                      'Body landed F_2','Body thrown F_2', 'Leg landed F_2', 'Leg thrown F_2',
                      'Distance landed F_2', 'Distance thrown F_2', 'Clinch landed F_2',
                      'Clinch thrown F_2', 'Ground landed F_2', 'Ground thrown F_2']
        
        # for each of the fight cols, if the x version is blank fill with the y version
        for x in fight_cols:    
            df[x] = np.where(df[x+'_x'].notnull(), df[x+'_x'], df[x+'_y'])
        
        # reindex the colummns to structure wanted 
        df = df.reindex(columns=[ # Event and main details of Fight
                                 'Event', 'Date', 'Weight class', 'Winner', 'Loser',
                                 'Win decided by', 'Win Method', 'Round', 'Time', 
                                  # Fighter 1 Details
                                 'Fighter 1', 'KD F_1', 'Sig. str. landed F_1',
                                 'Sig. str. thrown F_1', 'Sig. str. % F_1', 'Total str. landed F_1',
                                 'Total str. thrown F_1', 'Td completed F_1', 'Td attempted F_1',
                                 'Td % F_1', 'Sub. att F_1', 'Rev. F_1', 'Ctrl F_1', 'Head landed F_1',
                                 'Head thrown F_1', 'Body landed F_1', 'Body thrown F_1',
                                 'Leg landed F_1', 'Leg thrown F_1', 'Distance landed F_1',
                                 'Distance thrown F_1', 'Clinch landed F_1', 'Clinch thrown F_1',
                                 'Ground landed F_1', 'Ground thrown F_1',
                                  #  Fighter 2 Details
                                 'Fighter 2', 'KD F_2','Sig. str. landed F_2', 'Sig. str. thrown F_2', 
                                 'Sig. str. % F_2','Total str. landed F_2', 'Total str. thrown F_2', 
                                 'Td completed F_2','Td attempted F_2', 'Td % F_2', 'Sub. att F_2', 
                                 'Rev. F_2', 'Ctrl F_2','Head landed F_2', 'Head thrown F_2', 'Body landed F_2',
                                 'Body thrown F_2', 'Leg landed F_2', 'Leg thrown F_2',
                                 'Distance landed F_2', 'Distance thrown F_2', 'Clinch landed F_2',
                                 'Clinch thrown F_2', 'Ground landed F_2', 'Ground thrown F_2'])
        
        # drop the 2 duplicates created during the merge for fights that have two entries, 
        # Win decided by isnt in right table so is used now to drop the 2 extra entries that have a re-match
        df = df.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event', 'Win decided by'])
        
        
        return df
    
    
    # Merge the fight details and print info
    events_and_fights = get_merged_fights()
    
    
    #--------------------------------------------------------------------------------------------------------------------
    
    
    # duplicate the fighter DataFrame to be used as Fighter 1 or 2
    def fighters_duplicate():
        # copy the fighters
        fighter_1 = fighters.copy()
        fighter_2 = fighters.copy()
        
        # list of column names in fighter to be changed
        fighter_cols = ['First Name','Last Name','Nickname', 'Height', 'Weight', 'Reach',
                        'Stance', 'Wins', 'Losses', 'Draws', 'DOB']
        
        #--------------------------------------------------------------------------------------------------------------------
        
        # add a rename columned with the fighters name
        def rename(frame, x,y):
            frame['First Name'] = frame['First Name'].fillna('')
            frame['Last Name'] = frame['Last Name'].fillna('')
            frame['Fighter '+ x] = frame['First Name'] + ' ' + frame['Last Name']
            frame['Fighter '+x] = frame['Fighter '+x].str.strip()
            
            for i in fighter_cols:
                frame.rename(columns={i: i+y}, inplace=True)
            
            return frame
        
        # add the columns
        fighter_1 = rename(fighter_1, '1', ' F_1' )
        fighter_2 = rename(fighter_2, '2', ' F_2')
        
        
        return fighter_1, fighter_2
    
    
    # duplicate the dataframe
    fighters_duplicated = fighters_duplicate()
    fighter_1 = fighters_duplicated[0]
    fighter_2 = fighters_duplicated[1]   
    del fighters_duplicated  
    
    #--------------------------------------------------------------------------------------------------------------------
    
    # merge the fighter info onto the fight info
    def get_merged_fighter_info():
        # copies of needed dataframes
        df_1 = events_and_fights.copy()
        df_f1 = fighter_1.copy()
        df_f2 = fighter_2.copy()
      
        # merge and drop dupliactes due to rematches and duplicate fighter info
        df_merged = pd.merge(df_1, df_f1, on=['Fighter 1'], how='left')
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event', 'Win decided by'], keep='last')
        df_merged = pd.merge(df_merged, df_f2, on=['Fighter 2'], how='left')
        df_merged = df_merged.drop_duplicates(subset=['Fighter 1', 'Fighter 2', 'Event', 'Win decided by'], keep='last')
        
        # reindex columns 
        df_merged = df_merged.reindex(columns=[# Event and main details of Fight
                                               'Event', 'Date', 'Weight class', 'Winner', 'Loser', 'Win decided by',
                                               'Win Method', 'Round', 'Time', 
                                               # Fighter 1 Details
                                               'Fighter 1','First Name F_1', 'Last Name F_1', 
                                               'Nickname F_1','Height F_1', 'Weight F_1', 'Reach F_1', 'Stance F_1', 'Wins F_1',
                                               'Losses F_1', 'Draws F_1', 'DOB F_1', 
                                               # Fighter 1 Fight Details
                                               'KD F_1','Sig. str. landed F_1', 'Sig. str. thrown F_1', 'Sig. str. % F_1',
                                               'Total str. landed F_1', 'Total str. thrown F_1', 'Td completed F_1',
                                               'Td attempted F_1', 'Td % F_1', 'Sub. att F_1', 'Rev. F_1', 'Ctrl F_1',
                                               'Head landed F_1', 'Head thrown F_1', 'Body landed F_1',
                                               'Body thrown F_1', 'Leg landed F_1', 'Leg thrown F_1',
                                               'Distance landed F_1', 'Distance thrown F_1', 'Clinch landed F_1',
                                               'Clinch thrown F_1', 'Ground landed F_1', 'Ground thrown F_1',
                                               # Fighter 2 Details
                                               'Fighter 2','First Name F_2', 'Last Name F_2',
                                               'Nickname F_2', 'Height F_2', 'Weight F_2', 'Reach F_2', 'Stance F_2',
                                               'Wins F_2', 'Losses F_2', 'Draws F_2', 'DOB F_2',
                                               # Fighter 2 Fight Details
                                               'KD F_2', 'Sig. str. landed F_2', 'Sig. str. thrown F_2',
                                               'Sig. str. % F_2', 'Total str. landed F_2', 'Total str. thrown F_2',
                                               'Td completed F_2', 'Td attempted F_2', 'Td % F_2', 'Sub. att F_2',
                                               'Rev. F_2', 'Ctrl F_2', 'Head landed F_2', 'Head thrown F_2',
                                               'Body landed F_2', 'Body thrown F_2', 'Leg landed F_2',
                                               'Leg thrown F_2', 'Distance landed F_2', 'Distance thrown F_2',
                                               'Clinch landed F_2', 'Clinch thrown F_2', 'Ground landed F_2',
                                               'Ground thrown F_2' ])
        
        
        return df_merged
    
    data = get_merged_fighter_info()
    
    return data 


#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


# print the data details
def print_and_export_data(data):
    data.info()
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 15)
    pd.set_option('display.width', 1000)
    print(data)
    data.to_csv('../data/main_data_not_cleaned.csv', index=False)

#-------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


# calling main function.
if __name__ == "__main__":
    main()


