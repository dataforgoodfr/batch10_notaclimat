import pandas as pd
import base64

# functions

def encode(text):
  btext = text.encode('utf-8')[:6]
  return base64.b64encode(btext).decode("utf-8") 


# variables
# For global score references
list_reference = ['Unrevealed', 'TotallyInsufficient', 'Sufficient', 'Partial', 'Strong', 'VeryStrong']

# For C1 and C2 direct scores references
list_reference2 = ['Non publiée', 'Vers + 4°C', 'Entre +2°C et +3°C', '2°C', 'Bien moins de 2°C', '1,5°C', 'n.a. (trop récente)']
list_hexcolors_direct = ['820000', 'C00000', 'FF8939', 'FEC800', '8CDF41', '0DB800', 'C00000']
list_scores = ['1','2','3','4','5','6','99']


# Extract origin table

df = pd.read_excel("../data/BDD Surcouche pour dataviz_v03.xlsx")
df = df.drop([0])

# Pre-treatment

t1b4_data = df.rename(columns={'Group':'company_name'})
t1b4_data['company_id'] = [encode(x) for x in t1b4_data['company_name']]


# Calculating global performance to choose pic
ref_dict = {}
for i, t in enumerate(list_reference):
    ref_dict[i+1] = t
    
global_score_reference_table = pd.DataFrame.from_dict(
  ref_dict, 
  orient='index'
  ).reset_index(
    ).rename(
      columns={'index':'global_score',0:'global_score_label'}
      )
    
global_score_reference_table['global_score'] = global_score_reference_table['global_score'].astype('str')


# Calculating score performance to choose color
direct_score_reference_table = pd.DataFrame(
  data={
    'direct_score': list_scores, 
    'direct_score_label': list_reference2, 
    'hexcolor':list_hexcolors_direct
    }
  )


# Generating filtered df once company is selected
df_filtered = t1b4_data[['company_name','Sector', 'Global score','C1 direct score','C2 complete score']]

df_filtered= df_filtered.astype(
  {'Global score': int,
   'C1 direct score': int, 
   'C2 complete score': int
  }
).astype(
  {'Global score': str,
   'C1 direct score': str, 
   'C2 complete score': str
  }
)    
    
# Filtering data & adding reference columns

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
              
# Global score references
df_filtered = pd.merge(
  df_filtered, 
  global_score_reference_table, 
  how='left', 
  left_on='Global score',
  right_on='global_score'
).drop(
  columns=['global_score']
)


# Adding the global score image
df_filtered['global_score_pic'] = 'assets/frames/climate_score/Frame_'+ df_filtered['global_score_label']+'.png' 


# Exporting
df_filtered.to_csv(
  path_or_buf='t1b4.csv',
  sep=',', 
  header=True, 
  index=False
)