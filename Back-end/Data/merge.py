import pandas as pd
#merge and delete duplicates from the phish tank urls

# header=None specifies that there is no header, but there is - so we skiprows to not have that
df1 = pd.read_csv('verified_online(1).csv', skiprows = 1, header=None)
df2 = pd.read_csv('verified_online(4).csv', skiprows = 1, header=None)
df3 = pd.read_csv('verified_online(5).csv', skiprows = 1, header=None)
df4 = pd.read_csv('verified_online(6).csv', skiprows = 1, header=None)
df5 = pd.read_csv('verified_online.csv', skiprows = 1, header=None)
df6 = pd.read_csv('verified_online7.csv', skiprows = 1, header=None)

res = pd.concat([df1, df2, df3, df4, df5], ignore_index=True) # ignore_index=True doesn't matter because it's exported without index, but just in case

df = res[1] # get second column - just the urls
noDuplicates = df.drop_duplicates(0) # now that only URLs are compared, drop duplicate lines

noDuplicates.to_csv('merged.csv',index=False,header=False)# export again with no index and no header - just data