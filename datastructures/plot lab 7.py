import matplotlib.pyplot as plt
import numpy as np

# Data from your image
ib_uA = np.array([9.94, 19.9, 30.03])
ic_mA = np.array([2.19, 4.15, 6.46])

# Calculate Linear Regression (Best Fit Line)
# m is the slope, b is the y-intercept
m, b = np.polyfit(ib_uA, ic_mA, 1)

# Create the plot
plt.figure(figsize=(8, 6))
#plt.plot(ib_uA, ic_mA, 'bo', label='Measured Data') # Blue dots
plt.plot(ib_uA, m*ib_uA + b, 'r--', label=f'Linear Fit') # Red dashed line

# Formatting
plt.title('Ic vs Ib Linearity (BJT Current Gain)')
plt.xlabel('Base Current $I_B$ ($\mu$A)')
plt.ylabel('Collector Current $I_C$ (mA)')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()