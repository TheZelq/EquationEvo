from connector import connect


def close(connection, cursor):
    cursor.close()
    connection.close()


def update_highest_stage(discord_id, new_highest_stage):
    try:
        connection = connect()
        cursor = connection.cursor()

        # Retrieve the current highest stage from the database
        select_query = "SELECT highest_stage FROM profiles WHERE discord_id = %s"
        cursor.execute(select_query, (discord_id,))
        result = cursor.fetchone()

        if result:
            current_highest_stage = result[0]
            # Check if the new value is higher and update if necessary
            if new_highest_stage > current_highest_stage:
                update_query = "UPDATE profiles SET highest_stage = %s WHERE discord_id = %s"
                cursor.execute(update_query, (new_highest_stage, discord_id))
                connection.commit()
                print(f"User {discord_id}'s highest stage updated to {new_highest_stage}")
        else:
            # User doesn't exist, insert a new profile
            insert_query = "INSERT INTO profiles (discord_id, highest_stage) VALUES (%s, %s)"
            cursor.execute(insert_query, (discord_id, new_highest_stage))
            connection.commit()
            print(f"New profile inserted for user {discord_id}")

        close(connection, cursor)
    except Exception as e:
        print("Error:", e)


def insert_new_profile(discord_id, name, currency, achievement_points, equations_answered, highest_stage, fastest_time, highest_abs_answer):
    try:
        connection = connect()
        cursor = connection.cursor()

        insert_query = "INSERT INTO profiles (discord_id, name, currency, achievement_points, equations_answered, highest_stage, fastest_time, highest_abs_answer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print("Executing query:", insert_query)
        cursor.execute(insert_query, (discord_id, name, currency, achievement_points, equations_answered, highest_stage, fastest_time, highest_abs_answer))
        connection.commit()
        print(f"New profile inserted for user {discord_id}")

        close(connection, cursor)
    except Exception as e:
        print("Error:", e)
