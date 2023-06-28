import pandas as pd
# df = pd.read_csv('https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/possum.csv?raw=true',on_bad_lines='skip')



# df.to_pickle('your_file.pkl')

df_from_pickle = pd.read_pickle('https://github.com/hotshotdragon/clearml_pipeline_trial/blob/main/data/data.pkl')

print(df_from_pickle.head())