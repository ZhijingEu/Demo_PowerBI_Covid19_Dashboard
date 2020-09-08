# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(SIR Curve - Start Day (From1Jan20) Value, No Of Initial Susceptibles Value, No Of Initial Infected Value, Beta - % Suspectibles Infected Daily Value, Gamma - % Infected Recovered Daily Value)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

#Code for SIR plotting was adapted from https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/ 

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

ActualDailyCases=dataset['cases'].to_numpy()
Days=dataset['RefDay'].to_numpy()

#Import the WhatIf Parameters from PowerBI into the Python Visual that represent key parameters of SIR Model

#StartDayRelativeTo 01 Jan 2020
StartDay=dataset.iloc[0][0]
#Total Population
N=dataset.iloc[0][1]
#Initial Infected
I0=dataset.iloc[0][2]
#Initial Recovered
R0=0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
beta=dataset.iloc[0][3]/100
gamma=dataset.iloc[0][4]/100


# A grid of time points (in days)
t = np.linspace(0, 360, 360)
shiftedt = [t+StartDay for element in t]

# The SIR model with differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t+StartDay, args=(N, beta, gamma))
S, I, R = ret.T

# Add leading values in order to shift the SIR curves along the x axis
leadingdays = [0]*int(StartDay)
Sleadingdays =[S0]*int(StartDay)
Sprime=np.concatenate((Sleadingdays, S))
Iprime=np.concatenate((leadingdays, I))
Rprime=np.concatenate((leadingdays, R))

# Plot the I(t) and Actual Daily Cases , uncomment the # for Sprime and Rprime to show all three SIR curves

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
#ax.plot(t, Sprime[:360], 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, Iprime[:360], 'r', alpha=0.5, lw=2, label='# Infected (Estimated By SIR Model)')
#ax.plot(t, Rprime[:360], 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.plot(Days,ActualDailyCases,'y', alpha=0.5, lw=2, label = 'Actual Daily Cases (Source: ECDC)' )
ax.set_xlabel('Time / Days (Day 0 = 1 Jan 2020)')
ax.set_ylabel('No Of People')
#ax.set_ylim(0,N)
ax.set_ylim(0,np.amax(Iprime)*1.1)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.2)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.show()
