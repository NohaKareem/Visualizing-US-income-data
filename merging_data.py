# %%
import os
try:
    os.chdir(os.path.join(os.getcwd(), ''))
    print(os.getcwd())
except:
    pass

# %% import packages
import pandas as pd

# %% import Data Sc. job data
data_sc_jobs = pd.read_csv('./data/data_sc_jobs.csv')
data_sc_jobs.head()

# %% import kaggle income data
# handle UnicodeDecodeError w/ Latin encoding
income = pd.read_csv('./data/kaggle_income.csv', encoding = 'latin-1')
income.head()

# %% explore data_sc_jobs
unique_titles = data_sc_jobs.job_title.unique()
print(len(unique_titles), ' unique titles')
# dataScTitles = uniqueTitles.job_title.str.contains('Data Scientist')
# print(len(dataScTitles)) #~

# %% comparing states data in job data_sc_jobs, if both lower case 
# seems that data is different, given returned value False, albeit case-insensitivity
print(data_sc_jobs['city'].str.lower().equals(data_sc_jobs['inferred_state'].str.lower()))

# %% compare data results from 
# conclusion: merging on inferred_city results in more data to explore
merged_data1 = income.merge(data_sc_jobs[['city', 'job_title', 'crawl_timestamp', 'salary_offered']], left_on = 'City', right_on = 'city')
merged_data2 = income.merge(data_sc_jobs[['inferred_city', 'job_title', 'crawl_timestamp', 'salary_offered']], left_on = 'City', right_on = 'inferred_city')

print('# merged_data1 rows: ', len(merged_data1.index))
print('# merged_data2 rows: ', len(merged_data2.index))

# %% joining datasets 
merged_data = income.merge(data_sc_jobs[['city', 'job_title', 'crawl_timestamp', 'salary_offered']], left_on = 'City', right_on = 'city')
merged_data.head()

# %% drop redundant/unneeded city data
merged_data = merged_data.drop(['city', 'id', 'State_Code'], axis = 1)
merged_data.head()

# %% data cleaning to get median salary offered
# remove non-numeric chars and strings, for later parsing as int
merged_data['salary_offered'] = merged_data['salary_offered'].str.replace('$', '').str.replace('K', '').str.replace('k', '').str.replace('|','').str.replace('Equity','')

# %% split salary range into 2 cols (min, max)
merged_data[['min_salary', 'max_salary']] = merged_data.salary_offered.str.split(' - ', 1, expand = True)
merged_data.head()

# %% drop null salary values + parse to int + add median col
merged_data = merged_data[merged_data['salary_offered'].notna()]

merged_data['min_salary'] = merged_data['min_salary'].astype(int)
merged_data['max_salary'] = merged_data['max_salary'].astype(int)

# compute median of last 2 cols
merged_data['median_salary'] = merged_data.iloc[:, [len(merged_data.columns) - 2, len(merged_data.columns) - 1]].median(axis = 1)
merged_data.head()

# %% view shape
# salary_offered.shape
merged_data.shape

# %% drop redundant salary_offered
merged_data = merged_data.drop(['salary_offered'], axis = 1)
merged_data.head()

# %% export to csv
merged_data.to_csv('./data/merged_data.csv')
