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


async def delve_game(ctx, bot):
    count = 1

    # Mathematical Variables
    operations = ["+", "-", "*"]

    # Level Defining Variables
    eq_length = 2
    difficulty_level = 1
    timelimit = 5
    cleared_levels = []
    failed_attempt = None
    highest_cleared_level = 0
    fastest_time = float('inf')
    fastest_stage = None
    game_output = ""

    while count != 0:
        # Generating Numbers and Signs
        table_numbers = []
        table_signs = []
        count_multiple = 0
        counter = 0

        for element in range(eq_length):
            lower_limit = (difficulty_level - 1) * -5
            upper_limit = (difficulty_level * 5) + 5
            table_numbers.append(random.randint(lower_limit, upper_limit))

            if element < eq_length - 1:
                if count_multiple < get_max_multiplications(difficulty_level) and all(
                        num <= upper_limit - 5 for num in table_numbers):
                    eligible_numbers = [num for num in table_numbers if num <= upper_limit - 5]
                    if len(eligible_numbers) >= 2:  # Check for multiplication eligibility
                        temp = random.randint(0, 2)
                        if temp == 2:
                            count_multiple += 1
                    else:
                        temp = random.randint(0, 1)  # Use addition or subtraction instead of multiplication
                else:
                    temp = random.randint(0, 1)
                table_signs.append(operations[temp])

        # Construct the equation string
        answer_parts = []
        index = 0
        for num, sign in zip(table_numbers, table_signs):
            if num < 0 and index != 0:
                answer_parts.append(f"({num}) {sign}")
            else:
                answer_parts.append(f"{num} {sign}")
            index += 1
        answer_parts.append(f"({table_numbers[-1]})" if table_numbers[-1] < 0 else str(table_numbers[-1]))

        answer_text = " ".join(answer_parts)

        # Set the start time of the game
        start_time = time.time()

        # Display the equation to the user
        await ctx.send(f"Level {count}: | {timelimit}s | {ctx.author.mention}\n``{answer_text}``")

        try:
            user_response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=timelimit)

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time

            converted = convert(user_response.content)

            if str(converted).isnumeric():
                for element in range(0, len(str(user_response.content))):
                    if element > 0 and str(user_response.content)[element] == "-":
                        counter += 1
                if counter > 0:
                    game_output = "\nInvalid input! The answer was: " + str(eval(answer_text))
                    failed_attempt = "Level {} - Invalid Answer".format(count)
                    count = 0
                else:
                    answer_num = int(user_response.content)

                    # Check user's answer and time
                    if answer_num == eval(answer_text) and elapsed_time <= timelimit:
                        game_output = "\nCorrect! You answered in: {:.2f}s\n".format(elapsed_time)
                        cleared_levels.append(count)
                        highest_cleared_level = max(cleared_levels)

                        # Updating the fastest time if the current time is faster
                        if elapsed_time < fastest_time:
                            fastest_time = elapsed_time
                            fastest_stage = count

                        count += 1
                        if count % 2 == 1:
                            eq_length += 1
                        if count % 4 == 1:
                            difficulty_level += 1
                            timelimit += 1

                    else:
                        game_output = "\nIncorrect! The answer was: " + str(
                            eval(answer_text)) + ". You answered in: {:.2f}s".format(elapsed_time)
                        failed_attempt = "Level {} - Incorrect Answer".format(count)
                        count = 0

            else:
                game_output = "\nInvalid input! The answer was: " + str(eval(answer_text))
                failed_attempt = "Level {} - Invalid Answer".format(count)
                count = 0

        except asyncio.TimeoutError:
            game_output = "\nTime's up! The answer was: " + str(eval(answer_text)) + ".\n"
            failed_attempt = "Level {} - Out of Time".format(count)
            count = 0

    # Display summary
    output_parts = []
    if highest_cleared_level > 0:
        output_parts.append("Summary of the Attempt:\n")
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
