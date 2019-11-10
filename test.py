from ThingspeakRead import ThingspeakRead
import pandas as pd
import matplotlib.pyplot as plt

ts = ThingspeakRead([819840, 819881],["064FW8NTX3QRY4QP","VL6335AOPWV00E4F"]); 
# ts = ThingspeakRead([819840],["064FW8NTX3QRY4QP"]); 

# dat   = ts.read(2000);
dat = ts.readRange("2019-10-21", "2019-11-10")


ts.toCSV();
y = dat[0]
y.plot(x="created_at", y=range(2,10))

plt.show()


