import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import spidev
import sacn
import time


# Sacn
# provide an IP-Address to bind to if you are using Windows and want to use multicast
sender = sacn.sACNsender()
sender.start()  # start the sending thread
sender.activate_output(4)  # start sending out data in the 1st universe
sender[4].multicast = True  # set multicast to True

sender[4].dmx_data = (255, 0, 0)  # some test DMX data
sender[4].dmx_data = (255, 0, 0)  # some test DMX data

time.sleep(10)  # send the data for 10 seconds
sender.stop()  # do not forget to stop the sender


# Radio
GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
radio.setPayloadSize(32)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()

radio.startListening()

while True:
    ackPL = [1]
    while not radio.available(0):
        time.sleep(1/100)
    time.sleep(1)
    recievedMessage = []
    radio.read(recievedMessage, radio.getDynamicPayloadSize())
    print("Recieved: ", recievedMessage)

    print("Translating recieved message")

    string = ""

    for n in recievedMessage:
        # To unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)

    print("decoded message", string)
    radio.writeAckPayload(1, ackPL, len(ackPL))

    print("Loaded payload reploy", ackPL)
