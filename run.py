from vacatempapi import *

manager = TempSensorManager(None)
manager.list_sensors()
manager.start()

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        break

manager.stop()
manager.join()
