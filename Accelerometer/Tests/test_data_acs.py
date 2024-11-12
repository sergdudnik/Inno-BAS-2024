import unittest
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Source.data_acs import data_acs

class TestDataAcs(unittest.TestCase):
    def test_data_processing(self):
        accel_data = [[2, 2, 2], [5, 5, 5], [8, 8, 8]]
        result = data_acs(accel_data)

        self.assertAlmostEqual(result['acceleration'][0], 2.0)
        self.assertAlmostEqual(result['acceleration'][1], 5.0)
        self.assertAlmostEqual(result['acceleration'][2], 8.0)

        self.assertAlmostEqual(result['inclination'][0], 11.96946312460731, places=2)
        self.assertAlmostEqual(result['inclination'][1], 31.23006977557103, places=2)

def plot_acceleration(accel_data):
    plt.figure(figsize=(10,5))
    plt.plot(accel_data[0], label='Acceleration X')
    plt.plot(accel_data[1], label='Acceleration Y')
    plt.plot(accel_data[2], label='Acceleration Z')
    plt.title("Acceleration Data")
    plt.xlabel("Samples")
    plt.ylabel("Acceleration (g)")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    unittest.main(verbosity=2)
    plot_acceleration(accel_data)