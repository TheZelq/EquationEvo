from connector import connect


def achievements_solved(discord_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        achievement_text = ""

        select_query = "SELECT user_id, equations_answered FROM profiles WHERE name = %s"
        cursor.execute(select_query, (discord_name,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            equations_answered = result[1]
            achievements = []

            select_query = "SELECT * FROM unlocked_achievements WHERE user_id = %s"
            cursor.execute(select_query, (user_id,))
            result2 = cursor.fetchall()

            if result2:
                for element in result2:
                    a = element[1]
                    achievements.append(a)

            if equations_answered != 0 and achievements.count(1) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Initiating the Dive** \n"
                cursor.execute(select_query, (user_id, 1))
                connection.commit()

            if equations_answered >= 10 and achievements.count(2) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Tenfold Diver** \n"
                cursor.execute(select_query, (user_id, 2))
                connection.commit()

            if equations_answered >= 100 and achievements.count(3) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Dive Centurion** \n"
                cursor.execute(select_query, (user_id, 3))
                connection.commit()

            if equations_answered >= 1000 and achievements.count(4) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Thousandth Conqueror** \n"
                cursor.execute(select_query, (user_id, 4))
                connection.commit()

            if equations_answered >= 2500 and achievements.count(5) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Equation Odyssey** \n"
                cursor.execute(select_query, (user_id, 5))
                connection.commit()

            if equations_answered >= 5000 and achievements.count(6) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Eternal Equation Virtuoso** \n"
                cursor.execute(select_query, (user_id, 6))
                connection.commit()

        cursor.close()
        connection.close()
        if achievement_text != "":
            return achievement_text
        return ""

    except Exception as e:
        print("Error:", e)
