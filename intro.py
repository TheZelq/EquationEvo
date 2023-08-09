import random

count = 1

# Variables
tableNumbers = []
operations = ["+", "-", "*"]
tableSigns = []
eqLength = 2
answerText = ""
difficultyLevel = 1
countMultiple = 0

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
        if difficultyLevel == 1:  # No Multiplication on levels 1 - 3
            temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 2:  # Maximum 1 Multiplication on levels 4 - 6
            if countMultiple < 1:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 3:  # Maximum 2 Multiplications on levels 7 - 10
            if countMultiple < 2:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        else:  # Maximum 3 Multiplications on levels 10+
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

    # Taking User's Input
    print("Answer this question:")
    answerNum = int(input(answerText))

    # Calculating a Solution
    solution = eval(answerText)

    # Comparing the Solution with user's Input
    if solution == answerNum:
        print("Good answer! \n")
        count += 1
        print("Level " + str(count) + ":")
        tableNumbers = []
        tableSigns = []
        answerText = ""
        solution = 0
        countMultiple = 0
        if count % 2 == 1:
            eqLength += 1
        if count % 3 == 1 and count <= 10:
            difficultyLevel += 1

    # Finishing the game by wrong user input
    else:
        print("No, that's wrong! The answer was: " + str(solution))
        count = 0
