"""This module contains the main class for time series data"""

import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tsa.stattools import kpss, adfuller

from utils.cleaning import clean_string, clean_vol, clean_change


def save_stats_fig(title, start_date, end_date):
    """save the figure in the plots directory"""

    plot_fname = os.path.join(".", "plots", f"{title}_{start_date}_to_{end_date}.png")

    # if the plots/ dir does not exist, make one!
    plot_dir = os.path.dirname(plot_fname)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plt.savefig(plot_fname, dpi=100, bbox_inches="tight")


def save_forecast_fig(title, start_date, n_days):
    """save the forecast figure in the plots directory"""

    plot_fname = os.path.join(".", "plots", f"Forecast_{title}_{n_days}_after_{start_date}.png")

    # if the plots/ dir does not exist, make one!
    plot_dir = os.path.dirname(plot_fname)
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plt.savefig(plot_fname, dpi=100, bbox_inches="tight")



class Data:
    """The data class for reading the prices and calculating stats"""

    def __init__(self,
                 file_name,
                 start_date=None,
                 end_date=None):

        self.df = self.read_and_clean_data(file_name)

        # make sure start and end dates have the right format
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.df = self.df[self.df["Date"] > start_date]

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            self.df = self.df[self.df["Date"] < end_date]

        # calculate basic statistical properties of data (mean, std, etc)
        self.summary = self.df.describe()

        # calculate new features
        self._calc_Pts()  # P_t and P_t-1
        self._calc_return()  # calculate R_t and R_t-1
        self._calc_log_V()  # calculate log Vol

    def read_and_clean_data(self, file_name):
        """read the csv file into a pandas dataframe"""

        assert file_name.endswith(".csv"), "Please provide a csv file"

        converters_dict = {
            "Price"   : clean_string,
            "Open"    : clean_string,
            "High"    : clean_string,
            "Low"     : clean_string,
            "Vol."    : clean_vol,
            "Change %": clean_change,
            }

        # read the csv file
        df = pd.read_csv(file_name,
                         parse_dates=["Date"],
                         converters=converters_dict)

        df.sort_values(by="Date", inplace=True)

        return df.reset_index(drop=True)

    def get_t_minus(self, n, column="Price"):
        """return the price for day t minus n (n days ago)"""
        return self.df[column].shift(n)

    def _calc_Pts(self):
        """make new columns for price at t and t-1"""
        self.df["P_t"] = self.get_t_minus(0, "Price")
        self.df["P_t-1"] = self.get_t_minus(1, "Price")

        # The first date will be NaN; fill it in with the value from the next day
        self.df["P_t-1"].fillna(method="bfill", inplace=True)

    def _calc_log_V(self):
        """calculate log of Vol."""
        self.df["log_Vol"] = np.log(self.df["Vol."])

    def _calc_return(self):
        """calculate the return at t and t-1 using P_t and P_t-1"""
        self.df["Return"] = (self.df["P_t"] / self.df["P_t-1"]) - 1
        self.df["R_t"] = self.df["Return"]
        self.df["R_t-1"] = self.get_t_minus(1, "Return")

        # The first date will be NaN; fill it in with the value from the next day
        self.df["R_t-1"].fillna(method="bfill", inplace=True)

    def plot_ts(self, column="Price", rolling=5, forecasts=None, jupyter=True, **forecast_kwargs):
        """plot the time series for the given column """
        fig, ax = plt.subplots(1, 1, figsize=(10, 3), dpi=100)
        plt.subplots_adjust(hspace=0.8)
        self.df.plot.line("Date", column, ax=ax, grid=True)

        if forecasts is not None:
            for forecast in forecasts:
                forecast.plot.line("Date", "Forecast " + column, ax=ax, **forecast_kwargs)

        if not jupyter:
            return fig

    def plot_corr(self, column="Price", lags=10, jupyter=True):
        """plot the autocorrelation and partial autocorrelation"""
        fig, ax = plt.subplots(2, 1, figsize=(10, 6), dpi=100)
        plt.subplots_adjust(hspace=0.5)
        sm.graphics.tsa.plot_acf(self.df[column], lags=lags, ax=ax[0])
        sm.graphics.tsa.plot_pacf(self.df[column], lags=lags, ax=ax[1])

        if not jupyter:
            return fig

    def plot_hist(self, column="Price", jupyter=True):
        """plot the time series histogram"""
        fig = plt.figure(figsize=(5, 3), dpi=100)

        sns.distplot(self.df[column], bins=10, )

        if not jupyter:
            return fig

    def kpss_test(self, column="Price"):
        """KPSS test for staionarity

        code source: https://www.statsmodels.org/dev/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
        """
        print(f'Results of KPSS Test on {column}:')
        kpss_test = kpss(self.df[column])
        kpss_output = pd.Series(kpss_test[0:3], index=['Test Statistic', 'p-value', 'Lags Used'])

        return kpss_output

    def adf_test(self, column="Price"):
        """ADF test for staionarity

        code source: https://www.statsmodels.org/dev/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
        """
        print(f'Results of ADF Test on {column}:')
        adf_test = adfuller(self.df[column])
        adf_output = pd.Series(adf_test[0:3], index=['Test Statistic', 'p-value', 'Lags Used'])

        return adf_output

