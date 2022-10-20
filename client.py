from socket import *
from time import time, ctime
from datetime import date
import sys
import statistics

# Inputs four arguments.
if (len(sys.argv) != 4):
    print(len(sys.argv))
    print("Wrong number of arguments.")
    print("Use: client.py <server_host> <server_port> <num_pings>")
    sys.exit()

# Preparing the socket
serverHost, serverPort, numPings = sys.argv[1:]
numPings = int(numPings)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1) # sets the timeout to 1 second
sucConn = False
numLostPackets = 0

pingTimes = []
# Send and receive 10 requests.
for i in range(numPings):
    startTime = time() # Retrieve the current time
    message = "Chaney " + str(i+1) + ' ' + str(date.today().strftime('%A')) + ' ' + str(date.today().strftime("%b")) + ' ' + str(date.today().day) + " " + ctime(startTime)[11:19] + ' ' + str(date.today().year)
    try:
        # Sending the message and waiting for the answer
        clientSocket.sendto(message.encode(),(serverHost, int(serverPort)))
        encodedModified, serverAddress = clientSocket.recvfrom(1024)

        # Checking the current time and if the server answered
        endTime = time()

        # Modified message is decoded.
        # Prints the RTT
        modifiedMessage = encodedModified.decode()
        print('Chaney %i: server reply: ' % (i+1) + modifiedMessage + ', ' + "RTT = %.3f ms" % ((endTime - startTime)*1000))
        pingTimes.append(float((endTime - startTime)*1000))
        if float((endTime - startTime)*1000) >= 1:
            numLostPackets += 1

    except:
        print("PING %i Request timed out\n" % (i+1))
        
    if i == numPings - 1: sucConn = True

if sucConn == True:
    print('Summary:')
    print("Min RTT =  %.3f ms" % (min(pingTimes)))
    print("Max RTT = : %.3f ms" % (max(pingTimes)))
    print("Avg RTT = : %.3f ms" % (statistics.mean(pingTimes)))
    print("Packet lost =  %.3f" % (numLostPackets / numPings) + '%')


clientSocket.close()