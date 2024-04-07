"""
Calculate coefficient of variation
And run rm ANOVA

"""
import os
import pandas as pd
import pingouin as pg
pd.options.display.max_colwidth = 100


# set the experiment to analyse
exp = 'Reproduction_exp'
# subfolder within experiment
sub_folder = 'Reprod_cleaned_data'
# filename with behavioral data
file_name = 'all_with_outliers.csv'

# data root
parent_dir = '/home/lisz/Desktop/Time_project/Time_project_exp'

# behavioral data dataset
df = pd.read_csv(os.path.join(parent_dir, exp, sub_folder, file_name))

def calculate_cv(df):
    '''
    Calculate coefficient of variation: SD / mean
    '''
    cv = df['key_resp_rt'].std() / df['key_resp_rt'].mean()
    return cv

############################################################################
### time bins CV analysis
############################################################################
# create a new list to save participant, bin number and its CV value
list_cv = []
for pp in df['participant'].unique():
    # subset for 1 subject
    subset = df[df['participant'] == pp]
    # set the size of the bin, here: divide dataset in 10 bins
    bin_length = int(len(subset)/10)
    # iterate through each bin
    for n in range(1,11):
        if n == 1:
            # for the first bin, start with 0
            # create a subset with defined boundaries
            bin_n = subset.iloc[0:bin_length]
        else:
            # start et the end of the previous bin
            start_bin = (n-1) * bin_length
            # define end by summing the length of the bin
            end_bin = start_bin + bin_length
            # create a subset with defined boundaries
            bin_n = subset.iloc[start_bin:end_bin]
        # calculate cv for the bin defined above
        cv = calculate_cv(bin_n)
        # add participant, bin number and its CV value
        list_cv.append([pp, n, cv])

# convert list to dataframe
df_cv = pd.DataFrame(data=list_cv, columns=['participant', 'time_bin', 'cv'])

############################################################################
# run rmANOVA, time bin within analysis
result_time = pg.rm_anova(data=df_cv, correction=True, dv='cv', within=['time_bin'], subject='participant',
                          detailed=True, effsize='np2')
# post hoc t-test
posthocs_time = pg.pairwise_tests(dv='cv', within='time_bin', subject='participant',
                                  padjust='bonf', effsize='eta-square', data=df_cv)
# Filter significant comparisons
sign_ph_time = posthocs_time[posthocs_time['p-corr'] < 0.05]

############################################################################
### pause duration CV analysis
############################################################################
# create a new list to save participant, bin number and its CV value
list_pd = []
for pp in df['participant'].unique():
    # subset for 1 subject
    subset = df[df['participant'] == pp]
    # iterate through pause durations
    for dd in subset['pause_duration'].unique():
        # CV of a subset with one pause duration
        cv = calculate_cv(subset[subset['pause_duration'] == dd])
        # add participant, bin number and its CV value
        list_pd.append([pp, dd, cv])

df_pd = pd.DataFrame(data=list_pd, columns=['participant', 'pause_duration', 'cv'])
##############################################################################
# run rmANOVA, pause duration within analysis
result_pd = pg.rm_anova(data=df_pd, correction=True, dv='cv', within='pause_duration', subject='participant',
                          detailed=True, effsize='np2')

############################################################################
### eccentricity CV analysis
############################################################################
# create a new list to save participant, bin number and its CV value
list_cc = []
for pp in df['participant'].unique():
    # subset for 1 subject
    subset = df[df['participant'] == pp]
    for cc in subset['eccentricity'].unique():
        # CV for a subset with 1 eccentricity
        cv = calculate_cv(subset[subset['eccentricity'] == cc])
        # add participant, bin number and its CV value
        list_cc.append([pp, cc, cv])

df_cc = pd.DataFrame(data=list_cc, columns=['participant', 'eccentricity', 'cv'])
##############################################################################
# run rmANOVA, time bin as a dependent variable
result_cc = pg.rm_anova(data=df_cc, correction=True, dv='cv', within='eccentricity', subject='participant',
                        detailed=True, effsize='np2')
