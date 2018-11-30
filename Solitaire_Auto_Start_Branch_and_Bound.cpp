// CMPE 356 - Solitaire Auto Start Project
// Branch & Bound Algorithm

// ==================== LIBRARY INCLUDES ====================

#include <stdio.h>      // For the standard stuff
#include <iostream>     // For printing
#include <iomanip>      // For setting output # of decimal places
#include <algorithm>    // For suffling cards
#include <string>       // For names of card values and suits
#include <random>       // For suffling cards
#include <ctime>        // For random seed
#include <time.h>       // For timing of elapsed time

// ==================== SETUP ====================

using namespace std;    // For not having to write "std::" 100's of times

// ==================== CONSTANTS ====================

// If this is defined (uncommented), the individual results are not printed out, instead the average amound of iterations for this amount of tests is
// Otherwise, if this is commented, the individual results not printed out
//#define REPEATED_TESTS     100

int debugPrintLevel = 0;
// Set to > 0 to see debugging info (this will have a very significant negative impact on speed!)
// Level 0: no debug prints
// Level 1: Print each card as it is auto placed, plus basic info
// Level 2: Also print the cards initialy in each card stack
// Level 3: Also print the cards in the suffled deck(s)
// Level 4: Also print the card wanted by each ace pile after each card is auto placed
// Level 5: Also print the card stack movement array in each pass of the algorithm

// Print the status every 1000 iterations, as well as the best case so far, even if debugPrintLevel = 0
const bool printProgress = true;

// Used to determine if an ace pile is full
#define KING_VALUE 12

// Used for debug printing only
string valueNames[] = {"Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"};
//                       0     1    2    3    4    5    6    7    8    9      10       11      12
string suitNames[] = {"Spades", "Clubs", "Hearts", "Diamonds"};
//                      100       200       300        400

// Card format: simple integer
// Hundreds is suit     (100, 200, 300, 400)
// Ones & Test is value (0-12)
// Ex: (100) is Ace of Spades, (304) is 5 of Hearts (as defined in name arrays above)

// ==================== DATA ====================

// The configuration for the game
const int numDecks = 2;
const int numAcePiles = 8;
const int numCardStacks = 10;
const int cardStackSize = 4;

// This is changed with the first command line argument
const unsigned int targetNumberOfAutoPlacements = 15;

// ==================== HELPER FUNCTIONS ====================

// Print the human-readible name of a card (e.g. Ace of Spades)
void printCard(int cardToPrint, bool addNewline = true) {
    
    int suit = (cardToPrint / 100) - 1;
    int value = cardToPrint - (suit + 1) * 100;
    
    if(suit < 0 || suit > 3 || value < 0 || value > 12) {
        cout << "Invalid card! (Suit: " << suit << ", Value: " << value << ")";
    }
    
    else {
        cout << valueNames[value] << " of " << suitNames[suit];
    }
    
    if(addNewline) {
        cout << endl;
    }
    
}

// Print all the cards in a card stack, from top to bottom
void printCardStack(int cardStackToPrint[], int cardStackIndex) {
    
    cout << "--- Card stack #" << cardStackIndex << " ---" << endl;
    
    if(cardStackToPrint[0] == 0) {
        cout << "Empty" << endl;
    }
    
    else {
    
        for(int cardIndex = cardStackToPrint[0]; cardIndex > 0; cardIndex--) {
            // Print the card at the current index, starting from the top        
            printCard(cardStackToPrint[cardIndex]);
        }
    
    }
    
}

// Determine if an ace pile can have more cards placed onto it (i.e. not full yet)
bool acePileIsFull(int currentWantedCard) {
    
    int suit = (currentWantedCard / 100) - 1;
    int value = currentWantedCard - (suit + 1) * 100;
    
    // If the wanted card's value is more than a king, the ace pile is full
    return (value > KING_VALUE);
    
}

// Compare the first elements in the array (number of possible movements) (Bit of a hack way to do it, but it works and its fast)
int compareCardStackMovement(const void *ap, const void *bp) {
    
    // Get number of potential moves
    int *numMovesA = (int *)ap;
    int *numMovesB = (int *)bp;
    
    // If number of moves differ, sort by number of moves (higher is better)
    if(*numMovesB - *numMovesA != 0) {
        return *numMovesB - *numMovesA;
    } 
    
    // Otherwise, sort by card to move value (lower is better)
    else {
        
        // Get number of potential moves
        int *valueA = (int *)(ap + 2);
        int *valueB = (int *)(bp + 2);
    
        return *valueB - *valueA;
    
    }
}

// ==================== CARD MOVEMENT CALCULATION FUNCTION ====================

int calculateCardMovement(int currentAcePiles[], int currentCardStack[], int cardStackIndex, int *acePileToPlaceCardTo, int *cardValueToMove) {
    
    // The list of ace pile indicies to move the cards in the current stack to
    int numberOfMovableCards = 0;
    
    //cout << "Calculating card movement..." << endl;
    //printCardStack(currentCardStack, cardStackIndex);
    
    // Base case: there are no cards in the current card stack
    if(currentCardStack[0] == 0) {
        // No cards can be placed on no ace piles
        *acePileToPlaceCardTo = 0;
        *cardValueToMove = 0;
        return 0;
    } 
    // Recursive case: there are still cards in the current card stack
    else {
        
        // Can the current top card be placed onto any ace pile?
        bool topCardCanBeAutoPlaced = false;
        
        // Loop through all the ace piles
        for(int acePileIndex = 0; acePileIndex < numAcePiles; acePileIndex++) {
            
            // If the current ace pile is still not full (Ace to King not placed yet)
            if(!acePileIsFull(currentAcePiles[acePileIndex])) {
                
                // Check if the current ace pile wants the current top card
                if(currentAcePiles[acePileIndex] == currentCardStack[currentCardStack[0]]) {

                    //cout << "Can place ";
                    //printCard(currentCardStack[currentCardStack[0]], false); // Print with no newline
                    //cout << "(" << currentCardStack[currentCardStack[0]] << ") from stack #" << cardStackIndex << " to ace pile #" << acePileIndex << endl;

                    // If it does, a card can be moved to the current ace pile
                    numberOfMovableCards += 1;

                    // Record which ace pile the card can be placed on and the value of that card;
                    *acePileToPlaceCardTo = acePileIndex;
                    *cardValueToMove = currentCardStack[currentCardStack[0]] - ((currentCardStack[currentCardStack[0]] / 100) * 100);
                    
                    //cout << "Can place (" << *cardValueToMove << ")" << endl;
                    
                    // Simulate moving the card
                    currentCardStack[0]--;              // Pop the top card of the current card stack
                    currentAcePiles[acePileIndex]++;    // Place it on the current ace pile

                    // Indicate that a card was moved
                    topCardCanBeAutoPlaced = true;

                    // Stop current card placing simulation and re-simulate with the top card of the current stack removed
                    break;
                    
                }
                
            }
            
        }
        
        // If the current top card was placed, check if the next card can be placed
        if(topCardCanBeAutoPlaced) {
            // Get the number of cards that can be placed after the top card is placed (the ace piles that can be additionally placed onto are not used)
            int dummyInt1, dummyInt2;
            numberOfMovableCards += calculateCardMovement(currentAcePiles, currentCardStack, cardStackIndex, &dummyInt1, &dummyInt2);
        }
        
    }
    
    return numberOfMovableCards;
    
}

int solitaireAutoStart(int acePiles[], int cardStacks[][cardStackSize + 1], int level) {
    
    // The number of cards which were auto-placed
    unsigned int numAutoPlacedCards = 0;

    // Flag used to indicate if some top card can be moved or not, used to prevent sorting if no top cards can be moved anymore
    bool movableCardExists = false;
    
    // The list of card stack indicies, number of movable cards, and ace pile indicies to move the cards to for each of the card stacks to
    // Format is:
    // [0] - Number of possible movements if the top card is placed (0 by default)
    // [1] - Which ace pile to place to top card on (-1 by default)
    // [2] - Card stack index, required since this array will be sorted and need to keep track of which card stack is which
    // [3] - Value of the top card that can be placed
    int cardMovementArray[numCardStacks][4];
    
    // Loop through all the card stacks
    for(int currentCardStackIndex = 0; currentCardStackIndex < numCardStacks; currentCardStackIndex++) {
        
        // Make a copy of the ace piles
        int currentAcePiles[numAcePiles];
        copy(acePiles, (acePiles + numAcePiles), currentAcePiles);
        
        // Make a copy of the card stacks
        int currentCardStack[cardStackSize + 1];
        for(int i = 0; i <= cardStackSize; i++) {
            currentCardStack[i] =  cardStacks[currentCardStackIndex][i];
        }
        
        // Calculate how many cards can be moved in this card stack and which ace pile to place to top card on (lists passed by value since they are not to be changed by this "simulation of movement")
        cardMovementArray[currentCardStackIndex][3] = 0;
        cardMovementArray[currentCardStackIndex][1] = -1;
        cardMovementArray[currentCardStackIndex][2] = currentCardStackIndex;
        cardMovementArray[currentCardStackIndex][0] = calculateCardMovement(currentAcePiles, currentCardStack, currentCardStackIndex, &cardMovementArray[currentCardStackIndex][1], &cardMovementArray[currentCardStackIndex][3]);
        
        // If at least one card can be moved, set the flag so the auto card placement happens
        if(cardMovementArray[currentCardStackIndex][0] > 0) {
            movableCardExists = true;
        }
        
    }
    
    // Print out the movement array:
    //for(int currentCardStackIndex = 0; currentCardStackIndex < numCardStacks; currentCardStackIndex++) {
    //    cout << "Stack #" << cardMovementArray[currentCardStackIndex][2] << ", possible moves: " << cardMovementArray[currentCardStackIndex][0] << ", ace pile to move top card to: " << cardMovementArray[currentCardStackIndex][1] << ", value of card to move: " << cardMovementArray[currentCardStackIndex][3] << endl;
    //}
    
    // If no more cards can be moved, end current iteration
    if(!movableCardExists) {
        return 0;
    }
    
    // Sort the card movement array by number of potential card movements
    qsort(cardMovementArray, numCardStacks, 4 * sizeof(int), compareCardStackMovement);
    
    // Print out the sorted card movement array:
    if(debugPrintLevel >= 5) {
        for(int currentCardStackIndex = 0; currentCardStackIndex < numCardStacks; currentCardStackIndex++) {
            for(int t = 0; t < level; t++) {
                cout << "\t";
            }
            cout << "Stack #" << cardMovementArray[currentCardStackIndex][2] << ", possible moves: " << cardMovementArray[currentCardStackIndex][0] << ", ace pile to move top card to: " << cardMovementArray[currentCardStackIndex][1] << ", value of card to move: " << cardMovementArray[currentCardStackIndex][3] << endl;
        }
    }
    
    // The card stack index to move and the ace pile index to move its top card to
    // Required for debug printing only
    int bestCardStackIndex;
    int acePileToMoveToIndex;

    // The data for each sub-branch
    vector<int> equalMovementPotentialCardStackIndexes;
    vector<int> equalMovementPotentialAcePileIndexes;
    vector<int> equalMovementPotentialNumberOfPossiblePlacements;
    
    int maxMovementAmount = cardMovementArray[0][0];
    for(int currentCardStackIndex = 0; currentCardStackIndex < numCardStacks; currentCardStackIndex++) {
        if(cardMovementArray[currentCardStackIndex][0] == maxMovementAmount) {
            equalMovementPotentialCardStackIndexes.push_back(cardMovementArray[currentCardStackIndex][2]);
            equalMovementPotentialAcePileIndexes.push_back(cardMovementArray[currentCardStackIndex][1]);
        }
    }
    
    int maxAdditionalMovementAmount = -1;
    int indexOfEqualMovementPotential = 0;
    for(int currentCardStackIndex : equalMovementPotentialCardStackIndexes) {
        
    
        // Make a copy of the ace piles
        int currentAcePiles[numAcePiles];
        copy(acePiles, (acePiles + numAcePiles), currentAcePiles);
        
        // Make a copy of the card stacks
        int currentCardStacks[numCardStacks][cardStackSize + 1];
        for(int i = 0; i < numCardStacks; i++) {
            for(int j = 0; j <= cardStackSize; j++) {
                currentCardStacks[i][j] =  cardStacks[i][j];
            }
        }
    
        currentCardStacks[currentCardStackIndex][0]--;                                                   // Pop the top card of the current card stack
        currentAcePiles[equalMovementPotentialAcePileIndexes[indexOfEqualMovementPotential]]++;          // Place it on the current ace pile
        
        // Recurse down the sub-branches
        int additionalMovementAmount = solitaireAutoStart(currentAcePiles, currentCardStacks, level + 1);
        equalMovementPotentialNumberOfPossiblePlacements.push_back(additionalMovementAmount);
        
        // Required for debug printing only
        if(additionalMovementAmount > maxAdditionalMovementAmount) {
            maxAdditionalMovementAmount = additionalMovementAmount;
            bestCardStackIndex = currentCardStackIndex;
        }
        
        indexOfEqualMovementPotential++;
        
    }
    
    // Find the greatest number of possible aout placements in each sub-branch
    numAutoPlacedCards = *max_element(begin(equalMovementPotentialNumberOfPossiblePlacements), end(equalMovementPotentialNumberOfPossiblePlacements)) + 1;
    
    // Required for debug printing only
    for(int currentCardStackIndex = 0; currentCardStackIndex < numCardStacks; currentCardStackIndex++) {
        if(cardMovementArray[currentCardStackIndex][2] == bestCardStackIndex) {
            acePileToMoveToIndex = cardMovementArray[currentCardStackIndex][1];
        }
    }

    // Print out info about the card that is about to be auto placed
    if(debugPrintLevel >= 1) {            
        for(int t = 0; t < level; t++) {
            cout << "\t";
        }
        cout << "Auto placed ";
        printCard(cardStacks[bestCardStackIndex][cardStacks[bestCardStackIndex][0]], false); // Print with no newline
        cout << " from stack #" << bestCardStackIndex << " to ace pile #" << acePileToMoveToIndex << endl;
    }
        
    // Return the number of cards that can currently be placed
    return numAutoPlacedCards;
    
}

// ==================== MAIN ====================

int main(int argc, char **argv) {
    
    // ==================== DATA ====================

    // Contains cards in all decks
    int decks[numDecks * 52];

    // Contains the multiple cards in each card stack (first element is "stack pointer" to the index of the current top card, which is also the number of cards currently in the stack)
    int cardStacks[numCardStacks][cardStackSize + 1];

    // Contains the wanted card for each ace pile
    int acePiles[numAcePiles];
    
    // Keep track of how many iterations it took to reach the target number of auto placed cards
    unsigned int numIterations = 0;
    
#ifdef REPEATED_TESTS
    // The total iterations, used if the repeated test mode is used
    unsigned int totalNumIterations = 0;
#endif

    // The number of cards which were auto-placed
    unsigned int numAutoPlacedCards = 0;
    
    // Keep track of the maximum number of auto placed cards so far
    unsigned int maxAutoPlacedCards = 0;
    
    // Keep track of how many times X number of cards were auto placed
    vector<unsigned int> autoPlacedCardsHistogram;
    
    // Times when algorithm was started and finished, used to calculate run time
    double startTime, finishTime;
    
    // ==================== INITIALIZE ====================
    
    // Set the random seed to be different each time
    srand(time(NULL));
    
    // Record time when algorithm was started
    //startTime = clock();
    
    // ==================== GENERATE DECK(S) ====================
    
    // Place cards in order into decks (cards array)
    for(int deck = 0; deck < numDecks; deck++) {
        for(int suit = 0; suit < 4; suit++) {
            for(int value = 0; value < 13; value++) {
                decks[deck * 52 + suit * 13 + value] = (suit + 1) * 100 + value;
            }
        }
    }
    
    // Print out the cards in the decks
    //cout << "=========== Decks ===========" << endl;
    //for(int card : decks) {
    //    printCard(card);
    //}
    
#ifdef REPEATED_TESTS
    for(int i = 0; i < REPEATED_TESTS; i++) {
        numIterations = 0;
        maxAutoPlacedCards = 0;
        autoPlacedCardsHistogram.clear();
#endif
    
    // Record time when algorithm was started
    startTime = clock();
    
    // ==================== REPEAT ALGORITHM UNTIL TARGET NUMBER OF CARDS ARE PLACED ====================
    
    while(true) {
        
        // Reset the number of cards which were auto-placed
        numAutoPlacedCards = 0;
        
        // Increment the number of iterations of the auto start algorithm that have been done
        numIterations++;
        
        // Print the current iteration number
        if(debugPrintLevel >= 1) {
            cout << "\n==================== Iteration # " << numIterations << " ====================" << endl;
        }
        
        // ==================== SUFFLE DECK(S) ====================
        
        // Make a copy of the decks and shuffle the copy
        int suffledDecks[numDecks * 52];
        copy(decks, (decks + numDecks * 52), suffledDecks);
        random_shuffle(suffledDecks, (suffledDecks + numDecks * 52));
        
        // Print out the suffled decks
        if(debugPrintLevel >= 3) {
            cout << "=========== Suffled decks ===========" << endl;
            for(int card : suffledDecks) {
                printCard(card);
            }
        }
        
        // ==================== GENERATE CARD STACKS ====================
        
        // Flag to indicate if an ace was placed on top
        bool aceWasPlacedOnTop = false;

        // How many aces were dealt out in total
        int numAcesDealtOut = 0;
        
        // Loop through all card stacks
        for(int cardStackIndex = 0; cardStackIndex < numCardStacks; cardStackIndex++) {
            // Set number of cards currently in card stack to cardStackSize
            cardStacks[cardStackIndex][0] = cardStackSize;
            // Loop through all cards to place
            for(int cardIndex = 0; cardIndex < cardStackSize; cardIndex++) {
                
                // Place card from top of suffled deck into the current card stack            
                cardStacks[cardStackIndex][cardIndex+1] = suffledDecks[cardStackIndex * cardStackSize + cardIndex];
                
                // Determine if an ace was placed
                if(cardStacks[cardStackIndex][cardIndex+1] % 100 == 0) {
                    // If so, add to the total number of aces placed
                    numAcesDealtOut++;
                    // Determine if it was placed on top of a card stack
                    if(cardIndex == cardStackSize - 1) {
                        // If so, set the flag to indicate it
                        aceWasPlacedOnTop = true;
                    }
                }
                
            }
        }
        
        // Print out the cards in each card stack
        if(debugPrintLevel >= 2) {
            cout << "=========== Card Stacks ===========" << endl;
            for(int cardStackIndex = 0; cardStackIndex < numCardStacks; cardStackIndex++) {
                printCardStack(cardStacks[cardStackIndex], cardStackIndex);
            }
        }
        
        // Maximum number of cards that can be auto placed is constrained by the amount of aced dealt out
        // For every ace that is dealt out, at most 13 cards can be placed in an ace pile (Ace to King)
        unsigned int maxPossibleAutoPlacedCards = numAcesDealtOut * 13;

        // It is possible to auto place the target amount of cards if
        bool isPossibleToReachTargetAutoPlacedCards = aceWasPlacedOnTop && maxPossibleAutoPlacedCards >= targetNumberOfAutoPlacements;

        // Only run the algorithm if an ace was placed on top of a card stack (otherwise, can't even start to place cards)
        // And the number of possible auto placements is >= the target number of auto placements
        if(!aceWasPlacedOnTop && debugPrintLevel >= 1) {
            cout << "No ace was placed on top!" << endl;
        }
        if(maxPossibleAutoPlacedCards < targetNumberOfAutoPlacements && debugPrintLevel >= 1) {
            cout << "Not enough aces dealt out (" << numAcesDealtOut << ")" << endl;
        }
        if(isPossibleToReachTargetAutoPlacedCards) {
        
            // ==================== GENERATE ACE PILES ====================
            
            // Create each ace pile
            for(int acePileIndex = 0; acePileIndex < numAcePiles; acePileIndex++) {
                // Set the current ace pile's wanted card to the ace of the current suit (once 4 are created, the suits repeat)
                acePiles[acePileIndex] = ((acePileIndex % 4) + 1) * 100;
            }
            
            // Print out the wanted card of each ace pile
            //cout << "=========== Ace Piles ===========" << endl;
            //for(int card : acePiles) {
            //    printCard(card);
            //}
            
            // ==================== AUTO PLACE ALGORITHM ====================
            
            // Last parameter is to formal debug printing only
            numAutoPlacedCards = solitaireAutoStart(acePiles, cardStacks, 0);
            
        }
        
        // ==================== SAVE RESULTS OF CURRENT ITERATION ====================
        
        // Print out how many cards were auto placed in the current iteration
        if(debugPrintLevel >= 1) {
            cout << "Number of auto placed cards: " << numAutoPlacedCards << endl;
        }
        
        //Keep track of the maximum number of auto placed cards so far
        maxAutoPlacedCards = max(maxAutoPlacedCards, numAutoPlacedCards);
        
        // If this is a new maximum number of cards auto placed, allocate space to store the number of times it happened in the histogram vector
        if(autoPlacedCardsHistogram.size() < maxAutoPlacedCards + 1) {
            autoPlacedCardsHistogram.resize(maxAutoPlacedCards + 1, 0);
        }
        
        // Increment the number of times this many cards were auto placed
        autoPlacedCardsHistogram[numAutoPlacedCards]++;
        
        // ==================== PRINT PROGRESS ====================
        
        // Print out the number of iterations at 1000 iteration intervals
        if(printProgress && numIterations % 1000 == 0) {
            cout << "\rStatus (1000's of iterations | best case): " << (numIterations/1000) << " | (" << maxAutoPlacedCards << " , " << autoPlacedCardsHistogram[maxAutoPlacedCards] << ")";
        }
        
        // ==================== CHECK TO MOVE TO NEXT ITERATION ====================
        
        // It number of auto placed cards reache reached or exceeded the target number of cards to auto place, stop iterating and print results
        if(numAutoPlacedCards >= targetNumberOfAutoPlacements) {
            break;
        }
        
    }
    
    // ==================== PRINT OUT RESULTS WHEN TARGET IS REACHED ====================
    
    // Record time when algorithm is finished
    finishTime = clock();
    
    // Calculate runtime in ms
    double runTime = (finishTime - startTime);
    
    // Print out the number of iterations, time it took, target number of cards to auto place, actual number of auto placed cards, and ms/iteration
    cout << fixed;
    cout << setprecision(3);
#ifdef REPEATED_TESTS
    cout << "It took " << numIterations << " iterations (" << (runTime / 1000) << "s) to auto place at least " << targetNumberOfAutoPlacements << " cards (" << numAutoPlacedCards << " cards were placed, " << (runTime / numIterations) << " ms/iteration)" << endl;
#else
    cout << "\n-------------------------------------------------------------------------------------------------------------" << endl;
    cout << "It took " << numIterations << " iterations (" << (runTime / 1000) << "s) to auto place at least " << targetNumberOfAutoPlacements << " cards (" << numAutoPlacedCards << " cards were placed, " << (runTime / numIterations) << " ms/iteration)" << endl;
    cout << "-------------------------------------------------------------------------------------------------------------\n" << endl;
    cout << "The resulting histogram (number of occurrences in order of number of cards placed) is:" << endl;
    
    // Print out how many times X many cards were placed, starting with 0 to maxAutoPlacedCards (it may be more than the target number of cards to auto place)
    for(int currentNumberOfAutoPlacedCards : autoPlacedCardsHistogram) {
        cout << currentNumberOfAutoPlacedCards << endl;
    }
#endif
    
#ifdef REPEATED_TESTS
        totalNumIterations += numIterations;

    }
    
    cout << "\n-------------------------------------------------------------------------------------------------------------" << endl;
    cout << "Average # of iterations: " << (totalNumIterations / REPEATED_TESTS) << endl;
#endif
    
    // ==================== END ====================
    
    cout << "\nPress enter key to exit..." << endl;
    cin.get();
    
	return 0;
}