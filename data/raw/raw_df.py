from load_data import load_data

data = load_data(repo_id=222)

data.to_pickle("raw_df.pkl")