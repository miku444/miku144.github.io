import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt

# 连续信号
t = np.linspace(0, 2*np.pi, 1000)
y = np.cos(t)

plt.figure()
plt.plot(t, y)
plt.title("cos(t)")
plt.grid()

# 离散信号
n = np.arange(0, 20)
x = np.cos(n)

plt.figure()
plt.stem(n, x)
plt.title("cos(n)")
plt.grid()

plt.show()
input("按回车退出")