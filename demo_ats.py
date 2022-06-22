import pickle
from src.ats import *
import pandas as pd
from src.print_ats import *
from src.input_data import InputData
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
    ElasticNetCV,
)
from sklearn.svm import SVR
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from src.helper import print_progress_bar
from src.globals import (
    PREPROCESSING_IN_FILE,
    INPUTDATA_OBJECT,
    ATS_OUT_FILE,
    RANDOM_SEED,
    TARGET_COLUMN,
    DATE_COLS,
)


if __name__ == "__main__":

    try:
        # raise Exception("tuning prep process")
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}.pkl")
    except:
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_standard_preprocessing(
            agg_col="rem_time",  # calculated y column
            filter_incompletes=True,
            dropna=False,
            date_cols=DATE_COLS,  # list of cols that must be transformed. If empty / not given, nothing will be transformed
        )

        # # columns that have have ordinal values are label encoded
        # input.use_cat_encoding_on("label", ["Category", "Activity"])

        # columns with too many categories are deleted
        input.use_cat_encoding_on(
            "none",
            [
                "Service Affected",
                "Asset Affected",
                "Asset SubType Affected",
                "Service Caused",
                "Assignment Group",
                "Priority",
                "Asset Type Affected",
                "Category",
                "Status",
                "Closure Code",
                "Asset Caused",
                "Asset Type Caused",
                "Asset SubType Caused",
            ],
        )

        input.save_df(
            n_rows=20
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(INPUTDATA_OBJECT)

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=TARGET_COLUMN, ratio=0.8, seed=RANDOM_SEED
    )

    X_test = input.add_prev_events(X_test)

    # X_test = X_test[~["activity"]]
    # X_train = X_train[~["activity"]]

    # X_test = input.add_prev_events(X_test)  # self explanatory

    ats = ATS(
        trace_id_col="Incident ID",
        act_col="Activity",
        y_col="RemainingTime",
        representation="multiset",
        horizon=1,
        model=HistGradientBoostingRegressor(),
        seed=RANDOM_SEED,
    )

    ats.fit(X_train, y_train)
    ats.finalize()
    # ats.print()

    ats.save(ATS_OUT_FILE)

    diff = 0.0

    print_progress_bar(
        0, len(y_test), prefix="Prediction:", suffix="Complete", length=50
    )

    for i, event in enumerate(X_test.to_dict(orient="records")):

        y_pred = ats.predict(event)

        diff += abs(y_pred - y_test.iloc[i])

        # print(f" --> diff: {round(diff / (60*60))}, y_pred: {round(y_pred / (60*60))}, y_real: {round(y_test.iloc[i] / (60*60))}")

        print_progress_bar(
            i + 1, len(y_test), prefix="Prediction:", suffix="Complete", length=50
        )

        # if i == 5:
        #     break

    diff = diff / len(y_test)

    print(
        f"MAE: {round(diff / (60*60))} hours  = {round(diff / (60*60*24))} days"
    )  # get difference in hours instead of seconds
