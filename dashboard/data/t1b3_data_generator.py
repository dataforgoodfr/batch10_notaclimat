import pandas as pd

def generate_logo_path_variable(df_company_scores):
	df_company_scores.loc[df_company_scores['global_score'] == 1, 'global_score_logo_path'] = "../assets/Pics/1_not_released_reduction.png"
	df_company_scores.loc[df_company_scores['global_score'] == 2, 'global_score_logo_path'] = "../assets/Pics/2_totally_unsatisfactory_reduction.png"
	df_company_scores.loc[df_company_scores['global_score'] == 3, 'global_score_logo_path'] = "../assets/Pics/3_unsatisfactory_reduction.png"
	df_company_scores.loc[df_company_scores['global_score'] == 4, 'global_score_logo_path'] = "../assets/Pics/4_partial_reduction.png"
	df_company_scores.loc[df_company_scores['global_score'] == 5, 'global_score_logo_path'] = "../assets/Pics/5_strong_reduction.png"
	df_company_scores.loc[df_company_scores['global_score'] == 6, 'global_score_logo_path'] = "../assets/Pics/6_very_strong_reduction.png"
	return df_company_scores

print('Loading data...', end="")
df = pd.read_excel("notaclimat_en.xlsx")
df_correlation_table_global_score = pd.read_excel("scores_correlation_table.xlsx", 
												sheet_name="Affichage score global")
df_correlation_table_direct_complete_score = pd.read_excel("scores_correlation_table.xlsx", 
												sheet_name="Affich score direct ou complet")
print('done.')

print('Processing data...', end="")
df = df[['Group', 'Global score', 'C1 direct score', 'C2 complete score', 'Comment']]
df_correlation_table_global_score = df_correlation_table_global_score[['Global score', 'Color Hex', 'Short label']]
df_correlation_table_direct_complete_score = df_correlation_table_direct_complete_score [['Direct or complete score', 'Color Hex', 'Short label']]

df = df.merge(df_correlation_table_global_score, how='inner', on='Global score', suffixes=('_df', '_global_score'))
df = df.merge(df_correlation_table_direct_complete_score, how='inner', 
	left_on='C1 direct score', right_on='Direct or complete score', suffixes=(None, '_direct_score'))
df = df.merge(df_correlation_table_direct_complete_score, how='inner', 
	left_on='C2 complete score', right_on='Direct or complete score', suffixes=(None, '_complete_score'))

df = df.drop(columns=['Direct or complete score', 'Direct or complete score_complete_score'])

renamed_columns = {
	'Group': 'company_name',
	'Global score': 'global_score',
	'Color Hex': 'global_score_hexa_color_code',
	'Short label': 'global_score_short_label',
	'C1 direct score': 'direct_score',
	'Color Hex_direct_score': 'direct_score_hexa_color_code',
	'Short label_direct_score': 'direct_score_short_label',
	'C2 complete score': 'complete_score',
	'Color Hex_complete_score': 'complete_score_hexa_color_code',
	'Short label_complete_score': 'complete_score_short_label',
	'Comment': 'comment'
}
df = df.rename(columns=renamed_columns)
df = generate_logo_path_variable(df)
print('done.')

df.to_csv(path_or_buf='t1b3.csv', sep=',', header=True, index=False)
print('Data exported.')