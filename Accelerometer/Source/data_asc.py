import time
import numpy as np
def data_acs(accel_data):
    Args:
        accel_data: Список значений ускорения по осям X, Y, Z (g)
    Returns:
        Словарь с обработанными данными:
        - acceleration: Список значений ускорения (g).
        - inclination: Список углов наклона по осям X, Y (град).
    
    acceleration_x = np.mean(accel_data[0])
    acceleration_y = np.mean(accel_data[1])
    acceleration_z = np.mean(accel_data[2])

    inclination_x = np.arctan(acceleration_x / np.sqrt(acceleration_y + acceleration_z)) * 180 / np.pi
    inclination_y = np.arctan(acceleration_y / np.sqrt(acceleration_z + acceleration_z)) * 180 / np.pi
    return (
    "acceleration": [acceleration_x, acceleration_y, acceleration_z],
    "ïnclination": [inclination_x, inclination_y]
    )
