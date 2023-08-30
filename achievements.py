from connector import connect


def achievements_solved(discord_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        achievement_text = ""

        select_query = "SELECT user_id, equations_answered, highest_stage FROM profiles WHERE name = %s"
        cursor.execute(select_query, (discord_name,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            equations_answered = result[1]
            highest_stage = result[2]
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

            if highest_stage >= 4 and achievements.count(7) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Daring Diver** \n"
                cursor.execute(select_query, (user_id, 7))
                connection.commit()

            if highest_stage >= 8 and achievements.count(8) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Equation Enthusiast** \n"
                cursor.execute(select_query, (user_id, 8))
                connection.commit()

            if highest_stage >= 12 and achievements.count(9) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Mathematical Trailblazer** \n"
                cursor.execute(select_query, (user_id, 9))
                connection.commit()

            if highest_stage >= 16 and achievements.count(10) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Masterful Equator** \n"
                cursor.execute(select_query, (user_id, 10))
                connection.commit()

            if highest_stage >= 20 and achievements.count(11) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Champion of Complexity** \n"
                cursor.execute(select_query, (user_id, 11))
                connection.commit()

            if highest_stage >= 24 and achievements.count(12) == 0:
                select_query = "INSERT INTO unlocked_achievements (user_id, achievement_id) VALUES (%s, %s)"
                achievement_text += "Achievement Unlocked: **Eternal Equation Enigma** \n"
                cursor.execute(select_query, (user_id, 12))
                connection.commit()

        cursor.close()
        connection.close()
        if achievement_text != "":
            return achievement_text
        return ""

    except Exception as e:
        print("Error:", e)
