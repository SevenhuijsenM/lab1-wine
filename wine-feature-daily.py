
import os

#I want the minimum and maximum values for each feature
def generate_wine(quality, fixed_acidity_avg, fixed_acidity_std, volatile_acidity_avg, volatile_acidity_std, 
                    citric_acid_avg, citric_acid_std, residual_sugar_avg, residual_sugar_std, chlorides_avg, chlorides_std,
                    free_sulfur_dioxide_avg, free_sulfur_dioxide_std, total_sulfur_dioxide_avg, total_sulfur_dioxide_std,
                    density_avg, density_std, pH_avg, pH_std, sulphates_avg, sulphates_std, alcohol_avg, alcohol_std,
                    type):
    """
    Returns a single wine type as a single row in a DataFrame
    """
    import pandas as pd
    import random
    
    df = pd.DataFrame({"fixed_acidity": [random.normalvariate(fixed_acidity_avg, fixed_acidity_std)], "volatile_acidity": [random.normalvariate(volatile_acidity_avg, volatile_acidity_std)], "citric_acid": [random.normalvariate(citric_acid_avg, citric_acid_std)], "residual_sugar": [random.normalvariate(residual_sugar_avg, residual_sugar_std)], "chlorides": [random.normalvariate(chlorides_avg, chlorides_std)], "free_sulfur_dioxide": [random.normalvariate(free_sulfur_dioxide_avg, free_sulfur_dioxide_std)], "total_sulfur_dioxide": [random.normalvariate(total_sulfur_dioxide_avg, total_sulfur_dioxide_std)], "density": [random.normalvariate(density_avg, density_std)], "ph": [random.normalvariate(pH_avg, pH_std)], "sulphates": [random.normalvariate(sulphates_avg, sulphates_std)], "alcohol": [random.normalvariate(alcohol_avg, alcohol_std)], "type": [type]})
    
    df['quality'] = quality

    # Change the type to an int
    df['type'] = int(type)

    return df

def get_random_wine():
    """
    Returns a DataFrame containing one random wine
    """
    import pandas as pd
    import random

    # Generate a random number in a switch case that generates a random wine
    df_wine = None
    random_nr = random.randint(1, 13)

    if random_nr == 1:
        df_wine = generate_wine(3, 8.36, 1.77, 0.88, 0.33, 0.17, 0.25, 2.64, 1.4, 0.12, 0.07, 11.0, 9.76, 24.9, 16.83, 1.0, 0.0, 3.4, 0.14, 0.57, 0.12, 9.96, 0.82, 1)
    elif random_nr == 2:
        df_wine = generate_wine(4, 7.78, 1.63, 0.69, 0.22, 0.17, 0.2, 2.69, 1.79, 0.09, 0.08, 12.26, 9.03, 36.25, 27.58, 1.0, 0.0, 3.38, 0.18, 0.6, 0.24, 10.27, 0.93, 1)
    elif random_nr == 3:
        df_wine = generate_wine(5, 8.17, 1.56, 0.58, 0.16, 0.24, 0.18, 2.53, 1.36, 0.09, 0.05, 16.98, 10.96, 56.51, 36.99, 1.0, 0.0, 3.3, 0.15, 0.62, 0.17, 9.9, 0.74, 1)
    elif random_nr == 4:
        df_wine = generate_wine(6, 8.35, 1.8, 0.5, 0.16, 0.27, 0.2, 2.48, 1.44, 0.08, 0.04, 15.71, 9.94, 40.87, 25.04, 1.0, 0.0, 3.32, 0.15, 0.68, 0.16, 10.63, 1.05, 1)
    elif random_nr == 5:
        df_wine = generate_wine(7, 8.87, 1.99, 0.4, 0.15, 0.38, 0.19, 2.72, 1.37, 0.08, 0.03, 14.05, 10.18, 35.02, 33.19, 1.0, 0.0, 3.29, 0.15, 0.74, 0.14, 11.47, 0.96, 1)
    elif random_nr == 6:
        df_wine = generate_wine(8, 8.57, 2.12, 0.42, 0.14, 0.39, 0.2, 2.58, 1.3, 0.07, 0.01, 13.28, 11.16, 33.44, 25.43, 1.0, 0.0, 3.27, 0.2, 0.77, 0.12, 12.09, 1.22, 1)
    elif random_nr == 7:
        df_wine = generate_wine(3, 7.6, 1.72, 0.33, 0.14, 0.34, 0.08, 6.39, 5.32, 0.05, 0.05, 53.32, 69.42, 170.6, 107.76, 0.99, 0.0, 3.19, 0.21, 0.47, 0.12, 10.34, 1.22, 0)
    elif random_nr == 8:
        df_wine = generate_wine(4, 7.13, 1.08, 0.38, 0.17, 0.3, 0.16, 4.63, 4.16, 0.05, 0.03, 23.36, 20.39, 125.28, 52.75, 0.99, 0.0, 3.18, 0.16, 0.48, 0.12, 10.15, 1.0, 0)
    elif random_nr == 9:
        df_wine = generate_wine(5, 6.93, 0.84, 0.3, 0.1, 0.34, 0.14, 7.33, 5.33, 0.05, 0.03, 36.43, 18.15, 150.9, 44.09, 1.0, 0.0, 3.17, 0.14, 0.48, 0.1, 9.81, 0.85, 0)
    elif random_nr == 10:
        df_wine = generate_wine(6, 6.84, 0.84, 0.26, 0.09, 0.34, 0.12, 6.44, 5.17, 0.05, 0.02, 35.65, 15.74, 137.05, 41.29, 0.99, 0.0, 3.19, 0.15, 0.49, 0.11, 10.58, 1.15, 0)
    elif random_nr == 11:
        df_wine = generate_wine(7, 6.73, 0.76, 0.26, 0.09, 0.33, 0.08, 5.19, 4.3, 0.04, 0.01, 34.13, 13.24, 125.11, 32.74, 0.99, 0.0, 3.21, 0.16, 0.5, 0.13, 11.37, 1.25, 0)
    elif random_nr == 12:
        df_wine = generate_wine(8, 6.66, 0.82, 0.28, 0.11, 0.33, 0.09, 5.67, 4.26, 0.04, 0.01, 36.72, 16.2, 126.17, 33.01, 0.99, 0.0, 3.22, 0.15, 0.49, 0.15, 11.64, 1.28, 0)
    elif random_nr == 13:
        df_wine = generate_wine(9, 7.42, 0.98, 0.3, 0.06, 0.39, 0.08, 4.12, 3.76, 0.03, 0.01, 33.4, 13.43, 116.0, 19.82, 0.99, 0.0, 3.31, 0.08, 0.47, 0.09, 12.18, 1.01, 0)
    return df_wine

if __name__ == "__main__":
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()

    wine_df = get_random_wine()

    # Make sure the type is an int
    wine_df['type'] = wine_df['type'].astype(int)

    wine_fg = fs.get_feature_group(name="wine",version=1)
    wine_fg.insert(wine_df)
