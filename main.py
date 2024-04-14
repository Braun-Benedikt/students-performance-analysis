import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

survey_df = pd.read_csv('./data/stats_survey.csv')
avg_per_category = survey_df.groupby('Additional amount of studying (in hrs) per week')['Your 2023 academic year average/GPA in % (Ignore if you are 2024 1st year student)'].mean().reset_index()

# Create a strip plot
category_order = ['0', '1-3', '3-5', '5-8', '8+']
plt.figure(figsize=(8, 6))
sns.stripplot(x='Additional amount of studying (in hrs) per week', y='Your 2023 academic year average/GPA in % (Ignore if you are 2024 1st year student)', data=survey_df, order=category_order, jitter=True)
for i, row in avg_per_category.iterrows():
    plt.scatter(row['Additional amount of studying (in hrs) per week'], row['Your 2023 academic year average/GPA in % (Ignore if you are 2024 1st year student)'], color='red', label='Average' if i == 0 else None)
plt.title('Impact of additional studying on GPA ')
plt.xlabel('Additional studying (hrs)')
plt.ylabel('2023 GPA (%)')
plt.show()
