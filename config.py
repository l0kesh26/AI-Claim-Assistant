import pandas as pd

USER_DB = {"admin": "123", "harsha": "password123"}
SENDER_A = "ramtgemini@gmail.com"
SENDER_B = "rameshapk24@gmail.com"

# LOAD CSV
def load_policies():
    df = pd.read_csv("test.csv")
    df.columns = df.columns.str.strip()
    return df

policy_df = load_policies()