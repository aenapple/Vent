import matplotlib.pyplot as plt


def transform_data(file_name, t_array, s_array):
    file_input = open(file_name, 'r')
    for line in file_input:
        x = line.find('11/26/2020')
        if x != 0:
            continue

        str_record = line.replace('11/26/2020-', '')
        # minutes = int(str_record[0:2])
        # seconds = int(str_record[3:5])
        s_array.append(int(str_record[6:8]) + (int(str_record[3:5]) * 60) + (int(str_record[0:2]) * 3600))
        # t1 = int(str_record[13:17])
        # t2 = int(str_record[18:22])
        # t3 = int(str_record[23:27])
        t = (int(str_record[16:20]) + int(str_record[21:25]) + int(str_record[26:30])) / 300
        t_array.append(t)
        print(str_record, end='')

    file_input.close()


if __name__ == '__main__':
    __doc__ = """
    ....
    """

    # file_input = open('LogTemperature_4.txt', 'r')
    # str_record = file_input.readline()

    t1 = []
    t2 = []
    # t3 = []
    s1 = []
    s2 = []
    # s3 = []
    # transform_data('LogTemperature_4.txt', t1, s1)  # room-sensor
    # transform_data('LogTemperature_C.txt', t2, s2)  # vent-sensor
    transform_data('LogTemperature_6.txt', t1, s1)  # room-sensor
    # transform_data('LogTemperature_9.txt', t2, s2)  # vent-sensor
    transform_data('LogTemperature_B.txt', t2, s2)  # vent-sensor

    fig, ax = plt.subplots()
    ax.plot(s1, t1, label="room-sensor")
    ax.plot(s2, t2, label="vent1-sensor")
    # ax.plot(s3, t3, label="vent2-sensor")

    # ax.set_xlim(0, 5)
    # ax.set_ylim(0, 10)
    ax.set(xlabel='time', ylabel='temperature', title='Bedroom')
    # ax.set(xlabel='time', ylabel='temperature', title='Cabinet')
    ax.grid()

    # fig, ax = plt.subplots(2, 1)
    # fig.subplots_adjust(hspace=0.7)  # make a little extra space between the subplots

    # ax[0].plot([1, 2, 3, 4], [1, 4, 2, 3], label='A')
    # ax[0].plot([1, 3, 3, 4], [1, 3, 2, 4], label='B')
    # ax[0].set_xlim(0, 5)
    # ax[0].set_ylim(0, 10)
    # ax[0].set(xlabel='time', ylabel='temperature', title='Cabinet')
    # ax[0].grid()

    # ax[1].plot([1, 2, 3, 4], [1, 4, 2, 3], label="X")
    # ax[1].plot([1, 3, 3, 4], [1, 3, 2, 4], label='Y')
    # ax[1].set_xlim(0, 5)
    # ax[1].set_ylim(0, 10)
    # ax[1].set(xlabel='time', ylabel='temperature', title='Bedroom')
    # ax[1].grid()

    plt.legend()
    plt.show()

    print("OK")

