import pickle
from src.globals import *
from src.metrics import get_mae_mse
import numpy as np

# get same train-test-split as used in our actual experiment

with open(f"data/{INPUTDATA_OBJECT}.pkl", "rb") as file:
    input = pickle.load(file)

# use same split as for the advanced models
_, _, y_train, y_test = input.train_test_split_on_trace(
    y_col=TARGET_COLUMN, ratio=0.8, seed=RANDOM_SEED
)

y_test = np.array(y_test)
y_preds_mean = np.array([y_train.mean()] * len(y_test))
y_preds_median = np.array([y_train.median()] * len(y_test))
y_train_mode = y_train.mode().tolist()
y_preds_mode = np.array([y_train_mode[len(y_train_mode) // 2]] * len(y_test))

mae_mean, mse_mean = get_mae_mse(y_test, y_preds_mean)
mae_median, mse_median = get_mae_mse(y_test, y_preds_median)
mae_mode, mse_mode = get_mae_mse(y_test, y_preds_mode)

print("Naive Mean")
# get difference in hours instead of seconds
print(f"MAE: {round(mae_mean/ (60*60))} hours  = {round(mae_mean / (60*60*24))} days")
print(f"MSE: {round(mse_mean/ (60*60))} hours  = {round(mse_mean / (60*60*24))} days")
print()

print("Naive Median")
# get difference in hours instead of seconds
print(
    f"MAE: {round(mae_median/ (60*60))} hours  = {round(mae_median / (60*60*24))} days"
)
print(
    f"MSE: {round(mse_median/ (60*60))} hours  = {round(mse_median / (60*60*24))} days"
)
print()

print("Naive Mode")
# get difference in hours instead of seconds
print(f"MAE: {round(mae_mode/ (60*60))} hours  = {round(mae_mode / (60*60*24))} days")
print(f"MSE: {round(mse_mode/ (60*60))} hours  = {round(mse_mode / (60*60*24))} days")
print()