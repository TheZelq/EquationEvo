from pytz import timezone
from connector import connect
from collections import ChainMap
from datetime import datetime, timezone, timedelta


def close(connection, cursor):
    cursor.close()
    connection.close()


def update_profile(discord_id, discord_username, currency_added, new_highest_stage, new_highest_abs_answer,
                   new_fastest_time, new_equations_answered):
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
            currency = result[3]
            equations_answered = result[6]
            current_highest_stage = result[7]
            highest_abs_answer = result[11]
            current_fastest_time = result[10]

            # Updating values if necessary
            update_values = {}
            update_values['EQ_Ans'] = equations_answered
            update_values['FreeC'] = currency
            if new_highest_stage > int(current_highest_stage):
                update_values['Free_High'] = new_highest_stage
            if highest_abs_answer is None or new_highest_abs_answer > int(highest_abs_answer):
                update_values['High_Ans'] = new_highest_abs_answer
            if rounded_fastest_time < float(current_fastest_time):
                update_values['Fastest'] = rounded_fastest_time
            if name != discord_username:
                update_values['name'] = discord_username
            if current_fastest_time == 0:
                update_values['Fastest'] = rounded_fastest_time

            if update_values:
                update_query = "UPDATE profiles SET "
                update_query += ", ".join([f"{key} = %s" for key in update_values.keys()])
                update_query += ", EQ_Ans = EQ_Ans + %s"  # Add equations_answered update
                update_query += ", FreeC = FreeC + %s"  # Add currency update
                update_query += " WHERE discord_id = %s"

                cursor.execute(update_query, list(update_values.values()) + [new_equations_answered, currency_added,
                                                                             discord_id])
                connection.commit()
                print(f"Delve profile updated for user {discord_id}")

        else:
            # Insert a new profile
            insert_query = ("INSERT INTO profiles (discord_id, name, EQ_Ans, Free_High, "
                            "High_Ans, Fastest, NRG_V, NRG_M) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (discord_id, discord_username, new_equations_answered, new_highest_stage,
                                          new_highest_abs_answer, rounded_fastest_time, 3, 3,))
            connection.commit()
            print(f"New profile inserted for user {discord_id}")

        # Consume the results before closing
        cursor.fetchall()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def tld_update_profile(discord_id, discord_username, currency_added, new_equations_answered, new_tld_highest_stage):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Retrieve the current profile from the database
        select_query = "SELECT * FROM profiles WHERE discord_id = %s"
        cursor.execute(select_query, (discord_id,))
        result = cursor.fetchone()

        if result:
            name = result[2]
            currency = result[3]
            equations_answered = result[6]
            tld_highest_stage = result[8]

            # Updating values if necessary
            update_values = {}
            update_values['EQ_Ans'] = equations_answered
            update_values['FreeC'] = currency
            if new_tld_highest_stage > int(tld_highest_stage):
                update_values['TLD_High'] = new_tld_highest_stage
            if name != discord_username:
                update_values['name'] = discord_username

            if update_values:
                update_query = "UPDATE profiles SET "
                update_query += ", ".join([f"{key} = %s" for key in update_values.keys()])
                update_query += ", EQ_Ans = EQ_Ans + %s"  # Add equations_answered update
                update_query += ", FreeC = FreeC + %s"  # Add currency update
                update_query += " WHERE discord_id = %s"

                cursor.execute(update_query, list(update_values.values()) + [new_equations_answered, currency_added,
                                                                             discord_id])
                connection.commit()
                print(f"TLD Profile updated for user {discord_id}")

        else:
            # Insert a new profile
            insert_query = ("INSERT INTO profiles (discord_id, name, FreeC, EQ_Ans, TLD_High, NRG_V, NRG_M)"
                            " VALUES (%s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (discord_id, discord_username, currency_added, new_equations_answered,
                                          new_tld_highest_stage, 3, 3,))
            connection.commit()
            print(f"New profile inserted for user {discord_id}")

            # Consume the results before closing
        cursor.fetchall()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def chall_update_profile(discord_id, discord_username, currency_added, new_highest_stage, new_highest_abs_answer,
                         new_fastest_time, new_equations_answered, difficulty_level):
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
            chall_currency = result[4]
            equations_answered = result[6]
            current_highest_stage = result[9]
            highest_abs_answer = result[11]
            current_fastest_time = result[10]
            nrg_v = result[14]
            nrg_e = result[16]

            # Updating values if necessary
            update_values = {}
            update_values['EQ_Ans'] = equations_answered
            update_values['ChallC'] = chall_currency
            update_values['NRG_V'] = nrg_v - difficulty_level
            update_values['NRG_E'] = nrg_e + timedelta(minutes=difficulty_level * 20)
            if new_highest_stage > int(current_highest_stage):
                update_values['Chall_High'] = new_highest_stage
            if highest_abs_answer is None or new_highest_abs_answer > int(highest_abs_answer):
                update_values['High_Ans'] = new_highest_abs_answer
            if rounded_fastest_time < float(current_fastest_time):
                update_values['Fastest'] = rounded_fastest_time
            if name != discord_username:
                update_values['name'] = discord_username
            if current_fastest_time == 0:
                update_values['Fastest'] = rounded_fastest_time

            if update_values:
                update_query = "UPDATE profiles SET "
                update_query += ", ".join([f"{key} = %s" for key in update_values.keys()])
                update_query += ", EQ_Ans = EQ_Ans + %s"  # Add equations_answered update
                update_query += ", ChallC = ChallC + %s"  # Add currency update
                update_query += " WHERE discord_id = %s"

                cursor.execute(update_query, list(update_values.values()) + [new_equations_answered, currency_added,
                                                                             discord_id])
                connection.commit()
                print(f"Challenge profile updated for user {discord_id}")

        else:
            # Insert a new profile
            insert_query = ("INSERT INTO profiles (discord_id, name, EQ_Ans, Chall_High, "
                            "Chall_Ans, Fastest, NRG_V, NRG_M) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_query, (discord_id, discord_username, new_equations_answered, new_highest_stage,
                                          new_highest_abs_answer, rounded_fastest_time, 3, 3,))
            connection.commit()
            print(f"New profile inserted for user {discord_id}")

        # Consume the results before closing
        cursor.fetchall()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def challenge_time(discord_id):
    try:
        connection = connect()  # Establish a database connection
        cursor = connection.cursor()

        # Update NRG_T column with the current time for the specified user
        update_query = "UPDATE profiles SET NRG_T = %s WHERE discord_id = %s"
        current_time = datetime.now(timezone.utc)
        cursor.execute(update_query, (current_time, discord_id))
        connection.commit()

        print(f"NRG_T updated for user {discord_id} with current time")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def get_energy_info(discord_id):
    try:
        connection = connect()  # Establish a database connection
        cursor = connection.cursor()

        # Selecting the NRG_V value for a specific player
        select_query = "SELECT NRG_V FROM profiles WHERE discord_id = %s"
        cursor.execute(select_query, (discord_id,))
        result = cursor.fetchone()

        if result:
            nrg_v_value = result[0]
            return nrg_v_value
        else:
            print(f"No profile found for user {discord_id}")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)


def get_energy_max_info(discord_id):
    try:
        connection = connect()  # Establish a database connection
        cursor = connection.cursor()

        # Selecting the NRG_V value for a specific player
        select_query = "SELECT NRG_M FROM profiles WHERE discord_id = %s"
        cursor.execute(select_query, (discord_id,))
        result = cursor.fetchone()

        if result:
            nrg_m_value = result[0]
            return nrg_m_value
        else:
            print(f"No profile found for user {discord_id}")

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
                'FreeC': result[3],
                'ChallC': result[4],
                'achievement_points': result[5],
                'equations_solved': result[6],
                'highest_stage': result[7],
                'rounded_fastest_time': result[10],
                'new_highest_abs_answer': result[11],
                'shop_access': result[12],
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

        select_query = "SELECT name, Free_High from Profiles ORDER BY Free_High DESC LIMIT 10"
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


async def unlock_shop_access(discord_id):
    try:
        connection = connect()
        cursor = connection.cursor()

        update_query = "UPDATE profiles SET Shop = 1 WHERE discord_id = %s"
        cursor.execute(update_query, (discord_id,))
        connection.commit()
        print(f"Shop access unlocked for {discord_id}")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Error:", e)
