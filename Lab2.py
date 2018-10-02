import sys
import random
import itertools
#import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt

#inputList = [2, 4, 5, 13, -15, 7, 8, 1]
#inputList = [-2, -3, 4, -1, -2, 1, 5, -3]
#inputList = [-6, 2, 4, 5, -7, 3, -6, 1, 4]
#inputList = [-6, -3, -6, -7, -2, 4, -7, -1]

#inputList = [-17, 19, 28, 29]
#inputList = [14, 48, -19, 44, 26, -45, -48, 37]

minValue = -99999   # Minimum value used to replace the elements of the first segment sum. Used for simpliciy
iterations = 0      # Iteration counter
debugPrint = False  # Uncomment to see debugging info

part = 1            # Corresponts to question number

# Simple O(n^2) maximum segment sum
def simpleMSS(list):

    global iterations

    maxSum = -minValue
    maxSumStartingIndex = 0
    maxSumEndingIndex = 0
    listLength = len(list)

    for startingIndex in range(0, listLength):
        for endingIndex in range(startingIndex, listLength):

            iterations += 1

            currentSum = sum(list[startingIndex:endingIndex])
            if(currentSum > maxSum):
                maxSumStartingIndex = startingIndex
                maxSumEndingIndex = endingIndex
                maxSum = currentSum

    return list[maxSumStartingIndex:maxSumEndingIndex], maxSum


# Function to find the maximum contiguous subarray using Kadane's algorithm 
def KadaneMSS(list, start): 
	
    global iterations
    
    maxSoFar = minValue
    maxEndingHere = prevMaxEndingHere = startPos = endPos = 0
	
    for i in range(start, len(list)):
        iterations += 1
        maxEndingHere = maxEndingHere + list[i] 
        
        if debugPrint:
            print(f"i={i}, h={maxEndingHere}, m={maxSoFar}, v={list[i]}, s={startPos}, e={endPos}")

        if (maxSoFar < maxEndingHere):
            # Keep track of where the segment ends
            endPos = i
            maxSoFar = maxEndingHere
            if debugPrint:
                print(f"If 1")
            
        if maxEndingHere < 0:
            maxEndingHere = 0
            if debugPrint:
                print(f"If 2")

        if prevMaxEndingHere <= 0 and maxEndingHere > 0:
            # Keep track of where the segment starts
            startPos = i
            if debugPrint:
                print(f"If 3")

        prevMaxEndingHere = maxEndingHere

        if debugPrint:
            print(f"i={i}, h={maxEndingHere}, m={maxSoFar}, v={list[i]}, s={startPos}, e={endPos}")
    
    # Return the maximum segment
    return maxSoFar, startPos, endPos + 1
        
# Divide & Conquer maximum segment sum
def DCMSS(list, start, end):

    if debugPrint:
            print(f"[DCMSS]\n");

    global iterations
    iterations += 1
    
    #print(f"[{iterations}] Current: {list[start:end]}")

    # Base case: length = 1
    if(end - start == 1):

        if debugPrint:
            print(f"[Return] Base case: {list[start:end]}, from index {start} to {end}")

        # Return the element, the start index, and the end index
        return list[start], start, end

    # Recursive case: length > 1
    else:

        # Get the middle element
        mid = (start + end) // 2

        # For debugging
        if debugPrint:
            print(f"Recursive case: {list[start : end]}, start = {start}, end = {end}, mid = {mid}")
            print(f"Left list: {list[start : mid]}, Right list: {list[mid: end]}")

        # Divide and solve the left and right halves
        leftListSum, leftListSumStart, leftListSumEnd = DCMSS(list, start, mid)
        rightListSum, rightListSumStart, rightListSumEnd = DCMSS(list, mid , end)

        # Find the segment in the current list which is both in the left and right half
        midListTempSum = 0
        midListLeftSum = midListRightSum = minValue
        midListSumStart = midListSumEnd = 0

        # Find max sublist with max sum starting at midpoint down to start point (on left)
        for index in range(mid - 1, start - 1, -1):
            iterations += 1
            midListTempSum += list[index]
            if debugPrint:
                print(f"Added to mid left: {list[index]} at index {index}")
            if(midListTempSum > midListLeftSum):
                if debugPrint:
                    print(f"Set new mid list left max to: {midListTempSum} at index {index}")
                midListLeftSum = midListTempSum
                midListSumStart = index

        midListTempSum = 0

        # Find max sublist with max sum starting at midpoint up to end point point (on right)
        for index in range(mid, end):
            iterations += 1
            midListTempSum += list[index]
            if debugPrint:
                print(f"Added to mid right: {list[index]} at index {index}")
            if(midListTempSum > midListRightSum):
                if debugPrint:
                    print(f"Set new mid list left max to: {midListTempSum} at index {index}")
                midListRightSum = midListTempSum
                midListSumEnd = index

        # Total sum = sum of left + sum on right
        midListSum = midListLeftSum + midListRightSum
        # Adjust ending index
        midListSumEnd += 1

        # For debugging

        if debugPrint:
            print(f"Left:  {list[leftListSumStart : leftListSumEnd]} from index {leftListSumStart} to {leftListSumEnd}, sum = {leftListSum}")
            print(f"Right: {list[rightListSumStart : rightListSumEnd]} from index {rightListSumStart} to {rightListSumEnd}, sum = {rightListSum}")
            print(f"Mid:   {list[midListSumStart : midListSumEnd]} from index {midListSumStart} to {midListSumEnd}, sum = {midListSum}")

        # Determine which part has the largest sum
        maxSum = max(leftListSum, midListSum, rightListSum)

        # Return info about the largest sum
        if(maxSum == leftListSum):
            if debugPrint:
                print(f"[Return] Left had max")
            return maxSum, leftListSumStart, leftListSumEnd
        elif(maxSum == rightListSum):
            if debugPrint:
                print(f"[Return] Right had max")
            return maxSum, rightListSumStart, rightListSumEnd
        else:
            if debugPrint:
                print(f"[Return] Mid had max")
            return maxSum, midListSumStart, midListSumEnd

# Helper function to get a random list
def GetRandomList(num, min, max):

    randomList = []
    for i in range (num):
        randomList.append(random.randrange(min, max + 1, 1))

    return randomList

# Helper function to sort by 1st elements
def GetFirstElement(elem):
    return elem[0]


if __name__ == "__main__":

    # Get the max length of lists (part 1, 2, 3), and number of segments to find (part 3)
    maxLength = int(sys.argv[1])
    try:
        numSegments = int(sys.argv[2])
    except:
        numSegments = 1

    for length in range(1, maxLength + 1):
        inputList = GetRandomList(length, -50, 50)

        #print(f"[Input] List: {inputList}")

        # Simple O(n^2) MSS
        # maxList, maxSum = simpleMSS(inputList)

        # ==================== FIND FIRST MSS ====================

        if(part == 1):

            # Divide & Conquer MSS
            maxSum, maxSumStart, maxSumEnd = DCMSS(inputList, 0, len(inputList))
            maxList = inputList[maxSumStart : maxSumEnd]

            iterations1 = iterations    # Get iterations count
            iterations = 0              # Reset iterations

        # ==================== FIND SECOND MSS ====================

        if(part == 2):

            # Divide & Conquer MSS
            inputList2 = inputList.copy()
            for i in range(maxSumStart, maxSumEnd):
                inputList2[i] = minValue

            maxSum2, maxSumStart2, maxSumEnd2 = DCMSS(inputList2, 0, len(inputList2))
            maxList2 = inputList2[maxSumStart2 : maxSumEnd2]

            iterations2 = iterations    # Get iterations count
            iterations = 0              # Reset iterations

        # ==================== FIND K OVERLAPPING MSS'S ====================

        if(part == 3):

            maxSegments = []

            # Find all the possible segment sums
            for i in range(0, len(inputList)):
                maxSum, maxSumStart, maxSumEnd = KadaneMSS(inputList, i)
                maxList = inputList[maxSumStart : maxSumEnd]

                # Add the sum and segment to the list of all segments
                maxSegments.append((maxSum, maxList))

            # Remove the duplicate segments and sort in decreasing order by sum
            maxSegmentsSet = list(maxSegments for maxSegments, _ in itertools.groupby(maxSegments))
            maxSegments = maxSegmentsSet[:numSegments]

            iterations1 = iterations    # Get iterations count
            iterations = 0              # Reset iterations

        # ==================== PRINT RESULT ====================

        #print(f"From indexes {maxSumStart} to {maxSumEnd}")
        if(part == 1):
            print(f"{inputList}, {maxList}, {maxSum}, {iterations1}")
            #print(f"{iterations1}")

        if(part == 2):
            print(f"{inputList}, 1: {maxList}, {maxSum}, {iterations1}, 2: {maxList2}, {maxSum2}, {iterations2}, T: {iterations1 + iterations2}")
            #print(f"{iterations1 + iterations2}")

        if(part == 3):
            print(f"{inputList}, {maxSegments}, {iterations1}")
            #print(f"{iterations1}")