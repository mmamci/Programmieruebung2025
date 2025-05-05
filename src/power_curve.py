from load_data import load_data
from sort import bubble_sort
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    data = load_data('data/activity.csv')
    power_W = data['PowerOriginal']
    sorted_power_W = bubble_sort(power_W)
    time_s = np.array(range(len(sorted_power_W)))

    plt.style.use('seaborn-v0_8-dark')
    plt.plot(time_s/60 ,sorted_power_W[::-1], color = "#83c6e7")
    plt.fill_between(time_s / 60, sorted_power_W[::-1], color='#b1d1e2', alpha = 0.3)
    plt.grid(True)

    plt.title('Leistungskurve')
    plt.xlabel('Zeit in Minuten')
    plt.ylabel('Watt')
    #plt.show()

    plt.savefig("figures/fig.png")
    