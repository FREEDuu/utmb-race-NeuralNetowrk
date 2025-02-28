import pandas as pd

def delete_rows_with_missing_values(df, column_name):

    df_cleaned = df.dropna(subset=[column_name])
    return df_cleaned

# Example Usage:
# Assuming 'runner_df' is your DataFrame, and 'finish_hours' is the column with potential missing values:
# runner_df = delete_rows_with_missing_values(runner_df, 'finish_hours')
# print(runner_df)

def clean_swapped_columns(df):
    # Copy to avoid modifying original
    df = df.copy()
    
    # Detect rows where elevation contains "KM" (case-insensitive)
    elevation_has_km = df["race_elevation"].astype(str).str.contains("km", case=False, na=False)
    print(elevation_has_km)
    # Swap distance and elevation for these rows
    df.loc[elevation_has_km, ["race_distance", "race_elevation"]] = \
        df.loc[elevation_has_km, ["race_elevation", "race_distance"]].values
        
    for col in ["race_distance", "race_elevation"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("[^0-9.]", "", regex=True)  # Remove non-numeric
            .replace("", None)                        # Handle empty strings
            .astype(float)
        )
    return df

import pandas as pd
import datetime


def time_str_to_total_seconds(time_str):
    """Converts a time string (HH:MM:SS) to total seconds as an integer."""
    try:
        time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        total_seconds = (time_obj.hour * 3600) + (time_obj.minute * 60) + time_obj.second
        return total_seconds
    except (ValueError, AttributeError):
        return None  # Or some other default value

def convert_finish_time_to_hours(df, column_name="runner_finish_time", new_column_name="finish_hours"):
    """Converts the 'runner_finish_time' column to total hours as integers."""
    df[new_column_name] = df[column_name].apply(time_str_to_total_seconds)
    return df


if __name__ == "__main__":

    df = pd.read_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/final.csv")
    df = delete_rows_with_missing_values(df, "runner_finish_time")
    clean_df = convert_finish_time_to_hours(df)
    clean_df = clean_df.dropna()
    clean_df.to_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/final_cleaned.csv", index=False)