from connector import connect
from collections import ChainMap


def close(connection, cursor):
    cursor.close()
    connection.close()


def update_profile(discord_id, discord_username, new_highest_stage, new_highest_abs_answer, new_fastest_time,
                   new_equations_answered):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Round fastest_time to two decimal places
        rounded_fastest_time = round(new_fastest_time, 2)

        # Retrieve the current profile from the database
        select_query = "SELECT * FROM profiles WHERE discord_id = %s"
        cursor.execute(select_query, (discord_id,))
        result = cursor.fetchone()

        if result:
            name = result[2]
            equations_answered = result[5]
            current_highest_stage = result[6]
            highest_abs_answer = result[8]
            current_fastest_time = result[7]

            # Updating values if necessary
            update_values = {}
            update_values['equations_answered'] = equations_answered
            if new_highest_stage > int(current_highest_stage):
                update_values['highest_stage'] = new_highest_stage
            if highest_abs_answer is None or new_highest_abs_answer > int(highest_abs_answer):
                update_values['highest_abs_answer'] = new_highest_abs_answer
            if rounded_fastest_time < float(current_fastest_time):
                update_values['fastest_time'] = rounded_fastest_time
            if name != discord_username:
                update_values['name'] = discord_username
            if current_fastest_time == 0:
                update_values['fastest_time'] = rounded_fastest_time

            if update_values:
                update_query = "UPDATE profiles SET "
                update_query += ", ".join([f"{key} = %s" for key in update_values.keys()])
                update_query += ", equations_answered = equations_answered + %s"  # Add equations_answered update
                update_query += " WHERE discord_id = %s"

                cursor.execute(update_query, list(update_values.values()) + [new_equations_answered, discord_id])
                connection.commit()
                print(f"Profile updated for user {discord_id}")

        else:
            # Insert a new profile
            insert_query = ("INSERT INTO profiles (discord_id, name, equations_answered, highest_stage, "
                            "highest_abs_answer, fastest_time) VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (discord_id, discord_username, new_equations_answered, new_highest_stage,
                                          new_highest_abs_answer, rounded_fastest_time))
            connection.commit()
            print(f"New profile inserted for user {discord_id}")

        # Consume the results before closing
        cursor.fetchall()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def get_profile_data(discord_name):
    try:
        connection = connect()
        cursor = connection.cursor()

        select_query = "SELECT * FROM profiles WHERE name = %s"
        cursor.execute(select_query, (discord_name,))
        result = cursor.fetchone()

        if result:
            profile_data = {
                'name': result[2],
                'currency': result[3],
                'achievement_points': result[4],
                'equations_solved': result[5],
                'highest_stage': result[6],
                'rounded_fastest_time': result[7],
                'new_highest_abs_answer': result[8],
            }
            return profile_data
        else:
            return None

    except Exception as e:
        print("Error:", e)


def get_achievements_data(discord_name):
    try:
        connection = connect()
        cursor = connection.cursor()

        select_query = "SELECT user_id FROM profiles WHERE name = %s"
        cursor.execute(select_query, (discord_name,))
        result = cursor.fetchone()

        if result:
            user = str(result[0])
            select_query2 = ("SELECT achievement_name FROM achievements INNER JOIN unlocked_achievements ON "
                             "achievements.achievement_id = unlocked_achievements.achievement_id WHERE "
                             "unlocked_achievements.user_id = %s")
            cursor.execute(select_query2, (user,))
            result2 = cursor.fetchall()
            if result2:
                achievements = ""
                for element in result2:
                    achievements += element[0]
                    achievements += "\n"
                return achievements
            else:
                return "This user doesn't have any achievements."
        else:
            return None

    except Exception as e:
        print("Error:", e)


def get_achievement_desc(achievement_name):
    try:
        connection = connect()
        cursor = connection.cursor()

        select_query = "SELECT achievement_desc FROM achievements WHERE achievement_name = %s"
        cursor.execute(select_query, (achievement_name,))
        result = cursor.fetchone()

        if result:
            desc = result[0]
            return desc
        else:
            return ("There is no achievement under this name. Check if you don't have any spelling error or if you "
                    "put the quotation marks.")

    except Exception as e:
        print("Error:", e)


def leaderboard_data():
    try:
        connection = connect()
        cursor = connection.cursor()

        select_query = "SELECT name, highest_stage from Profiles ORDER BY highest_stage DESC LIMIT 5"
        cursor.execute(select_query)
        result = cursor.fetchall()

        if result:
            leaderboard = {}
            i = 0
            for element in result:
                a = {'name'+str(i): element[0]}
                leaderboard = ChainMap(leaderboard, a)
                a = {'highest'+str(i): element[1]}
                leaderboard = ChainMap(leaderboard, a)
                i += 1
            return leaderboard
        else:
            return None

    except Exception as e:
        print("Error:", e)
