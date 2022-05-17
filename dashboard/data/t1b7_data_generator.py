# Extract company table

import pandas as pd
df = pd.read_excel('notaclimat.xlsx')#, dtype={'Groupe': str})
df = df.drop([0])
companies = df.iloc[:, 0:1].rename(columns={'Groupe':'company_name'})#.astype(str)
companies

# Generating company_id variable

import base64
def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 


companies['company_id'] = [encode(x) for x in companies['company_name']]
companies = companies[['company_id', 'company_name']]

# Generating sector variable 

import random
from random_word import RandomWords
r = RandomWords()
t = range(companies.shape[0]+1)
sector = [r.get_random_word() for i in t]
companies['sector'] = pd.Series(sector)

# Generating revenue_year variable

years = [random.randint(2018, 2021) for i in t]
companies['revenue_year'] = pd.Series(years)
companies.dtypes

# Generating revenue variable

years = [random.uniform(1, 100) for i in t]
companies['revenue'] = pd.Series(years)
companies.dtypes

# Generating country_flag variable 

ris = {'country_flag': [':AC:',':AD:',':AE:',':AF:',':AG:',':AI:',':AL:',':AM:',':AO:',':AQ:',':AR:',':AS:',':AT:',':AU:',':AW:',':AX:',':AZ:',':BA:',':BB:',':BD:',':BE:',':BF:',':BG:',':BH:',':BI:',':BJ:']}
#companies = companies.append(ris, ignore_index=True)
tmp = pd.DataFrame(data=ris)
#test = test.append(ris, ignore_index=True)
companies['country_flag'] = tmp['country_flag']
#companies['country_flag']
#tmp

# Generating brand_logo variable

import pydenticon
#generator = pydenticon.Generator(10, 10)
fg = [ "rgb(45,79,255)",
       "rgb(226,121,234)",
       "rgb(30,179,253)",
       "rgb(232,77,65)",
       "rgb(49,203,115)",
       "rgb(141,69,170)" ]
bg = "rgb(255,255,255)"
generator = pydenticon.Generator(10, 10, foreground=fg, background=bg)

id = companies['company_id'].tolist()
id
for i in id:
    j = generator.generate(str(i), 240, 240, output_format="png")
    f = open("../assets/Pics/" + str(i) + ".png", "wb")
    f.write(j)
    f.close()

companies['brand_logo'] = 'assets/Pics/'+companies['company_id']+'.png'    

#identicon = generator.generate("Andros", 240, 240, output_format="png")
#f = open("./Pics/identicon.png", "wb")
#f.write(identicon)
#f.close()



# #+RESULTS:
# : /tmp/ipykernel_16393/2414179674.py:20: SettingWithCopyWarning: 
# : A value is trying to be set on a copy of a slice from a DataFrame.
# : Try using .loc[row_indexer,col_indexer] = value instead
# : 
# : See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
# :   companies['brand_logo'] = './Pics/'+companies['company_id']+'.png'



companies

# Generating top brands

import random
from random_word import RandomWords
r = RandomWords()
#s = r.get_random_words(limit=random.randrange(1, 8))
t = range(companies.shape[0])
brands = [r.get_random_words(limit=random.randrange(2, 8)) for i in t]
#dft = pd.DataFrame.from_records(brands)
companies['top_brands'] = pd.Series(brands)
companies
#df = companies({'top_brands':brands})
#df
#brands

# Export dataframe to csv

companies.to_csv(path_or_buf='t1b1-7.csv', sep=',', header=True, index=False)
