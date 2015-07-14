from __future__ import print_function, division
import statsmodels.api as sm
import matplotlib.pyplot as plt

def analyze(mosquito_data):
    """Fit and plot mosquito data
    
    Run a linear fit between rainfall and mosquito
    plot the result"""
    regr_result = sm.OLS.from_formula('mosquitos ~ rainfall', 
                                      mosquito_data).fit()
    parameters = regr_result.params
    line_fit = parameters["Intercept"] + \
            parameters["rainfall"] * mosquito_data["rainfall"]
    plt.figure()
    plt.plot(mosquito_data["rainfall"], mosquito_data["mosquitos"],
             ".", label="data")
    plt.plot(mosquito_data["rainfall"], line_fit, color="r", label="fit")
    plt.legend()
    return parameters