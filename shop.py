shop_items = [
    {
        "name": "Broken Clock",
        "description": "Even it is right twice a day",
        "price": 1000,
    },
]


# Checking if a user can access the shop
def shop_access(profile_data):
    return profile_data.get("highest_stage", 0) >= 9 and profile_data.get("shop_access", 0) == 1
