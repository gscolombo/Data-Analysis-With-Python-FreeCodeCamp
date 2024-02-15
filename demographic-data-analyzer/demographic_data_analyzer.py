import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('./adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percent = lambda count, total: round((count / total) * 100, 1)
    
    bachelors = df.groupby('education')['education'].count()['Bachelors']
    total = len(df.index)
    percentage_bachelors = percent(bachelors, total)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`.
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[~(df['education'].isin(['Bachelors', 'Masters', 'Doctorate']))]

    # percentage with salary >50K
    higher_education_rich = percent(higher_education[higher_education['salary'] == '>50K'].shape[0], higher_education.shape[0])
    lower_education_rich = percent(lower_education[lower_education['salary'] == '>50K'].shape[0], lower_education.shape[0])

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[(df['hours-per-week'] == min_work_hours)]
    num_min_workers_with_high_salary = df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == ">50K")]

    rich_percentage = percent(num_min_workers_with_high_salary.shape[0], num_min_workers.shape[0])

    # What country has the highest percentage of people that earn >50K?
    country_and_salaries_ratio = {}
    for country in df['native-country'].unique():
        crit = df['native-country'].map(lambda c: (c == country))
        rich = df[(crit) & (df['salary'] == '>50K')].shape[0]
        total = df[crit].shape[0]
        country_and_salaries_ratio[country] = percent(rich, total) if rich else None

    country_and_salaries_ratio = pd.Series(country_and_salaries_ratio)

    highest_earning_country = country_and_salaries_ratio.idxmax()
    highest_earning_country_percentage = country_and_salaries_ratio.max()

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')].groupby('occupation')['occupation'].count().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
