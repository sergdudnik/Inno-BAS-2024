import numpy as np

def data_acs(accel_data):
    """
    Обработка данных с акселерометра.

    Args:
        accel_data: Список значений ускорения по осям X, Y, Z (g).
    
    Returns:
        Словарь с обработанными данными:
        - acceleration: Список значений ускорения (g).
        - inclination: Список углов наклона по осям X, Y (град).
    """

    acceleration_x = np.mean(accel_data[0])
    acceleration_y = np.mean(accel_data[1])
    acceleration_z = np.mean(accel_data[2])
    
    inclination_x = np.arctan2(acceleration_x, np.sqrt(np.square(acceleration_y) + np.square(acceleration_z))) * 180 / np.pi
    inclination_y = np.arctan2(acceleration_y, np.sqrt(np.square(acceleration_x) + np.square(acceleration_z))) * 180 / np.pi
    
    return {
        "acceleration": [acceleration_x, acceleration_y, acceleration_z],
        "inclination": [inclination_x, inclination_y]
    }

accel_data = [[2, 2, 2], [5, 5, 5], [8, 8, 8]]

data_acs_obj = data_acs(accel_data)

print("Обработка данных:")
print(f"Ускорение: {data_acs_obj['acceleration']}")
print(f"Углы наклона: {data_acs_obj['inclination']}")