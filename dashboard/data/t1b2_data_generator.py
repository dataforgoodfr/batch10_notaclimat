import pandas as pd
import base64

# functions

def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 

# Generating company_id variable

import base64
def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 

cols_for_calculation = [
    'company_name',
    'C1 direct score',
    'C1 initial value',
    'C1 final value', 
    'C1 unit', 
    'C1 initial date',
    'C1 final date', 
    'C1 2deg final', 
    'C1 1,8deg final',
    'C1 1,5deg final',
    'C2 complete score', 
    'C2 complete level',
    'C2 reduction',
    'C2 initial value', 
    'C2 final value',
    'C2 unit',
    'C2 initial date',
    'C2 final date', 
    'C2 2deg final',
    'C2 1,8deg final',
    'C2 1,5deg final',
    'E1 commitment direct',
    'E1 score commitment direct',
    'E1 reduction',
    'E1 unit',
    'E2 commitment complete',
    'E2 score commitment',
    'E2 reduction',
    'E2 unit'
]


# variables
# For global score references
list_reference = ['Unrevealed', 'TotallyInsufficient', 'Insufficient', 'Partial', 'Strong', 'VeryStrong']

# For C1 and C2 direct scores references
list_reference2 = ['Non publiée', 'Vers + 4°C', 'Entre +2°C et +3°C', '2°C', 'Bien moins de 2°C', '1,5°C', 'n.a. (trop récente)']
list_hexcolors_direct = ['#820000', '#C00000', '#FF8939', '#FEC800', '#8CDF41', '#0DB800', '#C00000']
list_scores = ['1','2','3','4','5','6','99']


# Extract origin table

df = pd.read_excel("../data/BDD Surcouche pour dataviz_v03.xlsx")
#df = df.drop([0])

# Pre-treatment

t1b2_data = df.rename(columns={'Group':'company_name'})
t1b2_data['company_id'] = [encode(x) for x in t1b2_data['company_name']]


# Calculating score performance to choose color
direct_score_reference_table = pd.DataFrame(
  data={
    'direct_score': list_scores, 
    'direct_score_label': list_reference2, 
    'hexcolor':list_hexcolors_direct
    }
  )

   
# Filtering data & adding reference columns

df_filtered = t1b2_data[cols_for_calculation].fillna(0).copy()

df_filtered = df_filtered.replace(to_replace={'n.a.':0})

df_filtered= df_filtered.astype({
  'C1 direct score': int, 
  'C2 complete score': int,
  'C2 final value': float, 
  'C2 2deg final': float, 
  'C2 1,8deg final': float,
  'C2 1,5deg final': float,
  'C1 final value': float, 
  'C1 2deg final': float, 
  'C1 1,8deg final': float,
  'C1 1,5deg final': float,
  'E1 score commitment direct': int,
  'E1 commitment direct': float, 
  'E2 score commitment': int,
  'E2 commitment complete': float
}).astype({
  'C1 direct score': str, 
  'C2 complete score': str,
  'E1 score commitment direct': str,
  'E2 score commitment': str
})    


# C1 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='C1 direct score', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'c1_label', 'hexcolor': 'c1_color'}
).drop(
  columns=['direct_score']
)

# E1 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='E1 score commitment direct', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'e1_label', 'hexcolor': 'e1_color'}
).drop(
  columns=['direct_score']
)
  
  
# C2 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='C2 complete score', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'c2_label', 'hexcolor': 'c2_color'}
).drop(
  columns=['direct_score']
)


# E2 direct score references
df_filtered = pd.merge(
  df_filtered, 
  direct_score_reference_table, 
  how='left', 
  left_on='E2 score commitment', 
  right_on='direct_score'
).rename(
  columns={'direct_score_label':'e2_label', 'hexcolor': 'e2_color'}
).drop(
  columns=['direct_score']
)


# Updating column names to match variables list
# TODO
df_filtered = df_filtered.rename(
  columns={
    'C1 direct score': 'direct_score',
    'c1_label': 'direct_score_short_label',
    'c1_color': 'direct_score_hexa_color_code',
    'C2 complete score': 'complete_score',
    'c2_label': 'complete_score_short_label',
    'c2_color': 'complete_score_hexa_color_code',
    'E1 commitment direct': 'direct_score_commitments',
    'E1 score commitment direct': 'direct_rounding_score_commitments',
    'e1_color': 'direct_ambition_hexa_color_code',
    'E2 commitment complete': 'complete_score_commitments',
    'E2 score commitment': 'complete_rounding_score_commitments',
    'e2_color': 'complete_ambition_hexa_color_code',
    'C1 final value':'c1_final_value', 
    'C1 2deg final':'c1_2_deg_final', 
    'C1 1,8deg final':'c1_1_8_deg_final',
    'C1 1,5deg final':'c1_1_5_deg_final',
    'C2 final value':'c2_final_value', 
    'C2 2deg final':'c2_2_deg_final', 
    'C2 1,8deg final':'c2_1_8_deg_final',
    'C2 1,5deg final':'c2_1_5_deg_final',
    'C1 initial date': 'c1_initial_date',
    'C1 final date': 'c1_final_date',
    'C2 initial date': 'c2_initial_date',
    'C2 final date': 'c2_final_date',
  })

# Exporting
df_filtered.to_csv(
  path_or_buf='t1b2.csv',
  sep=',', 
  header=True, 
  index=False
)