"""this module displays price prediction of the commodity price"""

import os
import argparse
from utils.ts_data import Data, save_forecast_fig
from utils.predictor import KNNPredictor

# ----------------
# parse input args
# ----------------

parser = argparse.ArgumentParser()

parser.add_argument("commodity", # can be silver or gold
                    type=str,
                    help="commodity type")

parser.add_argument("-s", "--start_date",
                    default="2020-06-02",
                    type=str,
                    help="start date for stats to be shown")

parser.add_argument("-n", "--n_days",
                    default=4,
                    type=int,
                    help="end date for stats to be shown")

args = parser.parse_args()


# ------------
# file paths
# ------------

silver_data = os.path.join("data", "Silver_Futures_Historical_Data.csv")
gold_data = os.path.join("data", "Gold_Futures_Historical_Data.csv")

commodity_dict = {"silver": silver_data,
                 "gold": gold_data}

# --------
#   main
# --------
if __name__ == "__main__":

    print(f"Predicting the Price for {args.commodity} "
      f"for {args.n_days} after {args.start_date}")

    # look up the commodity file path and construct the Data class
    data = Data(commodity_dict[args.commodity.lower()])

    # build the prediction model
    knn_predictor = KNNPredictor(data=data.df, features=["R_t-1"], train_ratio=0.8)
    knn_predictor.build_model(n_neighbors=3)

    forecast = knn_predictor.forecast_price_on(args.start_date, n_days=args.n_days)

    # ---------------
    # Forecast Report
    # ---------------

    print(f"\n{'':=>50}\n")

    print(forecast)

    print(f"\n{'':=>50}\n")

    # plot the Price time series
    data.plot_ts(forecasts=[forecast], marker='.')
    save_forecast_fig(f"{args.commodity}_Price", args.start_date, args.n_days)


