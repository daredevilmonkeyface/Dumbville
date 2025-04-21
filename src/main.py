import random

class Dumbville:
    def __init__(self):
        # Initial stats
        self.population = 10
        self.food = 50
        self.iq = 80
        self.happiness = 70

        self.special_events_triggered = False  # Track if special events already happened

        # Yearly disasters
        self.yearly_disasters = [
            "A great cheese famine struck the village.",
            "A baby was born with the power to shoot lightning. Mixed reactions.",
            "A mysterious fog rolled in, people forgot how doors work.",
            "A massive flood washed away everyone's socks. Panic.",
            "The cows started floating. The reason is still unknown.",
            "A plague of hiccups hit. Everyone is annoyed and exhausted.",
        ]

        # Hourly randomness
        self.hourly_events = [
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

        # Weather effects
        self.weather_conditions = [
            ("Sunny", lambda: self.increase_happiness(3)),
            ("Rainy", lambda: self.decrease_happiness(2)),
            ("Windstorm", lambda: self.food_loss(5)),
            ("Snowy", lambda: self.decrease_iq(3)),
            ("Meteor Shower", lambda: self.random_disaster()),
        ]

    # Functions to change stats
    def increase_happiness(self, amount):
        self.happiness += amount

    def decrease_happiness(self, amount):
        self.happiness -= amount

    def decrease_iq(self, amount):
        self.iq -= amount

    def food_loss(self, amount):
        self.food = max(0, self.food - amount)

    def random_disaster(self):
        self.population = max(0, self.population - 2)
        self.happiness -= 5
        self.iq -= 4

    # Yearly event
    def do_yearly_event(self):
        event = random.choice(self.yearly_disasters)
        print(f"\n💥 Yearly Disaster: {event}")
        
        if "famine" in event:
            self.food_loss(10)
            self.happiness -= 6
        elif "baby" in event:
            self.population += 2
            self.iq += 4
            self.happiness += 3
        elif "fog" in event:
            self.iq -= 5
            self.happiness -= 3
        elif "flood" in event:
            self.food_loss(8)
            self.happiness -= 4
        elif "floating cows" in event:
            self.happiness += 5
            self.iq -= 2
        elif "hiccups" in event:
            self.happiness -= 7
            self.population = max(1, self.population - 1)

    # Hourly event
    def do_hourly_update(self, hour):
        event = random.choice(self.hourly_events)
        print(f"🕒 Hour {hour}: {event}")

        if "gossip" in event:
            effect = random.choice(["good", "bad", "weird"])
            if effect == "good":
                self.increase_happiness(2)
            elif effect == "bad":
                self.decrease_happiness(3)
            elif effect == "weird":
                self.iq -= 1

        if "chickens" in event:
            self.food += 2

    # Weather
    def do_weather(self):
        condition, effect = random.choice(self.weather_conditions)
        print(f"\n🌤️ Weather Today: {condition}")
        effect()

    # Special Events (run once)
    def run_special_events(self):
        print("\n🌋 A volcano near Dumbville has started... voting?")
        print("1: Ask what it's voting on")
        print("2: Build a statue to gain favor")
        print("3: Ignore it, volcanoes are dumb")

        choice = input("Choose your action (1-3): ")
        if choice == "1":
            print("🗳️ It was voting on whether to erupt. You accidentally swayed it to 'no'! Yay!")
            self.increase_happiness(5)
        elif choice == "2":
            print("🗿 The volcano is pleased. It sends down warm lava hugs. Slightly burns crops.")
            self.increase_happiness(2)
            self.food_loss(5)
        elif choice == "3":
            print("🌋 It erupts out of spite. Classic volcano behavior.")
            self.random_disaster()
        else:
            print("😐 You stood there doing nothing. Volcano got bored and wandered off.")

        print("\n👽 An alien arrives and asks to attend Dumbville Elementary.")
        print("1: Welcome them with a muffin basket")
        print("2: Challenge them to an IQ test")
        print("3: Panic and run in circles")

        choice = input("Choose your action (1-3): ")
        if choice == "1":
            print("🧁 They loved the muffins and taught quantum agriculture.")
            self.iq += 5
            self.food += 10
        elif choice == "2":
            print("🧠 They scored 9000. Villagers feel dumb but inspired.")
            self.iq += 3
            self.happiness -= 2
        elif choice == "3":
            print("😵 Chaos ensued. Alien confused, left with mild disgust.")
            self.decrease_happiness(6)
        else:
            print("🤖 The alien got bored and turned into a cow.")

    # Main Simulation
    def run_simulation(self):
        self.year = 1

        if not self.special_events_triggered:
            self.run_special_events()
            self.special_events_triggered = True

        while self.population > 0 and self.iq > 0 and self.happiness > 0:
            print(f"\n====================")
            print(f"📆 Year {self.year} Begins")
            print(f"Population: {self.population}, Food: {self.food}, IQ: {self.iq}, Happiness: {self.happiness}")
            print("====================")

            self.do_weather()

            for hour in range(1, 25):
                self.do_hourly_update(hour)

            self.do_yearly_event()

            self.food -= self.population
            if self.food < 0:
                self.food = 0
                self.happiness -= 10
                print("⚠️ Not enough food! People are sad.")

            print(f"\n📊 End of Year {self.year}:")
            print(f"Population: {self.population}, Food: {self.food}, IQ: {self.iq}, Happiness: {self.happiness}")

            if self.population <= 0 or self.happiness <= 0 or self.iq <= 0:
                print("\n💀 Dumbville has collapsed. Reality reboot recommended. Scroll to the top to read what happened in the civilization's era.")
                print("""\nNotes: I used ChatGPT to help me write and improve the Python code for this project.
    I made sure I understood what the code was doing and changed things to make it my own.
    I also used books and YouTube to learn along the way.
    I'm still learning Python, so I couldn't have done this completely on my own — but I had a lot of fun figuring things out. 🙂""")
                break

            self.year += 1

if __name__ == "__main__":
    game = Dumbville()
    game.run_simulation()

