import pandas as pd
"""
Script used to merge and delete duplicates from the collected phish tank urls
"""

# header=None specifies that there is no header, but there is - so skiprows is used to not have the header in the dataframes
df1 = pd.read_csv('verified_online(1).csv', skiprows=1, header=None)
df2 = pd.read_csv('verified_online(4).csv', skiprows=1, header=None)
df3 = pd.read_csv('verified_online(5).csv', skiprows=1, header=None)
df4 = pd.read_csv('verified_online(6).csv', skiprows=1, header=None)
df5 = pd.read_csv('verified_online.csv', skiprows=1, header=None)
df6 = pd.read_csv('verified_online7.csv', skiprows=1, header=None)
df7 = pd.read_csv('verified_online8.csv', skiprows=1, header=None)

# ignore_index=True doesn't matter because it's exported without index, but just in case
res = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
phish_tank = res[1]  # get second column - the URLs
print('--------------------------------------------------------------------------------')
print('Phish tank whole: ' + str(phish_tank.count()))
# now that only URLs are compared, drop duplicate lines
phish_tank_no_duplicates = phish_tank.drop_duplicates(0)
print('Phish tank deduplicated: ' + str(phish_tank_no_duplicates.count()))

# --------------------------------------
# phishing_dataset
# the dataset that was downloaded from  https://www.unb.ca/cic/datasets/url-2016.html
df8 = pd.read_csv('phishing_dataset.csv', header=None)
print('Ready dataset before: ' + str(df8.count()))
# now that only URLs are compared, drop duplicate lines
phishing_dataset_no_duplicates = df8.drop_duplicates(0)
print('Ready dataset deduplicated: ' +
      str(phishing_dataset_no_duplicates.count()))


# --------------------------------------
# concat and save
final_dataframe = pd.concat(
    [phish_tank_no_duplicates, phishing_dataset_no_duplicates], ignore_index=True)
print('Both datasets together: ' + str(final_dataframe.count()))
cum = final_dataframe.drop_duplicates(0)
print('Both datasets without duplication: ' + str(cum.count()))
# export again with no index and no header - just data
final_dataframe.to_csv('merged.csv', index=False, header=False)
