import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from itertools import combinations
from sklearn.cluster import KMeans

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
        print(f'Chi-Quadrat-Wert für {pair[0]} und {pair[1]}:', chi2)
        print(f'p-Wert für {pair[0]} und {pair[1]}:', p)
        print('------')

for column in survey_df.select_dtypes(include=['object']).columns:
    if column != 'time':
        unique_values = survey_df[column].unique()
        print(f"Mögliche Ausprägungen der Spalte '{column}': {unique_values}")

# the selected columns are expected to have the strongest correlation with study_year_avg
selected_columns = ['study_year', 'monthly_allowance', 'scholarship', 'wkly_stdy_hrs', 'socializing_freq',
                    'drinks_per_night', 'missed_classes', 'parent_strength', 'relationship']

# mapping the ordinal categories to numeric values
ordinal_categories_map = {
    '1st Year': 1,
    '2nd Year': 2,
    '3rd Year': 3,
    '4th Year': 4,
    'Postgraduate': 5,
    'R 4001- R 5000': 1,
    'R 5001 - R 6000': 2,
    'R 6001 - R 7000': 3,
    'R 7001 - R 8000': 4,
    'R 8000+': 5,
    'No': 0,
    'Yes (NSFAS, etc...)': 1,
    'Yes': 1,
    '0': 0,
    '1-3': 1,
    '3-5': 2,
    '5-8': 3,
    '8+': 4,
    '1': 1,
    'Only weekends': 1.5,
    '2': 2,
    '3': 3,
    '4+': 4,
    'Distant': 0,
    'Fair': 1,
    'Close': 2,
    'Very close': 3
}

for column in selected_columns:
    survey_df[column] = survey_df[column].map(ordinal_categories_map).fillna(survey_df[column])
print(survey_df.corrwith(survey_df['study_year_avg']))

# TODO check n_clusters
# perform k-Means clustering
kmeans = KMeans(n_clusters=3)
survey_df['cluster'] = 0
survey_df.dropna(subset=selected_columns)['cluster'] = kmeans.fit_predict(survey_df[selected_columns].dropna())

# print cluster centers
print("Cluster Centers:")
print(kmeans.cluster_centers_)

# TODO most/all 2 dimensional plots do not make sense here
# scatter plots of all possible combinations painted by cluster
for i, column1 in enumerate(selected_columns):
    for j, column2 in enumerate(selected_columns):
        if i < j:
            plt.scatter(survey_df[column1], survey_df[column2], c=survey_df['cluster'], cmap='viridis')
            plt.xlabel(column1)
            plt.ylabel(column2)
            plt.title(f'Scatterplot von {column1} vs. {column2}')
            plt.colorbar(label='Cluster')
            plt.show()

# scatter plots of 2023 GPA and the selected columns
for column in selected_columns:
    plt.scatter(survey_df[column], survey_df['study_year_avg'])
    plt.title(f'Impact of {column} on GPA')
    plt.xlabel(column)
    plt.ylabel('2023 GPA (%)')
    plt.show()
