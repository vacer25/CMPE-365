import sys
import random

part = 1            # Corresponds to question number, set as the first argument in the command line to change

MIN_ARRIVE_DEPART_TIME = 0.5 # At least 30 minutes between arrival and departure

# Helper function to get the first element in a tuple, used for sorting
def GetFirstElement(elem):
    return elem[0]


# Function to calculate the minimum number of terminals required to fit the planes in the airport
def GetMinTerminals(arriveTimesIn, departTimesIn):

    # Set up variables
    numTerminals = 0
    numPlanesInAirport = 0

    # Add a "1" label to all the arrivals and a "-1" label to all the departures
    arriveTimes = [(_, 1) for _ in arriveTimesOriginal]
    departTimes = [(_, -1) for _ in departTimesOriginal]
    
    # Add all the events to one list and sort them by increasing size
    allTimes = sorted(arriveTimes + departTimes, key = GetFirstElement)
    #print(allTimes)

    # Loop through all the events
    for currentEvent in allTimes:

        # Add or subract from the number of planes in the airport, depending on if the event is an arrival or departure
        numPlanesInAirport += currentEvent[1]

        # The number of terminals is the max number of planes in the airport at once
        numTerminals = max(numTerminals, numPlanesInAirport)

    return numTerminals

# Main function
if __name__ == "__main__":

    # Get the question number as the first argument
    try:
        part = int(sys.argv[1])
    except:
        pass

    # ==================== # OF TERMINALS ====================
    
    if(part == 1 or part == 2 or part == 3):    

        # Load the arrival and departure times
        arriveTimesOriginal = [float(arriveTimesOriginal.rstrip('\n')) for arriveTimesOriginal in open('start1.csv')]
        departTimesOriginal = [float(departTimesOriginal.rstrip('\n')) for departTimesOriginal in open('finish1.csv')]

        if(part == 1):

            # Calculate the number of required terminals
            numTerminals = GetMinTerminals(arriveTimesOriginal, departTimesOriginal)

            # Print the required number of terminals
            print(numTerminals)

        if(part == 2 or part == 3):

            if(part == 3):

                # Get the departure delay time as the second argument
                try:
                    departDelay = float(sys.argv[2])
                except:
                    departDelay = 1 # A whole hour by default
            
            # For 0% to 100% of the airplanes
            for percentLate in range(0, 101):

                # Re-load the times with no delays
                arriveTimes = arriveTimesOriginal
                departTimes = departTimesOriginal

                # Loop over all the arrival and departure times
                for i in range(0, len(arriveTimesOriginal)):

                    # Delay the random percentage of airplanes
                    if(random.randrange(0, 100) < percentLate):

                        # Continue doing this
                        while(True):

                            # Generate random arrival and departure delays of either 0, 15, 30, 45, or 60 minutes each
                            if(part == 2):
                                randomArriveDelay = random.randint(0, 4) * 0.25
                                randomDepartDelay = random.randint(0, 4) * 0.25

                            # Generate no arrival delays and departure delays of 60 minutes each
                            elif(part == 3):
                                randomArriveDelay = 0 # On time
                                randomDepartDelay = departDelay

                            # If the arrival time is still earlier than the departure time by the threshold, the delays are ok
                            if(arriveTimes[i] + randomArriveDelay + MIN_ARRIVE_DEPART_TIME < departTimes[i] + randomDepartDelay):
                                break

                        # Apply the delays
                        arriveTimes[i] += randomArriveDelay
                        departTimes[i] += randomDepartDelay

                # Calculate the number of required terminals
                numTerminals = GetMinTerminals(arriveTimes, departTimes)

                # Print the required number of terminals
                print(numTerminals)