# SpaceX Data Wrangling Notebook

This folder contains the Jupyter Notebook `labs-jupyter-spacex-Data wrangling-v2.ipynb`, which is part of the Applied Data Science Capstone project. The notebook focuses on data wrangling and exploratory data analysis (EDA) of SpaceX Falcon 9 launch data.

## Notebook Overview

The primary goal of this notebook is to prepare the data for training supervised machine learning models. This involves cleaning the data, handling missing values, and creating a target variable (label) for classification.

### Key Steps and Code Explanation

1.  **Import Libraries**:
    *   `pandas` and `numpy` are imported for data manipulation and numerical operations.

2.  **Load Data**:
    *   The dataset is loaded from a provided URL into a Pandas DataFrame (`df`).
    *   `df.head(10)` displays the first 10 rows to inspect the data structure.

3.  **Data Analysis & Missing Values**:
    *   `df.isnull().sum()/len(df)*100`: Calculates the percentage of missing values for each column. This helps identify which columns need attention (e.g., imputation or removal).
    *   `df.dtypes`: Displays the data types of each column to distinguish between numerical and categorical variables.

4.  **Task 1: Launch Site Analysis**:
    *   `df['LaunchSite'].value_counts()`: Counts the number of launches from each launch site (e.g., CCAFS SLC-40, KSC LC 39A, VAFB SLC 4E). This provides insight into the usage frequency of different launch facilities.

5.  **Task 2: Orbit Analysis**:
    *   `df['Orbit'].value_counts()`: Counts the number of launches for each target orbit (e.g., LEO, GTO, ISS). This helps understand the distribution of mission types.

6.  **Task 3: Mission Outcome Analysis**:
    *   `landing_outcomes = df['Outcome'].value_counts()`: Counts the frequency of different landing outcomes (e.g., True ASDS, False ASDS, True RTLS).
    *   The loop prints each outcome with its index to help identify which outcomes represent success or failure.

7.  **Task 4: Create Class Label (Target Variable)**:
    *   **Identify Bad Outcomes**: A set `bad_outcomes` is created containing outcomes that represent unsuccessful landings (e.g., False ASDS, False Ocean, None ASDS, None None).
    *   **Create `landing_class`**: A list comprehension is used to create a binary list:
        *   `0`: If the outcome is in `bad_outcomes` (Failure).
        *   `1`: If the outcome is NOT in `bad_outcomes` (Success).
    *   **Assign to DataFrame**: `df['Class'] = landing_class` adds this binary label to the DataFrame. This `Class` column will be the target variable for machine learning models.
    *   `df["Class"].mean()`: Calculates the success rate of the landings.

8.  **Export Data**:
    *   `df.to_csv("dataset_part_2.csv", index=False)`: Saves the cleaned and labeled DataFrame to a new CSV file (`dataset_part_2.csv`) for use in subsequent stages of the project.

## Outputs

*   **dataset_part_2.csv**: The processed dataset with the new `Class` column indicating landing success (1) or failure (0).
