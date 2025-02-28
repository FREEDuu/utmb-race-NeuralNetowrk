if __name__ == "__main__":
    
    import pandas as pd
    finalDF = pd.read_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/final_merge.csv")

        # Add the elevation per km feature

    finalDF["elevation_per_km"] = (finalDF["race_elevation"].astype(int) / 
                                    finalDF["race_distance"].astype(int))
    finalDF.to_csv("/home/francesco/Desktop/PersonalProject/utmb-race-NeuralNetowrk/database/data/final_merged_incline.csv", index=False)