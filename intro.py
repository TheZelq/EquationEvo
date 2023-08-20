import random
import time

count = 1

# Mathematical Variables
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
fastest_time = float('inf')
fastest_stage = None


def get_max_multiplications(difficulty_level):
    # Defining the maximum amount of allowed multiplications based on difficultyLevel variable
    max_multiplications_level = [0, 1, 2, 3]
    return max_multiplications_level[min(difficulty_level - 1, 3)]


print("Level 1:")
while count != 0:
    # Generating Numbers
    for element in range(eqLength):
        lower_limit = (difficultyLevel - 1) * -5
        upper_limit = (difficultyLevel * 5) + 5
        tableNumbers.append(random.randint(lower_limit, upper_limit))

    # Generating Signs
    while len(tableSigns) < eqLength - 1:
        if countMultiple < get_max_multiplications(difficultyLevel):
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

        # Updating the fastest time if the current time is faster
        if elapsed_time < fastest_time:
            fastest_time = elapsed_time
            fastest_stage = count

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
    elif solution == answerNum and elapsed_time > 5:
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
if fastest_time != float('inf'):
    print("Fastest Answer in Attempt: {:.2f}s in Stage {}".format(fastest_time, fastest_stage))
if failed_attempt:
    print(failed_attempt)
