from ucimlrepo import fetch_ucirepo
import pandas as pd

def load_data(repo_id):
    data = fetch_ucirepo(id=repo_id)
    X = pd.DataFrame(data.data.features)
    y = pd.DataFrame(data.data.targets, columns=['y'])

    df = pd.concat([X, y], axis=1)

    return df