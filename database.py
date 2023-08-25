from connector import connect


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
            if current_highest_stage and new_highest_stage > int(current_highest_stage):
                update_values['highest_stage'] = new_highest_stage
            if highest_abs_answer is None or new_highest_abs_answer > int(highest_abs_answer):
                update_values['highest_abs_answer'] = new_highest_abs_answer
            if current_fastest_time and rounded_fastest_time < float(current_fastest_time):
                update_values['fastest_time'] = rounded_fastest_time
            if name != discord_username:
                update_values['name'] = discord_username

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
                            "highest_abs_answer, fastest_time) VALUES (%s, %s, %s, %s, %s)")
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
