import sys
import time
from random import random
import math
import itertools
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

CLUSTER_SIZE = 3

NUM_POINTS_MIN_PART_1_2 = 10
NUM_POINTS_MAX_PART_1_2 = 100
NUM_POINTS_STEP_PART_1_2 = 10
NUM_POINTS_PART_3_4 = 50

PLOT_SIZE_PART_1_2 = CLUSTER_SIZE * 2
PLOT_SIZE_PART_3_4 = CLUSTER_SIZE * 6

debugPrint = False  # Uncomment to see debugging info
part = 1            # Corresponts to question number, set as the first argument in the command line to change

# Generate a list of points around a center coordinate, using either uniform or normal distribution
def randomCluster(numberOfPoints, center , maxRadius, type):

    centerX, centerY = center
    randomPoints = []

    for i in range(numberOfPoints):
        currentAngle = 2 * math.pi * random()
        currentRadius = 0
        if(type == "Uniform"):
            currentRadius = np.random.uniform(low = 0, high = maxRadius)
        if(type == "Normal"):
            currentRadius = np.random.normal(loc = 0, scale = maxRadius / math.e)
        randomPoints.append((centerX + currentRadius * math.cos(currentAngle), centerY + currentRadius * math.sin(currentAngle)))

    return randomPoints


# Helper function to sort by 2st elements (y-coordinate)
def GetYCoordinate(elem):
    return elem[1]


# Find the convex hull of a list of points
def JarvisMarch(points):

    # List of points in the convex hull
    pointsCH = []

    # Flag to determine if angles need to be calculated relative to -ve x axis after the top point has been passed
    didReachTopPoint = False

    # Find the lowest and higgest points
    lowestPoint = min(points, key = GetYCoordinate)
    highestPoint = max(points, key = GetYCoordinate)

    # Start at the lowest point
    currentPoint = lowestPoint

    # Keep going around the points while the convex hull is not complete
    while True:

        # Flip direction at highest point
        if currentPoint == highestPoint:
            didReachTopPoint = True

        # Add the current point to the convex hull
        pointsCH.append(currentPoint)
        #print(f"Added {currentPoint}")

        # Find the next point, the one with the lowest polar angle with respect to the current point
        currentMinimumAngle = math.pi
        for currentPointToCheck in points:
            
            # Skip the current point, it is already in the convex hull
            if currentPointToCheck == currentPoint:
                continue

            # Calculate the polar angle from the current end of convex hull to the current point to test
            if(didReachTopPoint == False):
                currentPolarAngle = math.atan2((currentPointToCheck[1] - currentPoint[1]), (currentPointToCheck[0] - currentPoint[0]))
            else:
                currentPolarAngle = math.atan2((currentPoint[1] - currentPointToCheck[1]), (currentPoint[0] - currentPointToCheck[0]))

            # If the point is in the wrong direction, skip it
            if(currentPolarAngle < 0):
                continue

            # If this is the lowest angle so far, set the current point to test at the possible next point
            if(currentPolarAngle < currentMinimumAngle):
                currentMinimumAngle = currentPolarAngle
                nextPoint = currentPointToCheck

        # Set the next point the in convex hull
        currentPoint = nextPoint

        # If all the points of the convex hull have been found, break out of the loop
        if currentPoint == lowestPoint:
            break

    # Add the lowest point to the convex hull
    pointsCH.append(lowestPoint)

    return pointsCH


# Helper function to get distance between 2 points
def GetDistance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1 , 2) + math.pow(y2 - y1 , 2))


# Helper function to get dot product between 2 points (vectors)
def GetDotProduct(x1, y1, x2, y2):
    return x1 * x2 +  y1 * y2


# Helper function to find furthest point in a list away from another point
def FindFurthestPoint(points, x, y):

    maxDistance = 0
    for point in points:
        currentDistance = GetDistance(point[0], point[1], x, y)
        if(currentDistance > maxDistance):
            maxDistance = currentDistance
    
    return maxDistance


# Main function
if __name__ == "__main__":

    # Get the question number as the first argument
    try:
        part = int(sys.argv[1])
    except:
        part = 1

    # Set up plot
    #plt.xkcd()
    fig, ax = plt.subplots();
    ax.axis('equal')

    # ==================== UNIFORM VS NORMAL DISTRIBUTION ====================
    
    if(part == 1 or part == 2):    

        # Set axis limits
        ax.axis([-PLOT_SIZE_PART_1_2, PLOT_SIZE_PART_1_2, -PLOT_SIZE_PART_1_2, PLOT_SIZE_PART_1_2])

        # Get the number of iterations to test percent of points in convex hull as the second argument
        try:
            numberOfIterations = int(sys.argv[2])
        except:
            numberOfIterations = 1

        for numPoints in range(NUM_POINTS_MIN_PART_1_2, NUM_POINTS_MAX_PART_1_2 + NUM_POINTS_STEP_PART_1_2, NUM_POINTS_STEP_PART_1_2):

            # Generate test cases to count average number of points in convex hull
            numberOfPointsInCH = 0
            for i in range(0, numberOfIterations):

                # Generate points using uniform distribution
                if(part == 1):
                    points = randomCluster(numPoints, (0, 0), CLUSTER_SIZE, "Uniform")
                # Generate points using normal distribution

                if(part == 2):
                    points = randomCluster(numPoints, (0, 0), CLUSTER_SIZE, "Normal")

                # Calculate the convex hull
                pointsCH = JarvisMarch(points)

                # Subtract 1 since the lowest point is in the convex hull twice (for graphing the line to and from it)
                numberOfPointsInCH += len(pointsCH) - 1
            
            # Calculate average number of points in convex hull
            averagePercentOfPointsInCH = (numberOfPointsInCH / (numPoints * numberOfIterations)) * 100
            #print(f"{numPoints}, {averagePercentOfPointsInCH}")
            print(f"{averagePercentOfPointsInCH}")

        # Split the list of tuples into lists of X and Y coordinates
        x, y = zip(*points)
        xCH, yCH = zip(*pointsCH)

        # Set the color
        if(part == 1):
            color = 'red'
            title = "Point Cluster with Uniform Distribution"
        
        if(part == 2):
            color = 'blue'
            title = " Point Cluster with Normal Distribution"

        # Plot the points and the convex hull
        plt.scatter(x, y, c = color, marker = 'o', edgecolors = 'black')
        plt.plot(xCH, yCH, '-.', c = color)

        plt.title(title)
        plt.show()

    # ==================== INTERSECTION CHECKING USING CONTAINING CIRCLES / POLYGON COLLISION ====================

    if(part == 3 or part == 4):

        # Set axis limits
        ax.axis([-PLOT_SIZE_PART_3_4, PLOT_SIZE_PART_3_4, -PLOT_SIZE_PART_3_4, PLOT_SIZE_PART_3_4])

        # Get the coordinates where to generate the second point cluster as the second and third arguments
        try:
            secondClusterCenterX = int(sys.argv[2])
            secondClusterCenterY = int(sys.argv[3])
        except:
            secondClusterCenterX = 0
            secondClusterCenterY = 0

        # Generate points using uniform distribution
        pointsU = randomCluster(NUM_POINTS_PART_3_4, (0, 0), CLUSTER_SIZE, "Uniform")

        # Generate points using normal distribution
        pointsN = randomCluster(NUM_POINTS_PART_3_4, (secondClusterCenterX, secondClusterCenterY), CLUSTER_SIZE, "Normal")

        # Calculate the convex hulls
        pointsUCH = JarvisMarch(pointsU)
        pointsNCH = JarvisMarch(pointsN)

        # Split the lists of tuples into lists of X and Y coordinates
        xU, yU = zip(*pointsU)
        xUCH, yUCH = zip(*pointsUCH)
        xN, yN = zip(*pointsN)
        xNCH, yNCH = zip(*pointsNCH)

        # Calculate the circles containing each convex hull
        averageUX = sum(xU) / len(xU)
        averageUY = sum(yU) / len(yU)
        averageNX = sum(xN) / len(xN)
        averageNY = sum(yN) / len(yN)

        # Calculate radius of circle containing the clusters
        radiusU = FindFurthestPoint(pointsU, averageUX, averageUY)
        radiusN = FindFurthestPoint(pointsN, averageNX, averageNY)

        #print(f"Average U: ({averageUX}, {averageUY}), R: {radiusU}")
        #print(f"Average N: ({averageNX}, {averageNY}), R: {radiusN}")

        # Use circle approximation
        if(part == 3):

            # Determine if containing circles overlap
            if(GetDistance(averageUX, averageUY, averageNX, averageNY) > radiusU + radiusN):
                title = "Non-overlapping clusters"
            else:
                title = "Overlapping clusters"

        # Use convex hull intersection
        if(part == 4):

            # Assume intersection
            title = "Intersection"

            # Check for intersection using all edges in first convex hull
            numberOfPointsUCH = len(pointsUCH)
            numberOfPointsNCH = len(pointsNCH)

            # Check for both convex hulls
            for currentHull in range(0, 2):
                
                # Determine the current number of points in the current convex hull
                numberOfPointsInCH = numberOfPointsUCH if currentHull == 0 else numberOfPointsNCH

                for pointCHIndex in range(0, numberOfPointsInCH):

                    # Get the points of the current line segment
                    if(currentHull == 0):
                        currentPointA = pointsUCH[pointCHIndex]
                        currentPointB = pointsUCH[(pointCHIndex + 1) % numberOfPointsInCH]
                    if(currentHull == 1):
                        currentPointA = pointsNCH[pointCHIndex]
                        currentPointB = pointsNCH[(pointCHIndex + 1) % numberOfPointsInCH]
                        
                    # Construct a parallel line segment
                    parallelLineXs = (currentPointA[0], currentPointB[0])
                    parallelLineYs = (currentPointA[1], currentPointB[1])

                    # Get the distance of the line segment
                    lineLength = GetDistance(parallelLineXs[0], parallelLineYs[0], parallelLineXs[1], parallelLineYs[1])
                
                    # If the line is of zero length, skip this line segment
                    if(lineLength == 0):
                        continue

                    # Construct the perpendicular line, starting at the current point in the convex hull and pointing outwards from the hull
                    # Done by: perpendicular line = (-y, x) of parallel line where x and y are the displacement between tha starting and ending points of the parallel line
                    # Displacement is divided by the negative line length to normalize it and make it point outwards from the hull
                    perpendicularLineXs = [parallelLineXs[0], -((parallelLineYs[1] - parallelLineYs[0]) / -lineLength) + parallelLineXs[0]]
                    perpendicularLineYs = [parallelLineYs[0], ((parallelLineXs[1] - parallelLineXs[0]) / -lineLength) + parallelLineYs[0]]

                    # Plot the current perpendicular line as a black dotted line
                    plt.plot(perpendicularLineXs, perpendicularLineYs, '--o', c = 'black')

                    # Project point for both convex hulls
                    for currentHull2 in range(0, 2):
                    
                        # Determine the current number of points in the current convex hull
                        numberOfPointsInCH2 = numberOfPointsUCH if currentHull2 == 0 else numberOfPointsNCH

                        # Project the all the points in the current convex hull onto the perpendicular line
                        minProjectedLength = 999999
                        maxProjectedLength = -999999
                        for pointCHIndex in range(0, numberOfPointsInCH2):
                            
                            # Get the displacement of the perpendicular line and the current point in the current convex hull
                            xDisplacementLine = perpendicularLineXs[1] - perpendicularLineXs[0]
                            yDisplacementLine = perpendicularLineYs[1] - perpendicularLineYs[0]

                            if(currentHull2 == 0):
                                xDisplacementPoint = pointsUCH[pointCHIndex][0]
                                yDisplacementPoint = pointsUCH[pointCHIndex][1]
                            if(currentHull2 == 1):
                                xDisplacementPoint = pointsNCH[pointCHIndex][0]
                                yDisplacementPoint = pointsNCH[pointCHIndex][1]

                            # Get the projected length by using the dot product
                            projectedLength = GetDotProduct(xDisplacementLine, yDisplacementLine, xDisplacementPoint, yDisplacementPoint)

                            # Record the maximum and minimum of the current projection to find the bounds of the projected area
                            minProjectedLength = min(projectedLength, minProjectedLength)
                            maxProjectedLength = max(projectedLength, maxProjectedLength)

                        
                        if(currentHull2 == 0):
                            minProjectedLengthU = minProjectedLength
                            maxProjectedLengthU = maxProjectedLength
                        if(currentHull2 == 1):
                            minProjectedLengthN = minProjectedLength
                            maxProjectedLengthN = maxProjectedLength

                    # If the polygons do not overlap, either:
                    # The minimum value for polygon A is bigger than the maximum value for polygon B, or
                    # The maximum value for A is smaller than the minimum value for B
                    if(minProjectedLengthU > maxProjectedLengthN or maxProjectedLengthU < minProjectedLengthN):
                        title = "No intersection"
                        break

                # If a dividing line was found, stop looking for more possible dividing lines
                if(title == "No intersection"):
                    break

        # Plot the points
        plt.scatter(xU, yU, c = 'red', marker = 'o', edgecolors = 'black')
        plt.scatter(xN, yN, c = 'blue', marker = 'o', edgecolors = 'black')

        # Plot the convex hulls
        plt.plot(xUCH, yUCH, '-.', c = 'red')
        plt.plot(xNCH, yNCH, '-.', c = 'blue')

        # Plot the circles containing the convex hulls
        #if(part == 3):
        circleU = plt.Circle((averageUX, averageUY), radiusU, color = 'red', alpha = 0.25)
        circleN = plt.Circle((averageNX, averageNY), radiusN, color = 'blue', alpha = 0.25)
        plt.gca().add_artist(circleU)
        plt.gca().add_artist(circleN)
        
        # Show the plot with the current title
        plt.title(title)
        plt.show()
