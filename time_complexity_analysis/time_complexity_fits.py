import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
import scipy.stats as stats
import os


x = np.linspace(1, 2500000, 10000)

def quadratic(x, a, b, c):
    return a * x ** 2 + b * x + c

def linear(x, a):
    return a * x

def logarithmic(x, a, b):
    return a * x * np.log(x) + b

def power(x, a, b):
    return a * x ** b

all_times = []
files = [f for f in os.listdir() if f.startswith('time_complexity_data_')]
for file in files:
    print(f"\nProcessing: {file}")
    n, t = np.loadtxt(file, delimiter = ',', skiprows = 1, unpack=True)  # Load data from file
    all_times.append(t)

stacked_times = np.vstack(all_times)
mean_times = np.mean(stacked_times, axis=0)

indices = []
for i in range(len(n)):
    if n[i] > 10000: #select value for which compression starts to occur
        indices.append(int(i))

fitting_values = np.array([mean_times[i] for i in indices])

errors = np.std(stacked_times, axis=0)
fitting_values_errors = np.array([errors[i] for i in indices])

n_fitting_values = np.array([n[i] for i in indices])
print(fitting_values)
print(f"n: {n_fitting_values}")

linparams, lincov = scp.curve_fit(linear, n_fitting_values, fitting_values, p0=[0.0004])


lin_params_errors = np.sqrt(np.diag(lincov))

deg_of_freedom = len(n) - len(linparams)

lin_t_values = linparams / lin_params_errors
lin_p_values = [2 * (1 - stats.t.cdf(abs(t), deg_of_freedom)) for t in lin_t_values]

print("\nLinear Fit:")
print(f"Parameters: {linparams}")
print(f"Errors: {lin_params_errors}")
print(f"t-values: {lin_t_values}")
print(f"p-values: {lin_p_values}")

plt.figure(figsize=(8, 6))
plt.loglog(x, linear(x, *linparams), label='Linear Function Fit', linestyle='-')
plt.errorbar(n, mean_times, yerr= 5 * errors, fmt='o', label='Data', color='r', alpha=1, linestyle='None')
# Labels and title
plt.xlabel('Number of points')
plt.ylabel('Execution time (s)')
plt.title('Linear Function Fit')

# Move legend to the top
plt.legend(loc='best', bbox_to_anchor=(0.5, 0.95), ncol=2)
plt.savefig('linear_function_fit_loglog.pdf', format='pdf')
plt.show()
plt.close()

plt.figure(figsize=(8, 6))
plt.plot(x, linear(x, *linparams), label='Linear Function Fit', linestyle='-')
plt.errorbar(n, mean_times, yerr=errors, fmt='o', label='Data', color='r', alpha=1, linestyle='None')
# Labels and title
plt.xlabel('Number of points')
plt.ylabel('Execution time (s)')
plt.title('Linear Function Fit')

# Move legend to the top
plt.legend(loc='best', bbox_to_anchor=(0.5, 0.95), ncol=2)
plt.savefig('linear_function_fit.pdf', format='pdf')
plt.show()
plt.close()