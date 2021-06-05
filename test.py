from ThingSpeakClient import ThingSpeakClient
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
import numpy as np

# fID_all=[2 1 2 % wh-25
#     2 3 4; % wh-flat
#     2 5 6 % gr-50
#     2 7 8 % gr-flat
#     1 7 8  %wh-50
#     1 1 2 %south-wh
#     1 3 3 %mono
#     1 4 5 %south-gr
#     1 6 6]; %horizon
# grab data

# ts = ThingspeakRead([819840, 819881],["064FW8NTX3QRY4QP","VL6335AOPWV00E4F"]); 
ts = ThingSpeakClient([819840],["064FW8NTX3QRY4QP"], tz='Asia/Dhaka'); 
# dat   = ts.read(8000);
dat = ts.readRange([2019,11,12,0,0,0 ], [2019,11,13,0,0,0] );
ts.toCSV();
y = dat[0]

# compute energy and compare 

y.set_index('created_at', inplace=True, drop=True)

z = pd.DataFrame()

res = y.iloc[: ,1].add(y.iloc[: ,2])
z = z.assign(bifacial_south_wh=res) 
res = y.iloc[:,4].add(y.iloc[: ,5])
z = z.assign(bifacial_south_gr=res) 
z = z.assign(monofacial=y.iloc[:,3]) 
z = z.assign(horizon=y.iloc[:,6])

z = z.mul(15)
print(z.head())

# print(z)
# z = z.drop(['entry_id'], axis=1);

# plot daily current for bifacial and monofacial
z.plot()
plt.show()

# generate daily energy data cond
f_res = []
x_names = ['bifacial_south_wh','bifacial_south_gr', 'monofacial', 'horizontal']
for idx, day in z.groupby(z.index.date):
    results = {}
    results['date'] = idx.strftime("%Y-%m-%d")
    for i in range(4):
        int_res = integrate.trapz(y = day.iloc[:,i], x = day.index ).astype('float64')/ (10**9 * 3600)
        results[x_names[i]] = int_res
        # .astype('timedelta64[s]')
        # make a dataframe whree there are five columns each days data and each days energy
    f_res.append(results); 

# plot a multibar plot
data= pd.DataFrame(f_res); 
data.set_index('date', inplace=True, drop=True)
data = data.div(24);
data.plot.bar();
plt.show()

