# DRAFT stuff (BASICALLY PSEUDOCODE)

import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import IV2SLS

def prepare_data(correlation_data, shares_data, version):
    # Filter shares data based on version and calculate averages
    shares_version = shares_data[version]
    shares_version = shares_version.groupby('iso3').mean().reset_index()

    # Merge correlation data with shares data based on country pairs
    merged_data = pd.merge(correlation_data, shares_version, left_on='iso3_firstcountry', right_on='iso3', suffixes=('_first', '_second'))
    merged_data = merged_data.drop('iso3', axis=1)

    # Calculate the product columns for import and export shares
    merged_data['prod_import'] = merged_data['Import USD_first'] * merged_data['Import USD_second'] + merged_data['Import EUR_first'] * merged_data['Import EUR_second']
    merged_data['prod_export'] = merged_data['Export USD_first'] * merged_data['Export USD_second'] + merged_data['Export EUR_first'] * merged_data['Export EUR_second']

    return merged_data


def run_regression(dependent_var, independent_vars, data, method='OLS'):
    # Add constant to independent variables
    independent_vars = sm.add_constant(independent_vars)

    if method == 'IV':
        # Perform instrumental variable regression using IV2SLS
        iv_model = IV2SLS(dependent_var, independent_vars, instrument=data['instrument'])
        iv_results = iv_model.fit()
        return iv_results
    elif method == 'OLS':
        # Perform ordinary least squares regression
        ols_model = sm.OLS(dependent_var, independent_vars)
        ols_results = ols_model.fit()
        return ols_results
    else:
        raise ValueError("Invalid regression method. Choose 'OLS' or 'IV'.")
