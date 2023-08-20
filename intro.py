import random
import time

count = 1

# Variables
tableNumbers = []
operations = ["+", "-", "*"]
tableSigns = []
answerText = ""

# Level Defining Variables
eqLength = 2
difficultyLevel = 1
countMultiple = 0
TimeLimit = 5
cleared_levels = []
failed_attempt = None
highest_cleared_level = 0

print("Level 1:")
while count != 0:
    # Generating Numbers
    for element in range(eqLength):
        if difficultyLevel == 1:  # Numbers used on this level (1 - 10)
            tableNumbers.append(random.randint(1, 10))
        elif difficultyLevel == 2:  # Numbers used on this level (-5 - 10)
            tableNumbers.append((random.randint(1, 16) - 6))
        elif difficultyLevel == 3:  # Numbers used on this level (-10 - 20)
            tableNumbers.append((random.randint(1, 31) - 11))
        else:  # Numbers used on this level (-20 - 30)
            tableNumbers.append((random.randint(1, 51) - 21))

    # Generating Signs
    for element in range(eqLength - 1):
        if difficultyLevel == 1:  # No Multiplication on levels 1 - 4
            temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 2:  # Maximum 1 Multiplication on levels 5 - 8
            if countMultiple < 1:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 3:  # Maximum 2 Multiplications on levels 9 - 12
            if countMultiple < 2:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        else:  # Maximum 3 Multiplications on levels 13+
            if countMultiple < 3:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])

    # Creating an Equation Display
    for element in range(eqLength):
        answerText += str(tableNumbers[element]) + " "
        if element < eqLength - 1:
            answerText += str(tableSigns[element]) + " "

    # Setting the Start Time of the Game
    start_time = time.time()

    # Taking User's Input
    print("Answer this question: | " + str(TimeLimit) + "s")
    answerNum = int(input(answerText))

    # Calculating a Solution
    solution = eval(answerText)

    # Calculating the elapsed time
    elapsed_time = time.time() - start_time

    # Comparing the Solution with user's Input
    if solution == answerNum and elapsed_time <= 5:
        print("Correct! You answered in: {:.2f}s".format(elapsed_time) + "\n")
        cleared_levels.append(count)
        highest_cleared_level = max(cleared_levels)  # Update the highest cleared level
        count += 1
        print("Level " + str(count) + ":")
        tableNumbers = []
        tableSigns = []
        answerText = ""
        solution = 0
        countMultiple = 0
        if count % 2 == 1:  # Every Two levels add one number to equations
            eqLength += 1
        if count % 4 == 1 and count <= 13:  # Every Four Levels, Increase the difficulty
            difficultyLevel += 1

    # Finishing the game by elapsed time
    elif elapsed_time > 5:
        print("Time's up! The answer was: " + str(solution) + ". \nYou answered in: {:.2f}s".format(elapsed_time))
        failed_attempt = "Level {} - Correct Answer, answered in {:.2f}s".format(count, elapsed_time)
        count = 0

    # Finishing the game
    else:
        print("Incorrect! The answer was: " + str(solution) + ". \nYou answered in: {:.2f}s".format(elapsed_time))
        failed_attempt = "Level {} - Incorrect Answer".format(count)
        count = 0

# Display summary
if highest_cleared_level > 0:
    print("\nSummary of Attempt:")
    print("Highest Level Cleared: Level", highest_cleared_level)
if failed_attempt:
    print(failed_attempt)
