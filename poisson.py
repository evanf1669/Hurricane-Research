import pandas as pd
from patsy import dmatrices
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

#Creates a data set
df = pd.read_csv('Everything_Bagel.csv', header=0, parse_dates=[0], index_col=[0])



choice = input("1) Annual Counts \n2) AnnualCountsHU :")
if (choice == '1'):
    #Creates a small data set with just one variable
    df['A'] = df[['NATL']].copy()
    df['B'] = df[['160E-80W HCI']].copy()
    df['C'] =df[['180W-100W HCI']].copy()
    df['D'] = df[['CO2']].copy()
    df['E'] = df[['Lowess (5)']].copy()
    df['F'] = df[['NINO1+2']].copy()
    df['G'] = df[['Nino1+2SST']].copy()
    df['H'] = df[['NINO3.4']].copy()
    df['I'] = df['NINO3'].copy()
    df['J'] = df[['Nino3SST']].copy()
    df['K'] = df[['Nino34SST']].copy()
    df['L'] = df[['No_Smoothing']].copy()
    df['M'] = df[['reqsoi']].copy()
    df['N'] = df['SATL'].copy()
    df['O'] =df[['sea level press (1000mb subtr)']].copy()
    df['P'] =df['soi standardized data'].copy()
    df['Q'] = df[['tahiti anomaly']].copy()
    df['R'] = df[['z500t original data']].copy()
    df['STORM_COUNT'] = df[['AnnualCounts']].copy()
if (choice == '2'):
    df['A'] = df[['CO2']].copy()
    df['B'] = df[['Darwin Original Data']].copy()
    df['C'] = df[['180W-100W HCI']].copy()
    df['D'] = df[['reqsoi']].copy()
    df['E'] = df[['soi standardized data']].copy()
    df['F'] = df[['NATL']].copy()
    df['G'] = df[['NINO1+2']].copy()
    df['H'] = df[['NINO3']].copy()
    df['I'] = df[['NINO4']].copy()
    df['J'] = df[['NINO3.4']].copy()
    df["K"] = df[['sea level press (1000mb subtr)']].copy()
    df['L'] = df[['tahiti anomaly']].copy()
    df['M'] = df[['Nino1+2SST']].copy()
    df['N'] = df[['Nino3SST']].copy()
    df['O'] = df[['Nino34SST']].copy()
    df['P'] = df[['Nino4SST']].copy()
    df['Q'] = df[['No_Smoothing']].copy()
    df['R'] = df[['Lowess (5)']].copy()
    df['STORM_COUNT'] = df[['AnnualCountsHU']].copy()

#The reason for training a regression model is to minimize the difference between predicted and actual values as much as possible
#msk is a boolean array msk[i] is true if msk[i] < 0.8. 
#Values of msk that are true are assigned to df_train whereas those that are false are assigned to df_test
mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]
print('Training data set length='+str(len(df_train)))
print('Testing data set length='+str(len(df_test)))

#First value is dependent variable, the rest are independent
expr = """STORM_COUNT ~ A + B + C + D + E + F + G + H + I + J + K + L + M + N + O + P + Q + R"""

#Creates two matrices, one for train and one for test
y_train, X_train = dmatrices(expr, df_train, return_type='dataframe')
y_test, X_test = dmatrices(expr, df_test, return_type='dataframe')

#Training summary
poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()
print(poisson_training_results.summary())

#Getting a prediction for the test data set
poisson_predictions = poisson_training_results.get_prediction(X_test)
predictions_summary_frame = poisson_predictions.summary_frame()
print(predictions_summary_frame)

#Graphs predicted vs actual
predicted_counts=predictions_summary_frame['mean']
actual_counts = y_test['STORM_COUNT']
fig = plt.figure()
fig.suptitle('Predicted versus actual')
predicted, = plt.plot(X_test.index, predicted_counts, 'go-', label='Predicted counts')
actual, = plt.plot(X_test.index, actual_counts, 'ro-', label='Actual counts')
plt.legend(handles=[predicted, actual])
plt.show()

#Show scatter plot of Actual versus Predicted counts
plt.clf()
fig = plt.figure()
fig.suptitle('Scatter plot of Actual versus Predicted counts')
plt.scatter(x=predicted_counts, y=actual_counts, marker='.')
plt.xlabel('Predicted counts')
plt.ylabel('Actual counts')
plt.show()