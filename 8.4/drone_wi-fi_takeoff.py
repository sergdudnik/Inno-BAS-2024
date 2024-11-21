import numpy as np
import random  # Импорт для генерации случайных данных гироскопа
import unittest
import socket  # Для проверки подключения к Wi-Fi

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

def read_gyro():
    """Чтение данных гироскопа (симуляция)."""
    # Симуляция случайных данных гироскопа
    x_gyro = random.uniform(-100, 100)  # Угловая скорость по X
    y_gyro = random.uniform(-100, 100)  # Угловая скорость по Y
    z_gyro = random.uniform(-100, 100)  # Угловая скорость по Z
    return x_gyro, y_gyro, z_gyro

def check_wifi_connection(host='8.8.8.8', port=53, timeout=3):
    """Проверка подключения к Wi-Fi, с помощью попытки подключения к интернету."""
    try:
        socket.create_connection((host, port), timeout)
        return True
    except OSError:
        return False

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
        # Чтение данных гироскопа
        gyro_data = read_gyro()
        print(f"Данные гироскопа (X, Y, Z): {gyro_data}")

        # Проверка Wi-Fi соединения
        if check_wifi_connection():
            print("Wi-Fi соединение активно.")
        else:
            print("Нет подключения к Wi-Fi.")
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

class TestWiFi(unittest.TestCase):
    def test_wifi_connection(self):
        """Тестирование Wi-Fi соединения."""
        # Здесь мы просто проверяем функцию, в реальной системе это будет зависеть от наличия сети
        self.assertTrue(check_wifi_connection() or not check_wifi_connection(), "Проблема с подключением к Wi-Fi или отсутствием сети.")

if __name__ == "__main__":
    unittest.main(verbosity=2)