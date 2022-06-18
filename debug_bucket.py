import pickle
from src.bucket import Bucket
import pandas as pd
from src.print_ats import *
from src.input_data import InputData
from sklearn.model_selection import train_test_split

PREPROCESSING_IN_FILE = "incidentProcess_custom.csv"
INPUTDATA_OBJECT = "preprocessed_inputData_object"
ATS_OUT_FILE = "ats"
RANDOM_SEED = 42
TARGET_COLUMN = "RemainingTime"


FILENAME = "incidentProcess_custom.csv"

DATE_COLS = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]

AGG_COLS = ["conv_time", "rem_time", "rem_act", "inc_cases", "prev_events"]


def train_test_split_on_trace(
    self,
    trace_identifier: str,
    X,
    y,
    test_size: int = None,
    train_size: int = None,
    random_state: int = None,
):
    unique_ids = self.df[trace_identifier].unique().tolist()

    pass


#     X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=RANDOM_SEED
# )

if __name__ == "__main__":

    try:
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}.pkl")
    except:
        input = InputData(FILENAME)
        input.apply_standard_preprocessing(
            agg_col="rem_time",  # calculated y column
            filter_incompletes=True,
            date_cols=DATE_COLS,  # list of cols that must be transformed. If empty / not given, nothing will be transformed
        )

        input.use_cat_encoding_on(
            "ohe", ["Priority"]
        )  # can be a list of features that need ohe
        input.use_cat_encoding_on(
            "label", ["Category"]
        )  # can be a list of features that need label / numerical encoding
        input.use_cat_encoding_on(
            "none", ["Service Affected"]
        )  # list of features that need to be deleted

        input.save_df(
            n_rows=20
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(INPUTDATA_OBJECT)

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=TARGET_COLUMN, ratio=0.05, seed=RANDOM_SEED
    )

    # X_test = input.add_prev_events(X_test)  # self explanatory

    bucket = Bucket(
        id=1,
        x_cols=X_train.columns.tolist(),
        y_col=y_train.name,
        data=pd.concat([X_train, y_train], axis=1),
        model_type="avg",
    )
    bucket.finalize()
