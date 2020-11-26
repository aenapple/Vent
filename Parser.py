import matplotlib.pyplot as plt


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3], label="X")
    ax.plot([1, 3, 3, 4], [1, 3, 2, 4], label="Y")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)
    ax.set(xlabel='time', ylabel='temperature', title='Bedroom')
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

