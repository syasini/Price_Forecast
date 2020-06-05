# Gold & Silver Price Forecast

## Installation

In order to use the library, clone it locally and install the setup
.py file.
 
 ```bash
git clone github.com/syasini/Gold_Silver_Forecast
cd Gold_silver_Forecast 
```
 
 If you are a conda user create a new enironment using the
 following:


```bash
conda env create -n gold_silver python=3.7
conda activate gold_silver
pip install -e .
``` 

## Notebook

Check out the notebook `price_predictions.ipynb` for a tour of various
 features of the library. 

## Modules

In order to see the Price and Return statistics between date ranges
 `start_date` and `end_date` run 
 
`python show_stats.py commodity -s start_date -e end_date`

for example,

`python show_stats.py Silver -s 2020-04-02 -e 2020-06-02`



In order to make price predictions on a specific date use 

`python predict_price.py commodity -s start_date -n n_days`

for example 

`python show_stats.py Silver -s 2020-06-02 -n 4`

predicts the price of silver for 4 days after June 2nd, 2020. 



 