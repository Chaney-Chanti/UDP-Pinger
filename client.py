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

pingTimes = []
# Send and receive 10 requests.
for i in range(numPings):
    startTime = time() # Retrieve the current time
    message = "Chaney " + str(i+1) + ' ' + str(date.today()) + " " + ctime(startTime)[11:19]
    try:
        # Sending the message and waiting for the answer
        clientSocket.sendto(message.encode(),(serverHost, int(serverPort)))
        encodedModified, serverAddress = clientSocket.recvfrom(1024)

        # Checking the current time and if the server answered
        endTime = time()

        # Modified message is decoded.
        # Prints the RTT
        modifiedMessage = encodedModified.decode()
        print('Chaney %i: server reply: ' % (i+1) + modifiedMessage + ', ' + "RTT = %.3f ms\n" % ((endTime - startTime)*1000))
        pingTimes.append(float((endTime - startTime)*1000))

    except:
        print("PING %i Request timed out\n" % (i+1))
        
    if i == numPings - 1: sucConn = True

if sucConn == True:
    print('Summary:')
    print("Min Trip Time: %.3f ms" % (min(pingTimes)))
    print("Max Trip Time: %.3f ms" % (max(pingTimes)))
    print("Avg Trip Time: %.3f ms" % (statistics.mean(pingTimes)))
    print("Percentage Packet Loss Rate: %.3f ms" % ((endTime - startTime)*1000))


clientSocket.close()

#Reqs:
    #Info:
    # send a specified number of poings
    # client cannot wait indeinitley for a reply to a ping message
    # (wait 1 second for a reply, if not packet, assume it was lost)
#Send the ping message using UDP

# print the response message from server if any was received
# calcualte and print the RTT, in milliseconds of each packet if the server respones otherwise print timeout
# provide a summary report at the end of all pings which includes
#     Min RTT
#     Max RTT
#     average RTT
#     percentage packet loss rate