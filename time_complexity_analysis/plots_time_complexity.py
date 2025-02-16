import numpy as np
import matplotlib.pyplot as plt
import os

def damped_sine_with_noise(t, omega=2*np.pi, noise_level= 1):
    signal = np.sin(omega * t)
    noise = noise_level * np.random.randn(len(t))
    return signal + noise

def gausian_noise(x, A=1, mu=5, sigma=0.75, noise_level=0.1):
    signal = A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    noise = noise_level * np.random.randn(len(x))
    return signal + noise


n_data = np.array([10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 250000, 500000, 750000, 1000000, 1500000, 2000000])

# Generate time values
for k in range(1, 9):
    directory = 'noisy_gaussian_' + str(k)
    os.makedirs(directory, exist_ok=True)
    for i in n_data:
        print(int(i))
        t = np.linspace(0, 10, int(i))
        y = gausian_noise(t)

        # Plot the function
        plt.figure(figsize=(8, 5))
        plt.scatter(t, y, label='Gaussian with noise', color='r', alpha=1, s=10)
        plt.markers = "o"
        plt.xlabel('x')
        plt.ylabel('Amplitude')
        plt.xlim(0, 10)
        plt.ylim(-0.7, 1.7)
        plt.title('Gaussian Function with Noisy Points')
        plt.legend()
        plt.savefig(directory + '/noisy_gauss' + str(int(i)) + '.svg', format='svg')
        plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(0, 1000, label='Gaussian with noise', color='r', alpha=1, s=10)
    plt.markers = "o"
    plt.xlabel('x')
    plt.ylabel('Amplitude')
    plt.xlim(0, 10)
    plt.ylim(-0.7, 1.7)
    plt.title('Gaussian Function with Noisy Points')
    plt.legend()
    plt.savefig(directory + '/clear.svg', format='svg')
    plt.close()