import sys

useOptimizedLooping = False

doesConverge = []
doesConvergeListSizeMultiplier = 1

def CollatzLoop(initialValue):

    x = initialValue        # Current value
    maxValue = 0            # The maximum value that x was durring the looping
    iterations = 0          # How many iterations were done

    # print(f"{x}")           # Print initial value
    while x != 1:

        if(useOptimizedLooping):
            if(x < len(doesConverge) and doesConverge[x]):
                # print(f"For init value: {initialValue}, stopped at {x}")
                break

        iterations += 1

        if x % 2 == 0:      # If x is even
            x = x // 2
        else:               # If x is odd
            x = x * 3 + 1

        maxValue = max(maxValue, x)

        #print(f"{x}")       # Print value after each iteration

    if(useOptimizedLooping):
        doesConverge[initialValue] = True

    return iterations, maxValue

def RunCollatzLoops(maxValue):

    #print(f"From 1 UP TO {maxValue}")

    # Try each value from 1 to max value
    for currentInitValue in range(1, maxValue + 1):
        currentNumberOfIteration, currentMaxValue = CollatzLoop(currentInitValue)

        print(f"{currentInitValue}, {currentNumberOfIteration}, {currentMaxValue}")


    #print(f"From {maxValue} DOWN TO 1")

    #for i in range(1, maxValue + 1):
    #    doesConverge[i] = False

    # Try each value from max value to 1
    #for currentInitValue in range(maxValue, 1, -1):
        #currentNumberOfIteration, currentMaxValue = CollatzLoop(currentInitValue)

        #print(f"{currentInitValue}, {currentNumberOfIteration}, {currentMaxValue}")


if __name__ == "__main__":

    # Get the max value
    maxValue = int(sys.argv[1])

    # Initialize the list of values known to converge 
    doesConverge = [False] * ((maxValue * doesConvergeListSizeMultiplier) + 1)

    # Run the loops!
    print(f"Init val, iterations, max val")
    RunCollatzLoops(maxValue)

    #CollatzLoop(maxValue)
