
def get_bot_response(message):

    message = message.lower().strip()

    # Welcome
    if any(word in message for word in ["hello", "hi", "hey"]):
        return (
            "Welcome to FITBOT Smart Habit Coach!\n\n"
            "I can help you build healthy daily habits.\n\n"
            "You can ask me about:\n"
            "1. Daily routine\n"
            "2. Sleep habits\n"
            "3. Nutrition\n"
            "4. Physical activities\n"
            "5. Motivation\n\n"
            "What would you like to improve today?"
        )

    # Daily routine
    elif "routine" in message or "daily plan" in message:
        return (
            "Let's create a healthy daily routine!\n\n"
            "Morning: Start your day calmly and have breakfast.\n"
            "Afternoon: Take regular breaks and stay hydrated.\n"
            "Evening: Enjoy an activity you like.\n"
            "Night: Make time for relaxation and sleep.\n\n"
            "FITBOT Question:\n"
            "Which part of your daily routine would you "
            "like to improve first?"
        )

    # Sleep coach
    elif "sleep" in message:
        return (
            "Welcome to FITBOT Sleep Coach!\n\n"
            "Here are some helpful habits:\n"
            "1. Maintain a regular sleep schedule.\n"
            "2. Create a calm sleeping environment.\n"
            "3. Reduce stimulating activities before bedtime.\n"
            "4. Give yourself enough time to rest.\n\n"
            "Let's personalize your routine!\n"
            "What would you like help with?\n"
            "A. Building a bedtime routine\n"
            "B. Reducing screen time before bed\n"
            "C. Understanding healthy sleep habits"
        )

    # Nutrition coach
    elif any(word in message for word in ["food", "diet", "nutrition"]):
        return (
            "Welcome to FITBOT Nutrition Coach!\n\n"
            "A balanced eating routine can include:\n"
            "1. Fruits and vegetables.\n"
            "2. Whole grains.\n"
            "3. Protein-rich foods.\n"
            "4. Regular meals and water.\n\n"
            "Let's understand your needs!\n"
            "What would you like to explore?\n"
            "A. Healthy breakfast ideas\n"
            "B. Nutritious snack ideas\n"
            "C. Balanced meal ideas"
        )

    # Movement coach
    elif any(word in message for word in
             ["workout", "exercise", "movement", "activity"]):
        return (
            "Welcome to FITBOT Activity Coach!\n\n"
            "Choose an enjoyable activity:\n"
            "1. Walking\n"
            "2. Cycling\n"
            "3. Dancing\n"
            "4. Swimming\n"
            "5. Gentle stretching\n\n"
            "FITBOT Question:\n"
            "Which activity do you enjoy most?\n"
            "I can help you create a flexible activity plan."
        )

    # Hydration
    elif "water" in message or "hydration" in message:
        return (
            "Welcome to FITBOT Hydration Coach!\n\n"
            "A few useful habits:\n"
            "1. Keep water accessible.\n"
            "2. Drink regularly throughout the day.\n"
            "3. Remember to drink more when you are "
            "active or in hot weather.\n\n"
            "Would you like help building a daily "
            "hydration reminder routine?"
        )

    # Motivation
    elif "motivation" in message or "lazy" in message:
        return (
            "Welcome to FITBOT Motivation Coach!\n\n"
            "Remember: Healthy habits are built gradually.\n\n"
            "Try choosing one small action today:\n"
            "1. Organize your daily routine.\n"
            "2. Enjoy an activity you like.\n"
            "3. Take a relaxing break.\n"
            "4. Make time for sufficient rest.\n\n"
            "What is one healthy habit you would "
            "like to start?"
        )

    # General fitness
    elif "fitness" in message:
        return (
            "FITBOT Fitness Guide!\n\n"
            "Well-being involves several connected areas:\n"
            "1. Enjoyable physical activity.\n"
            "2. Balanced nutrition.\n"
            "3. Quality sleep.\n"
            "4. Hydration.\n"
            "5. Mental relaxation.\n\n"
            "Which area would you like to explore?"
        )

    else:
        return (
            "I'm FITBOT Smart Habit Coach!\n\n"
            "I didn't fully understand that question.\n"
            "Try asking me about your daily routine, "
            "sleep, nutrition, movement or motivation.\n\n"
            "You can also explain what you want to improve "
            "in your own words."
        )
