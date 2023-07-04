import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import IV2SLS
import matplotlib.pyplot as plt

def prepare_shares(correlation_data, shares_data, version):
    # shares_data is a dict, access version by shares_data[version]
    shares_version = shares_data[version]
    shares_version = shares_version.groupby('iso3').mean().reset_index()

    # Merge correlation data with shares data based on country pairs
    merged_data = pd.merge(correlation_data, shares_version, left_on='iso3_firstcountry', right_on='iso3', suffixes=('_first', '_second'))
    merged_data = pd.merge(merged_data, shares_version, left_on='iso3_secondcountry', right_on='iso3', suffixes=('_first', '_second'))

    merged_data = merged_data.drop(['iso3_first', 'iso3_second'], axis=1)

    # Calculate the product columns for import and export shares
    merged_data['prod_import'] = merged_data['Import USD_first']/100 * merged_data['Import USD_second']/100 + merged_data['Import EUR_first']/100 * merged_data['Import EUR_second']/100
    merged_data['prod_export'] = merged_data['Export USD_first']/100 * merged_data['Export USD_second']/100 + merged_data['Export EUR_first']/100 * merged_data['Export EUR_second']/100

    return merged_data

class Regressions:
    def __init__(self, data, dependent_var, independent_vars):
        self.data = data
        self.dependent_var = dependent_var
        self.independent_vars = independent_vars

    def run_regression(self, method, instrument_vars=None):
        # drop missings (by row)
        input_data = self.data.dropna()

        # Add constant to independent variables
        y = input_data[self.dependent_var]
        X = input_data[self.independent_vars]
        X = sm.add_constant(X)

        # define instrument(s)
        if instrument_vars != None:
            instrument = input_data[instrument_vars]
        
        if instrument_vars == None and method == 'IV':
            raise ValueError("No instrument indicated for IV regression.")

        if method == 'IV':
            # Perform instrumental variable regression using IV2SLS
            iv_model = IV2SLS(y, X, instrument=instrument)
            iv_results = iv_model.fit()
            plt.rc('figure', figsize=(8, 5))
            plt.text(0.01, 0.05, str(iv_results.summary()), {'fontsize': 10}, fontproperties = 'monospace')
            plt.axis('off')
            plt.tight_layout()
            return iv_results

        elif method == 'OLS':
            # Perform ordinary least squares regression
            ols_model = sm.OLS(y, X, missing='drop')
            ols_results = ols_model.fit()
            plt.rc('figure', figsize=(8, 5))
            plt.text(0.01, 0.05, str(ols_results.summary()), {'fontsize': 10}, fontproperties = 'monospace')
            plt.axis('off')
            plt.tight_layout()
            return ols_results

        else:
            raise ValueError("Invalid regression method. Choose 'OLS' or 'IV'.")

# Regressions(data, dependent_var=['cons_corr'], independent_vars=['prod_cons_shares', 'prod_includeworldcorr']).run_regression(method='OLS').summary()
