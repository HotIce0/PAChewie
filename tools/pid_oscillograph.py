import matplotlib.pyplot as plt  # 导入模块
import csv


def show(filename):
    line_styles = ['r', 'g', 'b', 'r', 'g', 'b', 'y']
    data = []
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        while True:
            try:
                row = next(csv_reader)
            except Exception as e:
                break
            data.append(row)

    time = 0
    times = []

    pid_rolls = []
    pid_pitchs = []
    pid_yaw = []

    pwms_val1 = []
    pwms_val2 = []
    pwms_val3 = []
    pwms_val4 = []
    for row in data:
        delta_time = int(row[0])
        time += delta_time
        times.append(time)

        pid_rolls.append(float(row[1]))
        pid_pitchs.append(float(row[2]))
        pid_yaw.append(float(row[3]))

        pwms_val1.append(float(row[4]))
        pwms_val2.append(float(row[5]))
        pwms_val3.append(float(row[6]))
        pwms_val4.append(float(row[7]))

    plt.plot(
        times, pid_rolls, line_styles[0],
        times, pid_pitchs, line_styles[1],
        times, pid_yaw, line_styles[2],
        #
        linewidth=1,
    )
    plt.show()  # 输出图像
    plt.plot(
        times, pwms_val1, line_styles[3],
        times, pwms_val2, line_styles[4],
        times, pwms_val3, line_styles[5],
        times, pwms_val4, line_styles[6],
        linewidth=1,
    )
    plt.show()


show("pid.txt")
