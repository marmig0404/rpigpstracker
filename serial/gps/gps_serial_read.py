import serial  # import serial pacakge
from time import sleep
import sys  # import system package


def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]  # extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]  # extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]  # extract longitude from GPGGA string
    print("NMEA Time: ", nmea_time, '\n')
    print("NMEA Latitude:", nmea_latitude,
          "NMEA Longitude:", nmea_longitude, '\n')
    lat = float(nmea_latitude)  # convert string into float for calculation
    longi = float(nmea_longitude)  # convertr string into float for calculation
    # get latitude in degree decimal format
    lat_in_degrees = convert_to_degrees(lat)
    # get longitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi)

# convert raw NMEA string into degree decimal format


def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" % (position)
    return position


gpgga_info = "$GPGGA,"
ser = serial.Serial("/dev/ttyS0")  # Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
while True:
    received_data = (str)(ser.readline())  # read NMEA string received
    GPGGA_data_available = received_data.find(
        gpgga_info)  # check for NMEA GPGGA string
    if (GPGGA_data_available > 0):
        # store data coming after "$GPGGA," string
        GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]
        # store comma separated data in buffer
        NMEA_buff = (GPGGA_buffer.split(','))
        GPS_Info()  # get time, latitude, longitude
        print("lat in degrees:", lat_in_degrees,
              " long in degree: ", long_in_degrees, '\n')
        print("------------------------------------------------------------\n")
