import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

T = 25
v = 5000
V = 331.6 + T * 0.6
l_guess = 0.19
theta_guess = 27

def equations(vars):
    l, theta = vars
    m1 = 1
    m2 = 3
    eq1 = l * np.sin(np.radians(theta)) - m1 * V / 2000 / 2
    eq2 = l * np.sin(np.radians(60 - theta)) - m2 * V / v / 2  
    return [eq1, eq2]

l, theta = fsolve(equations, (l_guess, theta_guess))

x = np.linspace(-2, 2, 1000)
y = np.linspace(-2, 2, 1000)
x, y = np.meshgrid(x, y)

theta_rad = np.radians(theta)

# modify the sources' position to be on the line inclined by theta
sources = [
    (l * np.cos(theta_rad) * i, l * np.sin(theta_rad) * i) for i in [-0.5, 0.5]
]

intensity = np.zeros_like(x)

for sx, sy in sources:
    r = np.sqrt((x - sx)**2 + (y - sy)**2)
    phi = 2 * np.pi * r * v / V
    intensity += np.sin(phi)

intensity = np.abs(intensity)

plt.figure(figsize=(10,8))
plt.imshow(intensity, extent=(-2, 2, -2, 2), origin='lower')
plt.colorbar(label='Intensity')
plt.title('Sound Intensity of Two Sources')
plt.xlabel('x')
plt.ylabel('y')

for i, (sx, sy) in enumerate(sources, start=1):
    plt.scatter(sx, sy, color='red')
    plt.text(sx, sy, f'Source {i}', color='red', fontsize=12, verticalalignment='bottom')

plt.grid(True)
plt.show()
