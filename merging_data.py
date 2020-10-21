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

# %% joining datasets on City (income.City, job.city or job.inferred_city) 
# OR on income.State_Name and jobs.state
# ~nulls #~on
merged_data = income.merge(data_sc_jobs[['city', 'job_title', 'crawl_timestamp', 'salary_offered']], left_on = 'City', right_on = 'city')
merged_data.head()

# %% drop redundant city data
# merged_data = merged_data.drop(['city'])
# merged_data.head()
