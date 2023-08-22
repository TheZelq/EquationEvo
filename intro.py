import random
import time
import asyncio


def get_max_multiplications(difficulty_level):
    max_multiplications_level = [0, 1, 2, 3]
    return max_multiplications_level[min(difficulty_level - 1, 3)]


def convert(user_response_content):
    user_response_content = user_response_content.strip()
    user_response_content = user_response_content.replace("-", "", 1)
    return user_response_content


async def delvegame(ctx, bot):
    count = 1

    # Mathematical Variables
    operations = ["+", "-", "*"]
    solution = ""

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
    answerText = ""

    while count != 0:
        # Generating Numbers and Signs
        tableNumbers = []
        tableSigns = []

        for element in range(eqLength):
            lower_limit = (difficultyLevel - 1) * -5
            upper_limit = (difficultyLevel * 5) + 5
            tableNumbers.append(random.randint(lower_limit, upper_limit))

            if element < eqLength - 1:
                if countMultiple < get_max_multiplications(difficultyLevel):
                    temp = random.randint(0, 2)
                    if temp == 2:
                        countMultiple += 1
                else:
                    temp = random.randint(0, 1)
                tableSigns.append(operations[temp])

        # Construct the equation string
        # Construct the equation string
        answer_parts = []
        index = 0
        for num, sign in zip(tableNumbers, tableSigns):
            if num < 0 and index != 0:
                answer_parts.append(f"({num}) {sign}")
            else:
                answer_parts.append(f"{num} {sign}")
            index += 1
        answer_parts.append(f"({tableNumbers[-1]})" if tableNumbers[-1] < 0 else str(tableNumbers[-1]))

        answerText = " ".join(answer_parts)

        # Set the start time of the game
        start_time = time.time()

        # Display the equation to the user
        await ctx.send(f"Level {count}:\n{answerText}")

        try:
            user_response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=TimeLimit)

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time

            converted = convert(user_response.content)

            if str(converted).isnumeric():
                answerNum = int(user_response.content)

                # Check user's answer and time
                if answerNum == eval(answerText) and elapsed_time <= 5:
                    game_output = "Correct! You answered in: {:.2f}s\n".format(elapsed_time)
                    cleared_levels.append(count)
                    highest_cleared_level = max(cleared_levels)

                    # Updating the fastest time if the current time is faster
                    if elapsed_time < fastest_time:
                        fastest_time = elapsed_time
                        fastest_stage = count

                    count += 1
                    if count % 2 == 1:
                        eqLength += 1
                    if count % 4 == 1:
                        difficultyLevel += 1

                else:
                    game_output = "Incorrect! The answer was: " + str(
                        eval(answerText)) + ". \nYou answered in: {:.2f}s\n".format(elapsed_time)
                    failed_attempt = "Level {} - Incorrect Answer".format(count)
                    count = 0

            else:
                game_output = "Invalid input!"
                failed_attempt = "Level {} - Invalid Answer".format(count)
                count = 0

        except asyncio.TimeoutError:
            game_output = "Time's up! The answer was: " + str(eval(answerText)) + ".\n"
            failed_attempt = "Level {} - Time's up".format(count)
            count = 0

    # Display summary
    output_parts = []
    if highest_cleared_level > 0:
        output_parts.append("Highest Level Cleared: Level {}".format(highest_cleared_level))
    if fastest_time != float('inf'):
        output_parts.append("Fastest Answer in Attempt: {:.2f}s in Stage {}".format(fastest_time, fastest_stage))
    if failed_attempt:
        output_parts.append(failed_attempt)

    # Join the output parts and return the game output as a string
    if game_output:
        output_parts.append(game_output)

    game_output = "\n".join(output_parts)
    return game_output
