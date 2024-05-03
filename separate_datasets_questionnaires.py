'''
Create separate subset for each questionnaire in the dataset
'''
import pandas as pd
from os.path import join as opj


# directory of the project
root_dir = opj('/', 'home', 'lisz', 'Desktop', 'Time_project', 'time_fmri')

out_dir = opj(root_dir, 'questionnaire_datasets')

# open dataset with questionnaire results
df = pd.read_excel(root_dir + '/FMRI_participants.ods', engine='odf')

# list of questionnaires to extract from df, in this case it is the beginning of corresponding column names
list_quest = ['BFI', 'MQT', 'SEQ', 'MSSB']

# name of column with subjects' labels
sub_column = 'sub'

# drop the row (excluded subjects) based on empty values in the questionnaire
df.dropna(subset=['BFI1'], inplace=True)

########################################################################################
# separate questionnaires into different datasets
def create_subset(df, naming, sub_column):
    '''
    Creates a subset based on the beginning of the column name
    :param df: pandas dataframe
    :param naming:  a string with the beginning of the column name to create a subset
    :return: saved dataframe
    '''
    df_new = pd.DataFrame()
    for cc in df.columns:
        if cc.startswith(naming):
            # create new dataframe
            df_new[cc] = df[cc]
    df_new['participant'] = df[sub_column]
    #globals()[naming] = df_new
    #return df_new
    # save subset
    df_new.to_csv(out_dir + f'/{naming}.csv', index=False)


# loop through the questionnaires of interest to create an individual dataset for each of them
for qq in list_quest:
    create_subset(df, qq, sub_column)
