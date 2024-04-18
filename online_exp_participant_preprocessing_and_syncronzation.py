'''
For online experiments: match subject number from the behavioral experiment,
questionnaire and sociodemographic data
'''

import pandas as pd
import os
import zipfile
import shutil

# project directory
project_dir = os.path.join('/', 'home', 'lisz', 'Desktop', 'ITRI_project', 'analysis_itri')

# directory with questionnaires data
questionnaire_dir = os.path.join(project_dir, 'main_exp_data')

# directory of the data from behavioral experiment, 'data' folder will be created automatically during extraction
beh_exp_dir = os.path.join(project_dir, 'data')

# directory of the sociodemographic data
sociodemogr_dir = os.path.join(questionnaire_dir, 'data_questionnaires_and_socio')

# how many rows should be in the correct (full) csv from the main behavioral experiment
main_exp_len = 32

############################################################################
# unarchive zip files into a new folder in the project folder
############################################################################

# dirpath - the current directory being processed, the one which contains zip files
# dirnames - list of subdirectories in dirpath
# filenames - list of files in dirpath
for dirpath, dirnames, filenames in os.walk(project_dir):
    # iterate through each file in the folder
    for filename in filenames:
        # find in the folder: whether current file is .zip
        if filename.endswith(".zip"):
            zip_path = os.path.join(dirpath, filename)
            # Open the .zip in read ('r') mode
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # iterate through each file inside .zip
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith(".csv"):
                        # Extract the .csv file to the project folder
                        # it will create a folder "data"
                        zip_ref.extract(file_info, project_dir)

############################################################################
# Check the main experiment: doubles, length of the file, whether it is empty or not
# and delete the broken files
############################################################################
'''
set() - creates unordered list of items and if value already exists there, it will not double it
and will safe only unique values
'''
# make empty sets
list_sub = set()
repeated_sub = set()

# open the folder with extracted data
for filename in os.listdir(beh_exp_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(beh_exp_dir, filename)
        # without try empty files would ruin the code
        try:
            df = pd.read_csv(file_path)
            if "participant" in df.columns:
                # unique participants' values from the df
                unique_participants = set(df["participant"].unique())
                # check overlaps between current file's participant label and
                # the list_sub (participants who were checked before)
                # if .intersection gives no matches, nothing is added to repeated_sub below
                # repeated_sub - subjects which have more than file appearance in the dataset
                repeated_sub.update(unique_participants.intersection(list_sub))
                # add participant label to the list with all participants labels
                list_sub.update(unique_participants)
            if len(df)<main_exp_len: # lenth of the full dataset
                print(f'Short file {filename}')
                # delete short files
                os.remove(file_path)
        # check empty file and delete it
        except pd.errors.EmptyDataError:
            print(f"Empty CSV file: {filename}")
            # delete empty file
            os.remove(file_path)

# Print participant values that appear in multiple CSV files
for s in repeated_sub:
    print(f"Participant {s} appears in several csv")

############################################################################
# Open folder, find file from Pavlovia Survey (starts with "responses")
# find file from Prolific (starts with "prolific")
# merge these files based on the "participant" column in questionnaires and then check duplicates
############################################################################
def merge_questionnaires_sociodemogr(subfolder):
    '''
    Merge questionnaires and sociodemogr csv
    :param subfolder: beginning of the subfolder name
    :return: 
    '''
    df_dir = os.path.join(sociodemogr_dir, f'{subfolder}_quest')
    # open folder and open files
    for root,dirs,files in os.walk(df_dir):
        for file in files:
            if file.startswith("responses"):
                question = pd.read_csv(os.path.join(df_dir,file))
            if file.startswith("prolific"):
                socio = pd.read_csv(os.path.join(df_dir,file))
    # rename participant column in the Prolific file
    socio['participant'] = socio['Participant id']
    # merge based on 'participant' column with an inner merge
    merged_df = pd.merge(question, socio, on='participant', how='inner')
    return merged_df


q_s_emissions_negative = merge_questionnaires_sociodemogr('emissions_negative')
q_s_emissions_positive = merge_questionnaires_sociodemogr('emissions_positive')
q_s_money_negative = merge_questionnaires_sociodemogr('money_negative')
q_s_money_positive = merge_questionnaires_sociodemogr('money_positive')


# check and drop duplicates
def drop_doubles(df):
    # Check for duplicates based on the 'participant' column
    duplicate_mask = df.duplicated(subset='participant', keep='first')
    # Check if any duplicates were found
    for i in duplicate_mask:
        if i == True:
            # Extract the duplicated 'participant' values and convert them to a list
            duplicated_participants = df[duplicate_mask]['participant'].tolist()
            # Print the list of duplicated 'participant' values
            print(f'Dublicated participant {duplicated_participants}')
            # Drop the duplicates based on the 'participant' column, keeping the first occurrence
            df = df.drop_duplicates(subset='participant', keep='first')
    # Return the DataFrame with duplicates dropped
    return df

q_s_money_negative = drop_doubles(q_s_money_negative)
q_s_money_positive = drop_doubles(q_s_money_positive)
q_s_emissions_negative = drop_doubles(q_s_emissions_negative)
q_s_emissions_positive = drop_doubles(q_s_emissions_positive)

# combine 4 groups' datasets into one
dataframes = [q_s_emissions_negative, q_s_emissions_positive,
              q_s_money_negative, q_s_money_positive]
combined_df = pd.concat(dataframes, ignore_index=True)

# create subject list
subjects_list = set(combined_df['participant'])
len(subjects_list)

############################################################################
# check corresponding csv files between main exp, questionnaires and sociodemogr data
############################################################################

# iterate through main exp data files
for root,dirs,files in os.walk(beh_exp_dir):
    for file in files:
        csv_path = os.path.join(beh_exp_dir, file)
        df = pd.read_csv(csv_path)
        # cause we can only compare set to set, that's why here is set
        participant_n = set(df["participant"].unique())
        # is csv participant is in the subject list made from questionnarie merged file?
        if participant_n.issubset(subjects_list):
            pass
        else:
            print(f'{participant_n} is not in q and s list')
            print(file)
            os.remove(csv_path)


# save filtered data to group subfolders
for csv_file in os.listdir(beh_exp_dir):
    if csv_file.endswith(".csv"):
        csv_path = os.path.join(beh_exp_dir, csv_file)
        try:
            df = pd.read_csv(csv_path)
        except pd.errors.EmptyDataError:
            print(f"Empty dataset in {csv_file}")
            continue  # Move on to the next file

        df.dropna(subset=['group'], inplace=True)
        group_label = df['group'].unique()  # Access the 28th row (index 27)

        if group_label == ['Emissions-positive']:
            destination_folder = os.path.join(questionnaire_dir, 'data_emissions_positive')

        elif group_label == ['Emissions-negative']:
            destination_folder = os.path.join(questionnaire_dir, 'data_emissions_negative')

        elif group_label == ['Money-positive']:
            destination_folder = os.path.join(questionnaire_dir, 'data_money_positive')

        elif group_label == ['Money-negative']:
            destination_folder = os.path.join(questionnaire_dir, 'data_money_negative')

        else:
            print(f"Unknown group value in {csv_file}")
            continue  # Skip files with unknown group values

        # Check if the destination folder exists, and create it if not
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, csv_file)
        # Copy the file from the initial folder to the destination folder
        shutil.copy(csv_path, destination_path)

