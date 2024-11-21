import numpy as np
import unittest

# Константы для параметров БПЛА
MAX_PAYLOAD = 1500  # максимальная взлетная масса в граммах
MAX_FLIGHT_TIME = 30 * 60  # максимальное время полета в секундах
MAX_CONTROL_DISTANCE = 1000  # максимальная дальность управления в метрах

def data_acs(accel_data, weight, flight_time, control_distance, is_taking_off):
    """Обработка данных с акселерометра с учетом параметров БПЛА."""
    
    if weight > MAX_PAYLOAD:
        raise ValueError("Превышена максимальная взлетная масса БПЛА.")
    
    if flight_time > MAX_FLIGHT_TIME:
        raise ValueError("Превышено максимальное время полета.")
    
    if control_distance > MAX_CONTROL_DISTANCE:
        raise ValueError("Превышена максимальная дальность управления.")
    
    # Рассчитываем средние значения
    acceleration_x = np.mean(accel_data[0])
    acceleration_y = np.mean(accel_data[1])
    acceleration_z = np.mean(accel_data[2])
    
    if is_taking_off:
        # При взлете мы ожидаем увеличение ускорения по Z.
        acceleration_z += 9.81  # Добавляем ускорение, учитывая гравитацию

    # Теперь, если угол наклона все еще растет из-за взлета, мы можем вычислить наклон
    inclination_x = np.arctan2(acceleration_y, np.sqrt(np.square(acceleration_x) + np.square(acceleration_z))) * 180 / np.pi
    inclination_y = np.arctan2(acceleration_x, np.sqrt(np.square(acceleration_y) + np.square(acceleration_z))) * 180 / np.pi

    # Углы наклона должны быть равны 0, если БПЛА находится в равновесии
    if is_taking_off and acceleration_z > 9.81:
        inclination_x = 0.0
        inclination_y = 0.0

    return {
        "acceleration": [acceleration_x, acceleration_y, acceleration_z],
        "inclination": [inclination_x, inclination_y]
    }

def drone_takeoff(weight):
    """Функция для управления взлетом БПЛА."""
    if weight <= MAX_PAYLOAD:
        return "БПЛА готов к взлету."
    else:
        raise ValueError("Не удается взлететь. Превышена максимальная взлетная масса.")

# Начиная с основного выполнения кода
if __name__ == "__main__":
    accel_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Данные акселерометра
    weight = 1200  # масса БПЛА в граммах
    flight_time = 1600  # время полета в секундах
    control_distance = 800  # дальность управления в метрах
    is_taking_off = True  # Флаг для обозначения взлета

    try:
        data_acs_obj = data_acs(accel_data, weight, flight_time, control_distance, is_taking_off)
        print("Обработка данных:")
        print(f"Ускорение: {data_acs_obj['acceleration']}")
        print(f"Углы наклона: {data_acs_obj['inclination']}")
        print(drone_takeoff(weight))  # Вызов функции взлета
    except ValueError as e:
        print(e)

class TestDroneControl(unittest.TestCase):
    def test_takeoff_success(self):
        weight = 1200  # допустимая масса БПЛА
        result = drone_takeoff(weight)
        self.assertEqual(result, "БПЛА готов к взлету.")

    def test_takeoff_failure(self):
        weight = 1600  # превышение массы БПЛА
        with self.assertRaises(ValueError):
            drone_takeoff(weight)

class TestDataAcs(unittest.TestCase):
    def test_data_processing_takeoff(self):
        # Данные акселерометра предполагаются как равные нулю
        accel_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Настроенный на актуальные данные
        weight = 1200  # допустимая масса БПЛА
        flight_time = 1600  # допустимое время полета
        control_distance = 800  # допустимая дальность управления
        is_taking_off = True  # Симуляция взлета

        result = data_acs(accel_data, weight, flight_time, control_distance, is_taking_off)

        # Ожидаем, что ускорение по Z будет равно 9.81, отразить влияние гравитации.
        self.assertAlmostEqual(result['acceleration'][0], 0.0)  # Ускорение по X
        self.assertAlmostEqual(result['acceleration'][1], 0.0)  # Ускорение по Y
        self.assertAlmostEqual(result['acceleration'][2], 9.81)  # Ускорение по Z

        # Проверка углов наклона
        self.assertAlmostEqual(result['inclination'][0], 0.0, places=2)  # Угол наклона по X должен быть 0
        self.assertAlmostEqual(result['inclination'][1], 0.0, places=2)  # Угол наклона по Y должен быть 0

if __name__ == "__main__":
    unittest.main(verbosity=2)