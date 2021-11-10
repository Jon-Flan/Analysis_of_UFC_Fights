# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:06:37 2021

@author: jonathan.flanagan
"""
# imports
import pandas as pd


# import and create new dataframe
def import_adjust():
    # file
    file = ('../data/main_data_not_cleaned.csv')
    # dataframe
    df = pd.read_csv(file)
    
    # Fill na for Stance to 'Not Recorded
    df['Stance F_1'].fillna('Not Recorded', inplace=True)
    df['Stance F_2'].fillna('Not Recorded', inplace=True)
    
    # create new blank dataframes for fighters 1 and 2 per fight
    fighters_1 = pd.DataFrame(columns=['Weight class', 'Stance', 'Head Landed', 
                                       'Body Landed', 'Leg Landed'])
    
    fighters_2 = pd.DataFrame(columns=['Weight class', 'Stance', 'Head Landed',
                                       'Body Landed', 'Leg Landed'])

    # add the info for weight class, stance, strikes landed per body section for each fighters
    fighters_1[['Weight class', 'Stance', 
                'Head Landed', 'Body Landed', 
                'Leg Landed']] = df[['Weight class', 'Stance F_1', 
                                     'Head landed F_1','Body landed F_1',
                                     'Leg landed F_1']]
    fighters_2[['Weight class', 'Stance',
                'Head Landed', 'Body Landed', 
                'Leg Landed']] = df[['Weight class', 'Stance F_2', 
                                     'Head landed F_2','Body landed F_2',
                                     'Leg landed F_2']]

    # concatenate two dataframes into one
    df = pd.concat([fighters_1, fighters_2])

    # group the strikes by weight class and reset index
    df1 = df.groupby(['Weight class','Stance']).sum()
    df1.reset_index(inplace=True)
    

    return df1

# create the dataframe for visualising the strikes per body part
def create_strikes_frames(df1):

    # create a new dataframe that will be exported
    strikes = pd.DataFrame(columns=['Weight Class','Stance','Strike x', 'Strike y', 'Region', 'Strikes'])

    # expand the total for each strike type
    for x in range(len(df1)):
        i = df1.at[x, 'Head Landed'].astype(int)
        
        if i > 0:
            # create new rows for each weight class and assign random float at different sectors to visualize the strikes
            strikes_head = pd.concat([pd.DataFrame([[df1['Weight class'][x], df1['Stance'][x], 0.2,0.8, 'Head',1]],
                                                   columns=['Weight Class', 'Stance', 'Strike x', 'Strike y', 'Region', 'Strikes']) 
                                                   for n in range(i)], ignore_index=True)
            
            # append the created coordiantes to the the strikes data frame
            strikes = strikes.append(strikes_head)
     
    # expand the total for each strike type   
    for x in range(len(df1)):
        j = df1.at[x, 'Body Landed'].astype(int)

        if j > 0:
            # create new rows for each weight class and assign random float at different sectors to visualize the strikes
            strikes_body = pd.concat([pd.DataFrame([[df1['Weight class'][x], df1['Stance'][x], 0.1, 0.3, 'Body',1]], 
                                                   columns=['Weight Class', 'Stance', 'Strike x', 'Strike y', 'Region', 'Strikes']) 
                                                  for n in range(j)], ignore_index=True)
            
            # append the created coordiantes to the the strikes data frame
            strikes = strikes.append(strikes_body)
   
    # expand the total for each strike type   
    for x in range(len(df1)):
        k = df1.at[x, 'Leg Landed'].astype(int)
        
        if k > 0:
            # create new rows for each weight class and assign random float at different sectors to visualize the strikes
            strikes_leg = pd.concat([pd.DataFrame([[df1['Weight class'][x], df1['Stance'][x], 0.7, -0.4, 'Leg',1]], 
                                                  columns=['Weight Class', 'Stance', 'Strike x', 'Strike y', 'Region', 'Strikes']) 
                                                 for n in range(k)], ignore_index=True)
       
            
            # append the created coordiantes to the the strikes data frame
            strikes = strikes.append(strikes_leg)

    return strikes

def main():
    # get the info
    df1 = import_adjust()
    # get the created strikes dataframe with co ordinates associated with each strike region
    strikes_landed = create_strikes_frames(df1)
    strikes_landed
    # export to csv
    strikes_landed.to_csv('../data/strikes.csv', index=False)


# calling main function.
if __name__ == "__main__":
    main()