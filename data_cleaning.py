import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))


df = pd.read_csv('data.csv')

# Remove job postings without salary number
df = df[df['Salary Estimate'] != '-1']

# Simplify dataset to Glassdoor est. only
df['glassdoor est'] = df['Salary Estimate'].apply(lambda x: 1 if 'glassdoor est.' in x.lower() else 0)
df = df[df['glassdoor est'] == 1]

# Feature engineering on the salary column 
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))
df['min_salary'] = minus_Kd.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = minus_Kd.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2
df = df.drop(['Salary Estimate', 'glassdoor est', 'min_salary', 'max_salary'],1)

# Clean company names
df['Company Name'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'].split('\n')[0], axis = 1)

# Create City & State columns
df['City'] = df['Location'].apply(lambda x: x.split(',')[0] if ',' in x.lower() else x)
df['State'] = df['Location'].apply(lambda x: x.split(',')[1] if ',' in x.lower() else x) 
df = df.drop(['Location'],1)

# Calculate the age of company 
df['Founded'] = df['Founded'].apply(lambda x: np.nan if x in ['Company - Private', '-1', 'Company - Public', 'Unknown', 'Contract', 'Nonprofit Organization', 'Self-employed'] else x)
df['Age'] = df['Founded'].apply(lambda x: x if x is np.nan else 2021 - int(x))
df = df.drop(['Founded'],1)

# Convert company into lower case
df['Size'] = df['Size'].str.lower()

# Creating a function to encapsulate preprocessing job titles & descriptions, by removing special characters and stop words
def processing(df):
    df['Job Title'] = df['Job Title'].apply(lambda x: ' '.join(x.split()))
    df['Job Title'] = df['Job Title'].apply(lambda x: re.sub(r'[^\w\s]',' ', x.lower()))
    df['Job Description'] = df['Job Description'].apply(lambda x: ' '.join(x.split()))
    df['Job Description'] = df['Job Description'].apply(lambda x: re.sub(r'[^\w\s]','', x.lower()))
    df['Job Description'] = df['Job Description'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopWords]))                                               
    return(df)

# Classifying job titles into each category
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'data analyst'
    elif 'machine learning' in title.lower():
        return 'machine learning engineer'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'data science related jobs'

# Classifying job levels into each category
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'vp' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower()or 'experienced' in title.lower() or 'iii' in title.lower() or 'research' in title.lower() or 'manager' in title.lower():
        return 'Senior'
    elif 'intermediate' in title.lower() or 'staff' in title.lower() or 'ii' in title.lower():
        return 'Mid'
    elif 'jr' in title.lower() or 'junior' in title.lower() or 'intern' in title.lower() or 'student' in title.lower()or 'associate' in title.lower():
        return 'Junior'
    else:
        return 'Not Specified'

# Process data based on above defined functions 
df = processing(df)
df['Job'] = df['Job Title'].apply(title_simplifier)
df['Seniority'] = df['Job Title'].apply(seniority)

# Python
df['Python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
# R studio 
df['R'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)

# SQL 
df['SQL'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

# AWS 
df['AWS'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

# Excel
df['Excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

# Google Cloud
df['GCP'] = df['Job Description'].apply(lambda x: 1 if 'google cloud' in x.lower() or 'gcp' in x.lower() else 0)

# Microsoft Azure
df['Azure'] = df['Job Description'].apply(lambda x: 1 if 'microsoft azure' in x.lower() or 'azure' in x.lower() else 0)

# Spark
df['Spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

# PyTorch
df['PyTorch'] = df['Job Description'].apply(lambda x: 1 if 'pytorch' in x.lower() else 0)

# TensorFlow
df['TensorFlow'] = df['Job Description'].apply(lambda x: 1 if 'tensorflow' in x.lower() or 'tf' in x.lower() else 0)

# Tableau
df['Tableau'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)

# Keras
df['Keras'] = df['Job Description'].apply(lambda x: 1 if 'keras' in x.lower() else 0)

