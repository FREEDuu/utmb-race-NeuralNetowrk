if __name__ == "__main__":
    
    import pandas as pd
    runner_df = pd.read_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/runnerDF.csv")
    cleaned_races_df = pd.read_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/cleaned_raceDF.csv")


    merged_df = pd.merge(
        runner_df,
        cleaned_races_df,
        on="race_id"
    )

    merged_df.dropna(subset=["race_distance", "race_elevation", "runner_utmb_index"], inplace=True)
    merged_df.to_csv("cleaned_races_df.csv", index=False)