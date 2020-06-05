"""This module contains the main class for the predictor"""

import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from datetime import datetime
from datetime import timedelta
from sklearn.metrics import mean_squared_error


class Predictor:
    """General AR(1) class that predicts R_t from R_t-1"""

    def __init__(self,
                 data,
                 features, # features to be used as predictors
                 train_ratio=0.8,
                 ):

        self.data = data

        self.n_data = data.shape[0]  # number of data points
        self.n_train = int(train_ratio * self.n_data)

        self.date_index = self.data["Date"]  # just in case we need it

        self.X = self.data[features]
        self.y = self.data[["R_t"]]

        self.X_train = self.X[:self.n_train]
        self.y_train = self.y[:self.n_train]

        self.X_test = self.X[self.n_train:]
        self.y_test = self.y[self.n_train:]

        self.imputer = self._get_imputer()

        # impute nan values in features
        self.X_train.loc[:, features] = self.imputer.transform(self.X_train[features])
        self.X_test.loc[:, features] = self.imputer.transform(self.X_test[features])

    def _get_imputer(self):
        """return KNN imputer for nan values

        Returns
        -------
        sklearn.impute.KNNImputer
        """
        imputer = KNNImputer(n_neighbors=2, weights="uniform")
        imputer.fit(self.X_train)

        return imputer

    def build_model(self):
        """override this with specific model methods"""
        ...

    def get_RMSE(self):
        """calculate the RMSE for the test data"""
        return np.sqrt(mean_squared_error(self.y_test, self.model.predict(self.X_test)))

    def forecast_return_tomorrow(self, return_today):
        """forecast the return for tomorrow by applying model.predict on today's return

        Returns
        -------
        R_t+1 = model.predict(R_t)
        """
        return_tomorrow = self.model.predict([[return_today]])[0, 0]
        return return_tomorrow

    def get_price_tomorrow(self, price_today, return_tomorrow):
        """find tomorrow's price using today's price and tomorrow's return

        Returns
        -------
        P_t+1 = P_t * (1 + R_t+1)
        """
        price_tomorrow = price_today * (1 + return_tomorrow)
        return price_tomorrow

    def forecast_price_tomorow(self, price_today, return_today):
        """forecast tomorrow's price using today's price and today's return

        Returns
        --------
        P_t+1 = P_t * (1 + model.predict(R_t))
        """
        return_tomorrow = self.forecast_return_tomorrow(return_today)
        price_tomorrow = price_today * (1 + return_tomorrow)
        return price_tomorrow

    def forecast_price_on(self, date, n_days=4):
        """forecast price for n_days after the given day

        Returns
        -------
        pd.DataFrame ["Date", "Forecast Price", "Forecast Return"]
        """

        assert type(date) is str, "input date has to be a string in YYYY-mm-dd format"

        df_on_date = self.data[date == self.data["Date"].dt.strftime("%Y-%m-%d").values]

        assert len(df_on_date.index) > 0, "date not found"

        # convert input date to datetime format
        date = datetime.strptime(date, "%Y-%m-%d")

        # construct a date list to be returned
        dates = [date + timedelta(days=i) for i in range(n_days+1)]

        # grab the price and rate on day 0 (today)
        prices = [df_on_date["P_t"].iloc[0]]
        returns = [df_on_date["R_t"].iloc[0]]


        for i in range(n_days):

            return_tomorrow = self.forecast_return_tomorrow(returns[i])
            price_tomorrow = self.get_price_tomorrow(prices[i], return_tomorrow)

            returns.append(return_tomorrow)
            prices.append(price_tomorrow)

        forecast_df = pd.DataFrame({"Date": dates,
                                    "Forecast Price": prices,
                                    "Forecast Returns": returns})

        return forecast_df



class LinearPredictor(Predictor):
    """Linear Regression model"""

    def __init__(self,
                 data,
                 features=["R_t-1"],
                 train_ratio=0.8,
                 ):
        super().__init__(data, features, train_ratio)

    def build_model(self):
        """build a linear regression model

        Returns
        -------
        None
        sets self.model to sklearn.linear_model.LinearRegression
        """
        model = LinearRegression()

        model.fit(self.X_train, self.y_train)

        self.model = model


class KNNPredictor(Predictor):

    def __init__(self,
                 data,
                 features=["R_t-1"],
                 train_ratio=0.8,
                 ):
        super().__init__(data, features, train_ratio)


    def build_model(self, n_neighbors=3):
        """build a linear regression model

       Returns
       -------
       None
       sets self.model to sklearn.neighbors.KNeighborsRegression
       """
        model = KNeighborsRegressor(n_neighbors)

        model.fit(self.X_train, self.y_train)

        self.model = model



# Gradient boost test model
class GBPredictor(Predictor):

    def __init__(self,
                 data,
                 features=["R_t-1"],
                 train_ratio=0.8,
                 ):
        super().__init__(data, features, train_ratio)


    def build_model(self):
        model = GradientBoostingRegressor()

        model.fit(self.X_train, self.y_train)

        self.model = model