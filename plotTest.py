import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)


matplotlib.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()
ax.plot([2, 3, 4, 5], [2, 3, 4, 5],'-')
ax.set_title('Using hyphen instead of Unicode minus')

plt.show()
