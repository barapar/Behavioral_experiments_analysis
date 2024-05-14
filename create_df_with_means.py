
import pandas as pd
from statistics import mean
from os.path import join as opj


experiment = opj('Sixth_exp', 'Sixth_cleaned_data')

root_dir = opj('/', 'home', 'lisz', 'Desktop', 'Time_project', 'Time_project_exp')
project_file = opj(root_dir, experiment, 'all_with_outliers.csv')

df = pd.read_csv(project_file)

df_new = pd.DataFrame(columns=['participant', 'pause_duration', 'mean'])

# create and sort pause list
pause_list = sorted(df['pause_duration'].unique())

def create_row(sub, pause, df_new):
    subset = df.loc[(df['participant'] == sub) & (df['pause_duration'] == pause)]
    mean_value = mean(subset['key_resp_rt'])
    new_row = {'participant': sub,
               'pause_duration': pause,
               'mean': mean_value}
    print(new_row)
    df_new = pd.concat([df_new, pd.DataFrame([new_row])], ignore_index=True)
    print(mean_value)
    return df_new

for sub in df['participant'].unique():
    for pause in pause_list:
        df_new = create_row(sub, pause, df_new)

df_new.to_csv(opj(root_dir, experiment, 'means_pause_duration.csv'))
