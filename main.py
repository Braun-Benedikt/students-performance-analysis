import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from itertools import combinations

survey_df = pd.read_csv('./data/stats_survey.csv')
survey_columns = ['time', 'sex', 'matric_avg', 'study_year', 'faculty',
                  'study_year_avg', 'accom_status', 'monthly_allowance', 'scholarship',
                  'wkly_stdy_hrs', 'socializing_freq', 'drinks_per_night', 'missed_classes',
                  'failed_modules', 'relationship', 'approval', 'parent_strength']
print(survey_df.columns)
survey_df.columns = survey_columns
print(survey_df.columns)
print(survey_df.corr())

# create combinations of column pairs
categorical_columns = survey_df.select_dtypes(include=['object']).columns
column_pairs = combinations(categorical_columns, 2)

# chi-squared test for each pair of columns
for pair in column_pairs:
    cross_tab = pd.crosstab(survey_df[pair[0]], survey_df[pair[1]])
    chi2, p, _, _ = chi2_contingency(cross_tab)
    if p < 0.05:
        print(f"Chi-Quadrat-Wert für {pair[0]} und {pair[1]}:", chi2)
        print(f"p-Wert für {pair[0]} und {pair[1]}:", p)
        print("------")

# create a strip plot
category_order = ['0', '1-3', '3-5', '5-8', '8+']
plt.figure(figsize=(8, 6))
sns.stripplot(x='wkly_stdy_hrs', y='study_year_avg', data=survey_df, order=category_order, jitter=True)
avg_per_category = survey_df.groupby('wkly_stdy_hrs')['study_year_avg'].mean().reset_index()
for i, row in avg_per_category.iterrows():
    plt.scatter(row['wkly_stdy_hrs'], row['study_year_avg'], color='red', label='Average' if i == 0 else None)
plt.title('Impact of additional studying on GPA ')
plt.xlabel('Additional studying (hrs)')
plt.ylabel('2023 GPA (%)')
plt.show()
