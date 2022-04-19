# extract company table

import pandas as pd
df = pd.read_excel('notaclimat.xlsx')#, dtype={'Groupe': str})
df = df.drop([0])
companies = df.iloc[:, 0:1].rename(columns={'Groupe':'company_name'})#.astype(str)
companies

# create IDs

import base64

def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 


companies['company_id'] = [encode(x) for x in companies['company_name']]
companies = companies[['company_id', 'company_name']]
#companies['Id'] = companies.Company.encode('utf-8', 'strict').encode('base64')
#companies['Id'] = (companies.Company.str.encode('utf-8', 'strict'))

# export dataframe to csv

companies.to_csv(path_or_buf='t1b1.csv', sep=',', header=True, index=False)
