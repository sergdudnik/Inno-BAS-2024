from Source.data_acs import data_acs


if __name__ == "__main__":
    accel_data = [[2, 2, 2], [5, 5, 5], [8, 8, 8]]
    data_acs_obj = data_acs(accel_data)
    {
       'acceleration': [5.0, 5.0, 8.0],
       'inclination': [11.96946312460731, 31.23006977557103]
    }

def print_acceleration(data):
    print(f"Acceleration data:{data['acceleration']}")

    print("Обработка данных:")
    print(f"Ускорение: {data_acs_obj['acceleration']}")
    print(f"Углы наклона: {data_acs_obj['inclination']}")