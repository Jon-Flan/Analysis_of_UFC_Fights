# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:06:37 2021

@author: jonathan.flanagan

This script is for plotting made coordinates for visualization
in tableau for head body leg strikes both landed and missed

"""
# imports
import pandas as pd


# import and create new dataframe
def import_adjust():
    # file
    file = ('../data/main_data.csv')
    # dataframe
    df = pd.read_csv(file)
    
    # add missed columns
    df['Head missed F_1'] = df['Head thrown F_1'] - df['Head landed F_1']
    df['Body missed F_1'] = df['Body thrown F_1'] - df['Body landed F_1']
    df['Leg missed F_1'] = df['Leg thrown F_1'] - df['Leg landed F_1']
    
    df['Head missed F_2'] = df['Head thrown F_2'] - df['Head landed F_2']
    df['Body missed F_2'] = df['Body thrown F_2'] - df['Body landed F_2']
    df['Leg missed F_2'] = df['Leg thrown F_2'] - df['Leg landed F_2']
    
    # Filter only Fights that contain Southpaw versus Orthodox
    df = df[(df['Stance F_1'].str.contains('Orthodox') & df['Stance F_2'].str.contains('Southpaw')) |
            (df['Stance F_2'].str.contains('Orthodox') & df['Stance F_1'].str.contains('Southpaw'))]
    
    
    # create new blank dataframes for fighters 1 and 2 per fight
    fighters_1 = pd.DataFrame(columns=['Weight class', 'Stance', 'Head Landed', 
                                       'Body Landed', 'Leg Landed', 'Head Missed', 
                                       'Body Missed', 'Leg Missed'])
    
    fighters_2 = pd.DataFrame(columns=['Weight class', 'Stance', 'Head Landed',
                                       'Body Landed', 'Leg Landed', 'Head Missed', 
                                       'Body Missed', 'Leg Missed'])

    # add the info for weight class, stance, strikes landed per body section for each fighters
    fighters_1[['Weight class', 'Stance', 
                'Head Landed', 'Body Landed', 
                'Leg Landed', 'Head Missed', 
                'Body Missed', 'Leg Missed']] = df[['Weight class', 'Stance F_1', 
                                     'Head landed F_1','Body landed F_1',
                                     'Leg landed F_1', 'Head missed F_1',
                                     'Body missed F_1', 'Leg missed F_1']]
    fighters_2[['Weight class', 'Stance',
                'Head Landed', 'Body Landed', 
                'Leg Landed','Head Missed', 
                'Body Missed', 'Leg Missed']] = df[['Weight class', 'Stance F_2', 
                                     'Head landed F_2','Body landed F_2',
                                     'Leg landed F_2', 'Head missed F_2',
                                     'Body missed F_2', 'Leg missed F_2']]

    # concatenate two dataframes into one
    df = pd.concat([fighters_1, fighters_2])

    # group the strikes by weight class and reset index
    df1 = df.groupby(['Weight class','Stance']).sum()
    df1.reset_index(inplace=True)
    

    return df1



def strikes(frame, append_frame, type_, location, x_cor, y_cor):
    # expand the total for each strike type
    for x in range(len(frame)):
        i = frame.at[x, type_].astype(int)
        
        if i > 0:
            # create new rows for each weight class and assign random float at different sectors to visualize the strikes
            strikes = pd.concat([pd.DataFrame([[frame['Weight class'][x], frame['Stance'][x], x_cor, y_cor, location,1]],
                                                   columns=['Weight Class', 'Stance', 'Strike x', 'Strike y', 'Region', 'Strikes']) 
                                                   for n in range(i)], ignore_index=True)
            
            # append the created coordiantes to the the strikes data frame
            append_frame = append_frame.append(strikes)
            
    return append_frame        


def create_strikes():            
    # create a new dataframe for landed strikes
    strikes_landed = pd.DataFrame(columns=['Weight Class','Stance','Strike x', 'Strike y', 'Region', 'Strikes'])
    # create a new dataframe for thrown strikes
    strikes_missed = pd.DataFrame(columns=['Weight Class','Stance','Strike x', 'Strike y', 'Region', 'Strikes'])
    
    # imported dataframe
    df = import_adjust()
    
    # strikes landed 
    strikes_landed = strikes(df, strikes_landed, 'Head Landed', 'Head', 0.2, 0.8)          
    strikes_landed = strikes(df, strikes_landed, 'Body Landed', 'Body', 0.1, 0.3)          
    strikes_landed = strikes(df, strikes_landed, 'Leg Landed', 'Leg', 0.7, -0.4)   
    
    # strikes thrown 
    strikes_missed = strikes(df, strikes_missed, 'Head Missed', 'Head', 1.4, 0.8)          
    strikes_missed = strikes(df, strikes_missed, 'Body Missed', 'Body', 1.4, 0.3)          
    strikes_missed = strikes(df, strikes_missed, 'Leg Missed', 'Leg', 1.4, -0.4)        
    
    # join the two dataframes togthers
    strikes_total = pd.concat([strikes_landed, strikes_missed]) 
    
    return strikes_total
            


def main():
    # get the info
    df = create_strikes()

    # export to csv
    df.to_csv('../data/strikes.csv', index=False)


# calling main function.
if __name__ == "__main__":
    main()