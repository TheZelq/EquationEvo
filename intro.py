import random
count  = 1

#variables
tableNumbers = []
operations = ["+", "-", "*"]
tableSigns = []
eqLength = 2
answerText = ""
difficultyLevel = 1
countMultiple = 0

while(count != 0):
    #generating Numbers
    for element in range(eqLength):
        if difficultyLevel == 1:
            tableNumbers.append(random.randint(1, 10) )
        elif difficultyLevel == 2:
            tableNumbers.append((random.randint(1, 16) - 6))
        elif difficultyLevel == 3:
            tableNumbers.append((random.randint(1, 31) - 11))
        else:
            tableNumbers.append((random.randint(1, 51) - 21))

    #generating Signs
    for element in range(eqLength - 1):
        if difficultyLevel == 1:
            temp =  random.randint(0,1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 2:
            if countMultiple < 1:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        elif difficultyLevel == 3:
            if countMultiple < 2:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])
        else:
            if countMultiple < 3:
                temp = random.randint(0, 2)
                if temp == 2:
                    countMultiple += 1
            else:
                temp = random.randint(0, 1)
            tableSigns.append(operations[temp])

    #creating a Display
    for element in range(eqLength ):
        answerText += str(tableNumbers[element]) + " "
        if element < eqLength - 1:
            answerText += str(tableSigns[element]) + " "

    #taking user's Input
    print("Answer this question:")
    answerNum = int(input(answerText))

    #calculating a Solution
    solution  = eval(answerText)

    #comparing the Solution with user's Input
    if solution == answerNum:
        print("Good job!")
        print("Your current streak is " +str(count))
        count += 1
        tableNumbers = []
        tableSigns = []
        answerText = ""
        solution = 0
        countMultiple = 0
        if count % 2 == 1:
            eqLength += 1
        if count % 3 == 1 and count <= 10:
            difficultyLevel += 1

    else:
        print("No, that's wrong! The answer was: "  + str(solution))
        count = 0