from sklearn import datasets
import pandas as pd
import numpy as np


# data files
SAMPLE_FILE = 'data/kddcup.data_10_percent_corrected'
COMPLETE_FILE = 'data/kddcup.data.corrected'


# transforms sklearn dataset into pandas dataframe
def sklearn_to_df(sklearn_dataset):
    df = pd.DataFrame(sklearn_dataset.data, columns=sklearn_dataset.feature_names)
    df['target'] = pd.Series(sklearn_dataset.target)
    return df


# loads kdd dataset from sklearn
def load_from_sklearn():
    try:
        dataset = datasets.fetch_kddcup99(random_state=0, subset='SA', shuffle=True,
                                 percent10=True, download_if_missing=True)
        dataset = sklearn_to_df(dataset)

    except IOError:
        print("kddcup99 dataset cannot be loaded.")
        dataset = np.nan

    return dataset


# loads kdd dataset from file
def load_from_file():
    columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label", "last_flag"]

    df = pd.read_csv(SAMPLE_FILE, sep=',', names=columns)
    df = df.iloc[:,:-1]
    return df


# loads dataset, either from file or sklearn library
def load_dataset(type):
    dataset = np.nan

    if type == 'sklearn':
        dataset = load_from_sklearn()
    elif type == 'file':
        dataset = load_from_file()
    
    return dataset


# transforms categorical features
def transform_cat_features(df):
    df['protocol_type'] = df['protocol_type'].astype('category')
    df['service'] = df['service'].astype('category')
    df['flag'] = df['flag'].astype('category')
    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    return df


# split dataset into features and a target class
def split_dataset(df):
    features = df.iloc[:, 0:41].values  
    target = df.iloc[:, 41].values
    return features, target