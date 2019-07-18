import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results_intmodp.csv')
fig, axs = plt.subplots(2,3, figsize=(20,15)) 
axs = axs.ravel()
for i,bits in enumerate(df.bits.unique()):
    sub_df = df.loc[df.bits==bits]
    sub_df.plot('N',['NaiveMults', 'PipMults'], ax=axs[i])
    axs[i].set_title('{}-bits prime'.format(bits))
    axs[i].set_xlabel('N')
    axs[i].set_ylabel('# of multiplications')
plt.savefig('performance_integers_modp.png', bbox_inches='tight')

df = pd.read_csv('results_ec.csv')
fig, axs = plt.subplots(2,3, figsize=(20,15)) 
axs = axs.ravel()
for i,curve in enumerate(df.curve.unique()):
    sub_df = df.loc[df.curve==curve]
    sub_df.plot('N',['NaiveTime', 'PipTime'], ax=axs[i])
    axs[i].set_title(curve)
    axs[i].set_xlabel('N')
    axs[i].set_ylabel('time [s]')
plt.savefig('performance_ec.png', bbox_inches='tight')
