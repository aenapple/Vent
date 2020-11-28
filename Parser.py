import matplotlib.pyplot as plt


def transform_data(file_name):
    t_array = []
    s_array = []
    file_input = open(file_name, 'r')
    for line in file_input:
        x = line.find('11/27/2020')
        if x != 0:
            continue

        str_record = line.replace('11/27/2020-' , '')
        # minutes = int(str_record[0:2])
        # seconds = int(str_record[3:5])
        s_array.append(int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600))
        # t1 = int(str_record[13:17])
        # t2 = int(str_record[18:22])
        # t3 = int(str_record[23:27])
        # t = int(str_record[16:20] + int(str_record[21:25]) + int(str_record[26:30])) / 300
        t_array.append((int(str_record[16:20]) + int(str_record[21:25]) + int(str_record[26:30])) / 300)
        print(str_record, end='')

    file_input.close()
    return t_array, s_array


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    fig, ax = plt.subplots()

    data = transform_data('LogTemperature_4.txt')  # room-sensor
    ax.plot(data[1], data[0], label="l-room-sensor")

    data = transform_data('LogTemperature_B.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="l-vent1-sensor")

    data = transform_data('LogTemperature_C.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="l-vent2-sensor")

    data = transform_data('LogTemperature_3.txt')  # room-sensor
    ax.plot(data[1], data[0], label="b-room-sensor")

    data = transform_data('LogTemperature_6.txt')  # room-sensor
    ax.plot(data[1], data[0], label="b-vent1-sensor(isolated)")

    data = transform_data('LogTemperature_9.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="b-vent2-sensor")

    # ax.set_xlim(0, 5)
    # ax.set_ylim(0, 10)
    ax.set(xlabel='time', ylabel='temperature', title='Liv+Bed rooms')
    ax.grid()
    plt.legend()
    plt.show()

    print("OK")

