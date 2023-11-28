# daemon_script.py
# -*- coding: utf-8 -*-

import threading
import time
from DB import Database
import adafruit_dht
import board

class SensorDaemon:
    def __init__(self):
        self.dht_sensor = adafruit_dht.DHT11(board.D21)

    def save_sensor_data(self, db):
        while True:
            humidity_data = self.dht_sensor.humidity
            temperature_data = self.dht_sensor.temperature

            if humidity_data is not None and temperature_data is not None:
                now = time.localtime()
                nowtime = ("%04d/%02d/%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

                print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(
                    temperature_data, humidity_data))
                humi = round(humidity_data, 2)
                temper = round(temperature_data, 2)
                db.insert(nowtime, humi, temper)

            time.sleep(60)  # Save data every minute

    def update_realtime_data(self, db):
        MAX_RETRIES = 3

        while True:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    humidity_data = self.dht_sensor.humidity
                    temperature_data = self.dht_sensor.temperature
                    if humidity_data is not None and temperature_data is not None:
                        now = time.localtime()
                        nowtime = ("%04d/%02d/%02d %02d:%02d:%02d" % (
                            now.tm_year, now.tm_mon, now.tm_mday,
                            now.tm_hour, now.tm_min, now.tm_sec))
                        print('Realtime - Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(
                            temperature_data, humidity_data))
                        humi = round(humidity_data, 2)
                        temper = round(temperature_data, 2)

                        # Check if there is any data in the 'realtime' table
                        existing_data = db.show_realtime()
                        if existing_data:
                            # If data exists, update the existing record
                            db.update_realtime(nowtime, humi, temper)
                        else:
                            # If no data exists, insert a new record
                            db.insert_realtime(nowtime, humi, temper)

                        # Break out of the retry loop if the data is successfully read
                        break
                    else:
                        print('Realtime - Failed to get reading. Retrying...')
                except RuntimeError as e:
                    print(f"Realtime - Error reading sensor data: {e}")
                    retries += 1
                    time.sleep(1)  # Adjust the delay as needed
            else:
                print("Realtime - Exceeded maximum retries. Unable to read sensor data.")

            time.sleep(1)  # Wait for 1 second before the next reading

    def run_daemon(self):
        db_sensor = Database()
        db_realtime = Database()

        thread_save = threading.Thread(target=self.save_sensor_data, args=(db_sensor,))
        thread_update = threading.Thread(target=self.update_realtime_data, args=(db_realtime,))

        thread_save.start()
        thread_update.start()

        thread_save.join()
        thread_update.join()

if __name__ == "__main__":
    daemon = SensorDaemon()
    daemon.run_daemon()
