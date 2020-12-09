import matplotlib.pyplot as plt


def transform_data(number_module):
    t_array = []
    s_array = []

    str_temp = '-' + hex(number_module).replace('0x', '') + ':'
    file_input = open('LogTemperature.txt', 'r')
    file_csv = open('LogTemperature_' + hex(number_module).replace('0x', '') + '.csv', 'w')
    for line in file_input:
        if line.find(str_temp) < 0:  # wrong file line
            continue

        file_csv.write(line[0:10] + ',')
        str_record = line.replace(line[0:11], '')  # remove Date

        seconds = int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600)
        s_array.append(seconds)
        file_csv.write(str(seconds) + ',')

        if line.find('???') >= 0:  # empty line
            t = 15
        else:
            t = (float(str_record[18:23]) + float(str_record[18+6:23+6]) + float(str_record[18+12:23+12])) / 3

        t_array.append(t)
        file_csv.write(str(t) + ',' + '\n')
        print(str_record, end='')

    file_csv.close()
    file_input.close()
    return t_array, s_array

"""def transform_data(file_name):
    t_array = []
    s_array = []
    file_input = open(file_name, 'r')
    file_csv = open(file_name.replace('txt', 'csv'), 'w')
    for line in file_input:
        if (line.find('2020') < 0) or (line.find('ERR') >= 0) or (line.find('OK') >= 0):  # empty or error line
            continue

        file_csv.write(line[0:10] + ',')
        str_record = line.replace(line[0:11], '')  # remove Date

        seconds = int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600)
        s_array.append(seconds)
        file_csv.write(str(seconds) + ',')

        t = (int(str_record[16:20]) + int(str_record[21:25]) + int(str_record[26:30])) / 300
        t_array.append(t)
        file_csv.write(str(t) + ',' + '\n')
        print(str_record, end='')

    file_csv.close()
    file_input.close()
    return t_array, s_array"""


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    fig, ax = plt.subplots()

    str_label = [
        "m-liveroom-t1", # 2
        "m-liveroom-t2", # 3
        "m-liveroom-t3", # 4
        "d-liveroom-t1", # 5
        "d_bedroom-t1",  # 6
        "d_bedroom-t2",  # 7
        "m_bedroom-t1",  # 8
        "m_bedroom-t2",  # 9
        "d-bathroom-t",  # 10
        "m-bathroom-t",  # 11
        "cabinet-t",     # 12
        "???",  # 13
        "???",  # 14
        "???",  # 15
        "???",  # 16
    ]

    for i in range(2, 16):
        data = transform_data(i)  # room-sensor
        ax.plot(data[1], data[0], label=str_label[i-2])
        print(str_label[i-2])
        # print(i)


    """data = transform_data('Archive/12-01-2020/LogTemperature_4.txt')  # room-sensor
    ax.plot(data[1], data[0], label="l-room-sensor")

    data = transform_data('Archive/12-01-2020/LogTemperature_B.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="b-vent1-sensor")

    data = transform_data('Archive/12-01-2020/LogTemperature_C.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="b-vent2-sensor")

    data = transform_data('Archive/12-01-2020/LogTemperature_3.txt')  # room-sensor
    ax.plot(data[1], data[0], label="b-room-sensor")

    data = transform_data('Archive/12-01-2020/LogTemperature_6.txt')  # room-sensor
    ax.plot(data[1], data[0], label="l-vent1-sensor(isolated)")

    data = transform_data('Archive/12-01-2020/LogTemperature_9.txt')  # vent-sensor
    ax.plot(data[1], data[0], label="l-vent2-sensor")"""

    # ax.set_xlim(0, 5)
    # ax.set_ylim(0, 10)
    ax.set(xlabel='time', ylabel='temperature', title='Liv+Bed rooms')
    ax.grid()
    plt.legend()
    plt.show()

    print("OK")

