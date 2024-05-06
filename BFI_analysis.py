'''
Big-5 questionnaire analysis
'''
import re
import pandas as pd
from os.path import join as opj

# directory of the project
root_dir = opj('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri', 'questionnaire_datasets')

# open dataset with questionnaire results
df = pd.read_csv(opj(root_dir, 'BFI.csv'), sep=',')

# how many symbols in column name should be dropped to ease analysis
naming_int = 3

# rename columns from "BDI1" to 1 for readability
for cc in df.columns:
    # leave participant column untouced
    if not cc == 'participant':
        df.rename(columns={cc: cc[naming_int:]}, inplace = True)

########################################################################################
# Big-5 analysis
########################################################################################
# reverse the scores
reverse_scores = ['2', '6', '8', '9', '12', '18', '21', '23', '24', '27', '31', '34', '35', '37', '41', '43']

reverse_dict = {1:5, 2:4, 4:2, 5:1}

df[reverse_scores] = df[reverse_scores].replace(reverse_dict)

########################################################################################
# Big-5 scales
extrav_score = ['1', '6', '11', '16', '21', '26', '31', '36']
agree_score = ['2', '7', '12', '17', '22', '27', '32', '37', '42']
conscien_score = ['3', '8', '13', '18', '23', '28', '33', '38', '43']
neurotism_score = ['4', '9', '14', '19', '24', '29', '34', '39']
openness_score = ['5', '10', '15', '20', '25', '30', '35', '40', '41', '44']

# calculate sum within each scale and write it back to df
df['extraversion'] = df[extrav_score].sum(axis=1)
df['agreebleness'] = df[agree_score].sum(axis=1)
df['conscienceness'] = df[conscien_score].sum(axis=1)
df['neurotism'] = df[neurotism_score].sum(axis=1)
df['openness'] = df[openness_score].sum(axis=1)

# save df
df.to_csv(opj(root_dir, 'BFI.csv'), sep=',')