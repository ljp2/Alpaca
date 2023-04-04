from setupFit import *

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error

from xgboost import XGBRegressor

df = pd.read_csv(f'{getAllFileDirectory()}/all.csv')
X,y = calcXy(df, 'low+5c')

xgb = XGBRegressor(booster='gbtree', objective='reg:squarederror', max_depth=6,
                   learning_rate=0.025, n_estimators=100, random_state=2, n_jobs=-1)

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=101)

xgb.fit(X_train, y_train)

y_pred = xgb.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_pred, y_test))
print(rmse)

xgb.save_model('Fit/xgbL.json')
