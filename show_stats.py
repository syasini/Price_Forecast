"""this module displays some statistics for the input commodity"""
import os
import argparse
from utils.ts_data import Data, save_stats_fig

# ----------------
# parse input args
# ----------------

parser = argparse.ArgumentParser()

parser.add_argument("commodity", # can be silver or gold
                    type=str,
                    help="commodity type")

parser.add_argument("-s", "--start_date",
                    default="2020-04-02",
                    type=str,
                    help="start date for stats to be shown")

parser.add_argument("-e", "--end_date",
                    default="2020-06-02",
                    type=str,
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

    print(f"showing stats for {args.commodity} "
      f"from {args.start_date} to {args.end_date}")

    # look up the commodity file path and construct the Data class
    data = Data(commodity_dict[args.commodity.lower()])

    # -----------
    # Stats Plots
    # -----------

    # plot the Price time series
    data.plot_ts(column="Price")
    save_stats_fig(f"{args.commodity}_Price", args.start_date, args.end_date)

    # plot the Price correlations
    data.plot_corr(column="Price")
    save_stats_fig(f"{args.commodity}_Price_corr", args.start_date, args.end_date)

    # plot the Price histograms
    data.plot_hist(column="Price")
    save_stats_fig(f"{args.commodity}_Price_hist", args.start_date, args.end_date)

    # plot the Return time series
    data.plot_ts(column="Return")
    save_stats_fig(f"{args.commodity}_Return", args.start_date, args.end_date)

    # plot the Return correlations
    data.plot_corr(column="Return")
    save_stats_fig(f"{args.commodity}_Return_corr", args.start_date, args.end_date)

    # plot the Return histograms
    data.plot_hist(column="Return")
    save_stats_fig(f"{args.commodity}_Return_hist", args.start_date, args.end_date)

    # ------------
    # Stats Report
    # ------------

    print(f"\n{'':=>50}\n")

    print(data.summary)

    print(f"\n{'':=>50}\n")

    print(data.adf_test("Return"))

    print(f"\n{'':=>50}\n")

    print("Check out the plots/ directory for the figures!")
