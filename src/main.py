import random

# Initial stats
population = 10
food = 50
iq = 80
happiness = 70

special_events_triggered = False  # Track if special events already happened

# Yearly disasters
yearly_disasters = [
    "A great cheese famine struck the village.",
    "A baby was born with the power to shoot lightning. Mixed reactions.",
    "A mysterious fog rolled in, people forgot how doors work.",
    "A massive flood washed away everyone's socks. Panic.",
    "The cows started floating. The reason is still unknown.",
    "A plague of hiccups hit. Everyone is annoyed and exhausted.",
]

# Hourly randomness
hourly_events = [
    "Someone mistook a scorpion for their grandma.",
    "The chickens formed a heavy metal band.",
    "Gossip: Villager Zed claims the moon is his granny.",
    "The mayor sneezed and declared that everybody barricades their windows.",
    "A mysterious glowing rock was found. Everyone licked it 8274927 times. Each.",
    "Weather turned into bananas. No one knows what to wear.",
    "A child claims to have invented gravity. No Arguments follow.",
    "A squirrel gave an inspiring speech.",
    "The clouds spelled 'bum'. No one is sure why.",
    "Gossip: GEYUQWHE872Y87EY8IUAJS saw a potato whispering to itself.",
    "Gossip: Someone legally changed their name to 2378rtgyuf9t3e6gqi7yew890g29ehqyqyeheuij",
]

# Functions to change stats
def increase_happiness(amount):
    global happiness
    happiness += amount

def decrease_happiness(amount):
    global happiness
    happiness -= amount

def decrease_iq(amount):
    global iq
    iq -= amount

def food_loss(amount):
    global food
    food = max(0, food - amount)

def random_disaster():
    global population, happiness, iq
    population = max(0, population - 2)
    happiness -= 5
    iq -= 4

# Weather effects
weather_conditions = [
    ("Sunny", lambda: increase_happiness(3)),
    ("Rainy", lambda: decrease_happiness(2)),
    ("Windstorm", lambda: food_loss(5)),
    ("Snowy", lambda: decrease_iq(3)),
    ("Meteor Shower", lambda: random_disaster()),
]

# Yearly event
def do_yearly_event():
    global population, food, iq, happiness
    event = random.choice(yearly_disasters)
    print(f"\n💥 Yearly Disaster: {event}")
    
    if "famine" in event:
        food_loss(10)
        happiness -= 6
    elif "baby" in event:
        population += 2
        iq += 4
        happiness += 3
    elif "fog" in event:
        iq -= 5
        happiness -= 3
    elif "flood" in event:
        food_loss(8)
        happiness -= 4
    elif "floating cows" in event:
        happiness += 5
        iq -= 2
    elif "hiccups" in event:
        happiness -= 7
        population = max(1, population - 1)

# Hourly event
def do_hourly_update(hour):
    event = random.choice(hourly_events)
    print(f"🕒 Hour {hour}: {event}")

    if "gossip" in event:
        effect = random.choice(["good", "bad", "weird"])
        if effect == "good":
            increase_happiness(2)
        elif effect == "bad":
            decrease_happiness(3)
        elif effect == "weird":
            global iq
            iq -= 1

    if "chickens" in event:
        global food
        food += 2

# Weather
def do_weather():
    condition, effect = random.choice(weather_conditions)
    print(f"\n🌤️ Weather Today: {condition}")
    effect()

# Special Events (run once)
def run_special_events():
    global food, happiness, iq, population
    print("\n🌋 A volcano near Dumbville has started... voting?")
    print("1: Ask what it's voting on")
    print("2: Build a statue to gain favor")
    print("3: Ignore it, volcanoes are dumb")

    choice = input("Choose your action (1-3): ")
    if choice == "1":
        print("🗳️ It was voting on whether to erupt. You accidentally swayed it to 'no'! Yay!")
        increase_happiness(5)
    elif choice == "2":
        print("🗿 The volcano is pleased. It sends down warm lava hugs. Slightly burns crops.")
        increase_happiness(2)
        food_loss(5)
    elif choice == "3":
        print("🌋 It erupts out of spite. Classic volcano behavior.")
        random_disaster()
    else:
        print("😐 You stood there doing nothing. Volcano got bored and wandered off.")

    print("\n👽 An alien arrives and asks to attend Dumbville Elementary.")
    print("1: Welcome them with a muffin basket")
    print("2: Challenge them to an IQ test")
    print("3: Panic and run in circles")

    choice = input("Choose your action (1-3): ")
    if choice == "1":
        print("🧁 They loved the muffins and taught quantum agriculture.")
        iq += 5
        food += 10
    elif choice == "2":
        print("🧠 They scored 9000. Villagers feel dumb but inspired.")
        iq += 3
        happiness -= 2
    elif choice == "3":
        print("😵 Chaos ensued. Alien confused, left with mild disgust.")
        decrease_happiness(6)
    else:
        print("🤖 The alien got bored and turned into a cow.")

# Main Simulation
def run_simulation():
    global population, food, iq, happiness, special_events_triggered
    year = 1

    if not special_events_triggered:
        run_special_events()
        special_events_triggered = True

    while population > 0 and iq > 0 and happiness > 0:
        print(f"\n====================")
        print(f"📆 Year {year} Begins")
        print(f"Population: {population}, Food: {food}, IQ: {iq}, Happiness: {happiness}")
        print("====================")

        do_weather()

        for hour in range(1, 25):
            do_hourly_update(hour)

        do_yearly_event()

        food -= population
        if food < 0:
            food = 0
            happiness -= 10
            print("⚠️ Not enough food! People are sad.")

        print(f"\n📊 End of Year {year}:")
        print(f"Population: {population}, Food: {food}, IQ: {iq}, Happiness: {happiness}")

        if population <= 0 or happiness <= 0 or iq <= 0:
            print("\n💀 Dumbville has collapsed. Reality reboot recommended. Scroll to the top to read what happened in the civilization's era.")
            print("""\nNotes: I used ChatGPT to help me write and improve the Python code for this project.
I made sure I understood what the code was doing and changed things to make it my own.
I also used books and YouTube to learn along the way.
I'm still learning Python, so I couldn't have done this completely on my own — but I had a lot of fun figuring things out. 🙂""")
            break

        year += 1

run_simulation()
