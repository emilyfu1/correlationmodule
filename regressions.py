import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.iv import IV2SLS, IVLIML, IVGMM
import matplotlib.pyplot as plt
import preparecorrelations as pc
import regressions as reg
import importlib
from dotenv import dotenv_values, find_dotenv
import os
importlib.reload(pc)
importlib.reload(reg)
from IPython.display import HTML

# this looks for your configuration file and then reads it as a dictionary
config = dotenv_values(find_dotenv())

# set path using the dictionary key for which one you want
correlationpath = os.path.abspath(config["CORRELATIONDATA"]) + '\\'
cleandatapath = os.path.abspath(config["CLEANDATA"]) + '\\'
rawdatapath = os.path.abspath(config["RAWDATA"]) + '\\'
ocadatapath = os.path.abspath(config["FRANKELROSEDATA"]) + '\\'
gravitydatapath = os.path.abspath(config["GRAVITYDATA"]) + '\\'

# use to make a nice results table
def pretty_print(df):
    for_display = HTML(df.to_html().replace("\\n","<br>"))
    return for_display

def prepare_shares(correlation_data, shares_data, version):
    # shares_data is a dict, access version by shares_data[version]
    shares_version = shares_data[version]
    shares_version = shares_version[shares_version['iso3'].isin(list(correlation_data['iso3_firstcountry']) + list(correlation_data['iso3_secondcountry']))]
    shares_version = shares_version.groupby('iso3').mean().reset_index()

    # Merge correlation data with shares data based on country pairs
    merged_data = pd.merge(correlation_data, shares_version, left_on='iso3_firstcountry', right_on='iso3', suffixes=('_first', '_second'))
    merged_data = pd.merge(merged_data, shares_version, left_on='iso3_secondcountry', right_on='iso3', suffixes=('_first', '_second'))

    merged_data = merged_data.drop(['iso3_first', 'iso3_second'], axis=1)

    # Calculate the product columns for import and export shares
    merged_data['prod_import'] = merged_data['Import USD_first']/100 * merged_data['Import USD_second']/100 + merged_data['Import EUR_first']/100 * merged_data['Import EUR_second']/100
    merged_data['prod_export'] = merged_data['Export USD_first']/100 * merged_data['Export USD_second']/100 + merged_data['Export EUR_first']/100 * merged_data['Export EUR_second']/100

    # columns created by merge (not needed)
    to_remove = ['Import USD_first', 'Import EUR_first', 'Export USD_first', 'Export EUR_first', 'Import USD_second', 'Import EUR_second', 'Export USD_second', 'Export EUR_second']

    merged_data.drop(to_remove, axis=1, inplace=True)

    return merged_data

class Regressions:
    def __init__(self, data):
        self.data = data

    def run_regression(self, method, dependent_var, independent_vars=None, endog_vars=None, instrument_vars=None, iv_type='2SLS'):
        # drop missings (by row)
        input_data = self.data.copy()

        data_used = dependent_var
        if independent_vars != None:
            data_used = data_used + independent_vars
        if endog_vars != None:
            data_used = data_used + endog_vars
        if instrument_vars != None:
            data_used = data_used + instrument_vars
        
        input_data = input_data[data_used]
        input_data = input_data.dropna()

        # define dependent variable
        y = input_data[dependent_var]

        # add constant to independent variables
        if independent_vars != None:
            X = input_data[independent_vars]
            X = sm.add_constant(X)
        else:
            X = pd.DataFrame(1, index=np.arange(len(input_data)), columns=['const'])

        # define endog (to be instrumented)
        if endog_vars != None:
            endog=input_data[endog_vars]

        # define instrument(s)
        if instrument_vars != None:
            instrument = input_data[instrument_vars]
        
        if instrument_vars == None and method == 'IV':
            raise ValueError("No instrument indicated for IV regression.")

        if method == 'IV':
            # perform instrumental variable regression using IV2SLS/ML/GMM estimation (GMM with default parameters from linearmodels)
            if iv_type == '2SLS': 
                iv_model = IV2SLS(dependent=y, exog=X, endog=endog, instruments=instrument)
                iv_results = iv_model.fit()
                plt.text(0.5, 1.08, self.data.name, horizontalalignment='center',fontsize=15)
                plt.rc('figure', figsize=(8, 5))
                plt.text(0.01, 0.05, str(iv_results), {'fontsize': 10}, fontproperties = 'monospace')
                plt.axis('off')
                plt.tight_layout()
                plt.show()
            elif iv_type == 'ML':
                iv_model = IVLIML(dependent=y, exog=X, endog=endog, instruments=instrument)
                iv_results = iv_model.fit()
                plt.text(0.5, 1.08, self.data.name, horizontalalignment='center',fontsize=15)
                plt.rc('figure', figsize=(8, 5))
                plt.text(0.01, 0.05, str(iv_results), {'fontsize': 10}, fontproperties = 'monospace')
                plt.axis('off')
                plt.tight_layout()
                plt.show()
            elif iv_type == 'GMM':
                iv_model = IVGMM(dependent=y, exog=X, endog=endog, instruments=instrument)
                iv_results = iv_model.fit()
                plt.text(0.5, 1.08, self.data.name, horizontalalignment='center',fontsize=15)
                plt.rc('figure', figsize=(8, 5))
                plt.text(0.01, 0.05, str(iv_results), {'fontsize': 10}, fontproperties = 'monospace')
                plt.axis('off')
                plt.tight_layout()
                plt.show()
            else:
                raise ValueError("Indicate 2SLS, ML, OR GMM estimation method")
            return iv_results

        elif method == 'OLS':
            # perform ordinary least squares regression
            ols_model = sm.OLS(y, X, missing='drop')
            ols_results = ols_model.fit()
            plt.text(0.5, 1.08, self.data.name, horizontalalignment='center',fontsize=15)
            plt.rc('figure', figsize=(8, 5))
            plt.text(0.01, 0.05, str(ols_results.summary()), {'fontsize': 10}, fontproperties = 'monospace')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            return ols_results

        else:
            raise ValueError("Indicate 'OLS' or 'IV' regression")

