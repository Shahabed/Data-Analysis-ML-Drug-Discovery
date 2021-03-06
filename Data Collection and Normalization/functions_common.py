#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shahabedin Chatraee Azizabadi
"""

import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Split the list into groups ----------------------------------------
def get_reference_selection(df):
    df_sel = (df[(df['treatment'] == 'treatment01') |
                 (df['treatment'] == 'treatment02')|
                 (df['treatment'] == 'treatment03')|
                 (df['treatment'] == 'treatment04') |
                 (df['treatment'] == 'treatment05') |
                 (df['treatment'] == 'treatment06')]).copy()
    
    return df_sel
#---------------------------------------------------------------
def get_join_table(filename):
    tbl = pd.read_csv('../../---/--/plate_based_screening_list.csv')
    tbl.index = tbl['barcode']
    
    join_list = [] # Compared to a DataFrame, a list is much faster in loop appends due to the less memory usage 
    
    for index, row in tbl.iterrows():
        
        barcode = index
        donor = row['donor_1']
        
        layout_name = row['layout']
        layout_file_path = '../../----/data/layouts/'+layout_name+'.csv'
        
        layout = pd.read_csv(layout_file_path)
                
        # Each plate (each row from the main csv file) has several wells:
        for record in layout.itertuples():            
    
            well_key = record.well_key
            treatment = record.treatment
            
            # Join values from the two tables into one list
            join_list.append([barcode, donor, well_key, treatment])
    
    # make a datafarame from it
    col_names =  ['barcode', 'donor', 'well_key', 'treatment']
    join_table = pd.DataFrame(join_list, columns=col_names)
    return join_table
    
# -----------------------------------------------
def find_well_folder(parent_folder, plate_barcode, well_key):
     
    well_folder_pattern = '*' + plate_barcode + '?*' + well_key
    full_path_pattern = os.path.join(parent_folder, well_folder_pattern)        
    folders_found = glob.glob(full_path_pattern)
    
    # Important assumption: only one folder exists per each well
    if len(folders_found) > 0:
        return folders_found[0]
    else:
        return None

def read_well_features_from_agg_results(well_folder, desired_agg_type):
    
    try:        
        # load the features
        well_file = well_folder+'/aggregation_result.csv'        
        if os.path.exists(well_file):
            dfs = pd.read_csv(well_file)
        
            # To fix some columns
            dfs.rename(columns={'Unnamed: 0':'agg_type'}, inplace=True)
            
            # To select desired values
            selected_well_features = (dfs[dfs['agg_type'] == desired_agg_type]).copy()
            
            del dfs
            return selected_well_features            
        else:
            print("read_well_features_from_agg_results() WARNING: file does not exists:",well_file)
            return pd.DataFrame() # return an empty dataframe
    except Exception as e:
        print ("")
        print (">> read_well_features_from_agg_results():: FAILED ------------------------")
        print (">> well_folder:", well_folder)
        print ("exception: ", e)
        print ("")        
        return pd.DataFrame() # To return an empty dataframe

# ==================================================================

def read_well_features_from_agg_results_quan(well_file, desired_agg_type):
    
    try:        
        # load the features        
        if os.path.exists(well_file):
            dfs = pd.read_csv(well_file)
        
            # fix some columns
            dfs.rename(columns={'Unnamed: 0':'agg_type'}, inplace=True)
            
            # select desired values
            selected_well_features = (dfs[dfs['agg_type'] == desired_agg_type]).copy()
            
            del dfs
            return selected_well_features            
        else:
            print("read_well_features_from_agg_results_quan() WARNING: file does not exists:",well_file)
            return pd.DataFrame() # To return an empty dataframe
    except Exception as e:
        print ("")
        print (">> read_well_features_from_agg_results_quan():: FAILED ------------------------")
        print (">> well_file:", well_file)
        print ("exception: ", e)
        print ("")        
        return pd.DataFrame() # To return an empty dataframe
# ==================================================================
def get_dataframe_memory_usage(data):
    # We have the assumption that 1 MB = 1024 KBs.
    return round(data.memory_usage(deep=True).sum()/(2**20)) 


def pandas_groupby_to_list(groups, att_name):
    vals_list = []
    keys_list = []
    for key, vals in groups:
        vals_list.append(vals[att_name].values)
        keys_list.append(key)
    return keys_list, vals_list

# ==================================================================
# ==================================================================

def set_plot_style(labels_font_size = 10, tightlayout=True):
    plt.rcParams["figure.autolayout"] = tightlayout 
    plt.rcParams['font.size'] = labels_font_size
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelsize'] = labels_font_size
    plt.rcParams['axes.labelweight'] = 'bold'


def add_boxplot_legend(boxplots, legend_labels, fontsize=10, location='best'):
    legend_artists = []
    for bplot in boxplots:
        legend_artists.append(bplot['boxes'][0])
    plt.legend(legend_artists, legend_labels,
               prop={'size':fontsize, 'weight':'bold'}, loc=location, framealpha=0.5)    
