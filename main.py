import myo
import csv
from collections import deque
import datetime as dt
from msvcrt import getch
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import time
from pynput import keyboard


pressed = 0

EMG_DATA = deque()
emgVals = []
ORIENTATION_DATA = deque()
emg_timestamps = []
emg_1 = []
emg_2 = []
emg_3 = []
emg_4 = []
emg_5 = []
emg_6 = []
emg_7 = []
emg_8 = []

orientation_timestamps = []
orientation_1 = []
orientation_2 = []
orientation_3 = []
orientation_4 = []

acceleration_1 = []
acceleration_2 = []
acceleration_3 = []

gyroscope_1 = []
gyroscope_2 = []
gyroscope_3 = []


f, ((ax_emg, ax_orientation), (ax_acceleration, ax_gyroscope)) = plt.subplots(2, 2)

class Listener(myo.DeviceListener):
    def __init__(self, emg_filename='myo_emg.csv', orientation_filename='myo_orientation.csv'):
        self.emg_file = emg_filename
        self.orientation_file = orientation_filename



    def on_connected(self, event):
        print("A myo has connected!")
        event.device.stream_emg(True)

    def on_paired(self, event):
        print("Hello, {}!".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)

    def on_unpaired(self, event):
        self.write_emg_data()
        self.write_orientation_data()
        print('MYO unpaired')
        return False


    def on_orientation(self, event):
        orientation = event.orientation
        acceleration = event.acceleration
        gyroscope = event.gyroscope
        vals = [event.timestamp, orientation[0], orientation[1], orientation[2], orientation[3],
                acceleration[0],acceleration[1], acceleration[2], gyroscope[0],
                gyroscope[1], gyroscope[2]]
        orientation_timestamps.append(event.timestamp)
        orientation_1.append(orientation[0])
        orientation_2.append(orientation[1])
        orientation_3.append(orientation[2])
        orientation_4.append(orientation[3])
        acceleration_1.append(acceleration[0])
        acceleration_2.append(acceleration[1])
        acceleration_3.append(acceleration[2])
        gyroscope_1.append(gyroscope[0])
        gyroscope_2.append(gyroscope[1])
        gyroscope_3.append(gyroscope[2])
        ORIENTATION_DATA.append(vals)
        if(len(ORIENTATION_DATA) >= 10):
            self.write_orientation_data()

    def on_emg(self, event):
        emg = event.emg
        #if len(emgVals) == 0:
        emgVals.append(event.timestamp)
        #vals.append(event.timestamp)
        emgVals.append(emg[0])
        emgVals.append(emg[1])
        emgVals.append(emg[2])
        emgVals.append(emg[3])
        emgVals.append(emg[4])
        emgVals.append(emg[5])
        emgVals.append(emg[6])
        emgVals.append(emg[7])

        '''
        if len(emgVals) >= 64:
            self.write_emg_data()
            emgVals.clear()
        emg_timestamps.append(event.timestamp)
        emg_1.append(emg[0])
        emg_2.append(emg[1])
        emg_3.append(emg[2])
        emg_4.append(emg[3])
        emg_5.append(emg[4])
        emg_6.append(emg[5])
        emg_7.append(emg[6])
        emg_8.append(emg[7])
        '''
        if len(EMG_DATA) >= 10:
            print("EMG_DATA")
            print(EMG_DATA[0])
            self.write_emg_data()
        emgVals.clear()

    def on_pose(self, event):
        print(event.pose)

    def write_emg_data(self):
        global pressed
        with open(self.emg_file, 'a') as csvfile:
            if pressed != 0:
                print("wrote")
                pressed = pressed - 1
                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                writer.writerow(emgVals)


    def write_orientation_data(self):
        with open(self.orientation_file, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                while(len(ORIENTATION_DATA) > 0):
                    writer.writerow(ORIENTATION_DATA.popleft())


def animate(
    i, emg_timestamps, emg_1, emg_2, emg_3, emg_4, emg_5, emg_6, emg_7,
    emg_8, orientation_timestamps, orientation_1, orientation_2, orientation_3, orientation_4,
    acceleration_1, acceleration_2, acceleration_3, gyroscope_1, gyroscope_2, gyroscope_3):
    emg_timestamps = emg_timestamps[-140:]
    emg_1 = emg_1[-140:]
    emg_2 = emg_2[-140:]
    emg_3 = emg_3[-140:]
    emg_4 = emg_4[-140:]
    emg_5 = emg_5[-140:]
    emg_6 = emg_6[-140:]
    emg_7 = emg_7[-140:]
    emg_8 = emg_8[-140:]

    #ax_emg.clear()
    #ax_emg.plot(emg_timestamps, emg_1)
    #ax_emg.plot(emg_timestamps, emg_2)
    #ax_emg.plot(emg_timestamps, emg_3)
    # ax_emg.plot(emg_timestamps, emg_4)
    # ax_emg.plot(emg_timestamps, emg_5)
    # ax_emg.plot(emg_timestamps, emg_6)
    # ax_emg.plot(emg_timestamps, emg_7)
    # ax_emg.plot(emg_timestamps, emg_8)
    #ax_emg.set_xlabel('time in milliseconds')
    #fax_emg.set_ylabel('emg')

    orientation_timestamps = orientation_timestamps[-40:]
    orientation_1 = orientation_1[-40:]
    orientation_2 = orientation_2[-40:]
    orientation_3 = orientation_3[-40:]
    orientation_4 = orientation_4[-40:]
    ax_orientation.clear()
    ax_orientation.plot(orientation_timestamps, orientation_1)
    ax_orientation.plot(orientation_timestamps, orientation_2)
    ax_orientation.plot(orientation_timestamps, orientation_3)
    ax_orientation.plot(orientation_timestamps, orientation_4)
    ax_orientation.set_xlabel('time in milliseconds')
    ax_orientation.set_ylabel('orientation')

    acceleration_1 = acceleration_1[-40:]
    acceleration_2 = acceleration_2[-40:]
    acceleration_3 = acceleration_3[-40:]
    ax_acceleration.clear()
    ax_acceleration.plot(orientation_timestamps, acceleration_1)
    ax_acceleration.plot(orientation_timestamps, acceleration_2)
    ax_acceleration.plot(orientation_timestamps, acceleration_3)
    ax_acceleration.set_xlabel('time in milliseconds')
    ax_acceleration.set_ylabel('acceleration')


    gyroscope_1 = gyroscope_1[-40:]
    gyroscope_2 = gyroscope_2[-40:]
    gyroscope_3 = gyroscope_3[-40:]
    ax_gyroscope.clear()
    ax_gyroscope.plot(orientation_timestamps, gyroscope_1)
    ax_gyroscope.plot(orientation_timestamps, gyroscope_2)
    ax_gyroscope.plot(orientation_timestamps, gyroscope_3)
    ax_gyroscope.set_xlabel('time in milliseconds')
    ax_gyroscope.set_ylabel('gyroscope')



def temp_f(hub, listener):
    while hub.run(listener.on_event, 500):
        try:
            pass
        except KeyboardInterrupt:
            break

myo.init(sdk_path='./myo-sdk-win-0.9.0/')
hub = myo.Hub()
listener = Listener()


def thread1():
    def on_press(key):
        global pressed
        if key == keyboard.Key.space:
            pressed = 5
            print("pressed")

    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except Exception as e:
            print('{0} was pressed'.format(e.args[0]))


threading.Thread(target=temp_f, args=[hub, listener]).start()
#threading.Thread(target=thread1()).start()

time.sleep(6)
ani = animation.FuncAnimation(
    f, animate, fargs=(emg_timestamps, emg_1, emg_2, emg_3, emg_4, emg_5,
    emg_6, emg_7, emg_8, orientation_timestamps, orientation_1, orientation_2,
    orientation_3, orientation_4, acceleration_1, acceleration_2, acceleration_3,
    gyroscope_1, gyroscope_2, gyroscope_3), interval=200)


plt.show()