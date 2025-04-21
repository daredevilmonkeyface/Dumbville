import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QInputDialog,
)
from PyQt5.QtCore import QTimer, QObject, QRunnable, QThreadPool, pyqtSignal
from PyQt5 import QtGui

import random
import requests

YEAR_DELAY = 1000
HOUR_DELAY = 100
# ^^ change these to change the amount of time (ms) after each hour and after each year

# --- Worker for background text expansion ---
class WorkerSignals(QObject):
    finished = pyqtSignal(int, str)

class ExpandWorker(QRunnable):
    def __init__(self, index, text, signal):
        super().__init__()
        self.index = index
        self.text = text
        self.signal = signal

    def run(self):
        instr = (
            "Process the following text, by adding emojis and markdown,"
            " as well as adding funny details."
            " Keep the response within one short sentence."
            " Do not remove details from the original prompt."
        )
        # blocking HTTP call in worker thread
        res = requests.get(f"https://text.pollinations.ai/{instr}\n\n{self.text}")
        while res.status_code != 200:
            res = requests.get(f"https://text.pollinations.ai/{instr}\n\n{self.text}")
        r = "---\nPowered by Pollinations.AI free text APIs. [Support our mission](https://pollinations.ai/redirect/kofi) to keep AI accessible for everyone."
        self.signal.finished.emit(self.index, res.text.replace(r, "").replace("—", " - "))

class Dumbville(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dumbville")
        self.setGeometry(100, 100, 800, 600)

        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.stats_view = QHBoxLayout()
        self.all_stats = ["population", "food", "iq", "happiness"]
        for stat in self.all_stats:
            label = QLabel(f"{stat.upper()}: -")
            self.stats_view.addWidget(label)
            setattr(self, f"{stat}_label", label)
        self.layout.addLayout(self.stats_view)

        self.main_text = QTextEdit()
        self.main_text.setReadOnly(True)
        self.main_text.acceptRichText()
        self.layout.addWidget(self.main_text)

        self.init_game()
        self.run_simulation()

    def update_labels(self):
        for stat in self.all_stats:
            value = getattr(self, stat)
            label = getattr(self, f"{stat}_label")
            t = f"{stat.upper()}: {value}"
            label.setText(t)
    
    def send_message(self, message):
        t = self.main_text.toMarkdown()
        t += message
        self.main_text.setMarkdown(t)
        self.main_text.moveCursor(QtGui.QTextCursor.End)

    def receive_input(self, prompt):
        text, ok = QInputDialog.getText(self, "Select an Option", prompt)
        if ok and text:
            return text
        else:
            return ""

    def init_game(self):
        # Initial stats
        self.population = 10
        self.food = 50
        self.iq = 80
        self.happiness = 70

        self.special_events_triggered = False  # Track if special events already happened

        # Yearly disasters
        raw_yearly_disasters = [
            "A great cheese famine struck the village.",
            "A baby was born with the power to shoot lightning. Mixed reactions.",
            "A mysterious fog rolled in, people forgot how doors work.",
            "A massive flood washed away everyone's socks. Panic.",
            "The cows started floating. The reason is still unknown.",
            "A plague of hiccups hit. Everyone is annoyed and exhausted.",
        ]

        # Hourly randomness
        raw_hourly_events = [
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

        # Store raw & expanded placeholders
        self.raw_yearly_disasters = raw_yearly_disasters
        self.expanded_yearly = [None] * len(raw_yearly_disasters)
        self.raw_hourly_events = raw_hourly_events
        self.expanded_hourly = [None] * len(raw_hourly_events)

        # Setup signals & workers
        self.yearly_signals = WorkerSignals()
        self.yearly_signals.finished.connect(self.handle_yearly_result)
        for i, txt in enumerate(raw_yearly_disasters):
            QThreadPool.globalInstance().start(ExpandWorker(i, txt, self.yearly_signals))

        self.hourly_signals = WorkerSignals()
        self.hourly_signals.finished.connect(self.handle_hourly_result)
        for i, txt in enumerate(raw_hourly_events):
            QThreadPool.globalInstance().start(ExpandWorker(i, txt, self.hourly_signals))


        # Weather effects
        self.weather_conditions = [
            ("Sunny", lambda: self.increase_happiness(3)),
            ("Rainy", lambda: self.decrease_happiness(2)),
            ("Windstorm", lambda: self.food_loss(5)),
            ("Snowy", lambda: self.decrease_iq(3)),
            ("Meteor Shower", lambda: self.random_disaster()),
        ]

    # Callbacks for worker results
    def handle_yearly_result(self, idx, expanded):
        self.expanded_yearly[idx] = expanded

    def handle_hourly_result(self, idx, expanded):
        self.expanded_hourly[idx] = expanded

    # Functions to change stats
    def increase_happiness(self, amount):
        self.happiness += amount
        self.update_labels()

    def decrease_happiness(self, amount):
        self.happiness -= amount
        self.update_labels()

    def decrease_iq(self, amount):
        self.iq -= amount
        self.update_labels()

    def food_loss(self, amount):
        self.food = max(0, self.food - amount)
        self.update_labels()

    def random_disaster(self):
        self.population = max(0, self.population - 2)
        self.happiness -= 5
        self.iq -= 4
        self.update_labels()

    # Yearly event
    def do_yearly_event(self):
        i = random.randrange(len(self.raw_yearly_disasters))
        raw_event = self.raw_yearly_disasters[i]
        event = self.expanded_yearly[i] or raw_event
        self.send_message(f"\n💥 **Yearly Disaster**: {event}")
        
        if "famine" in raw_event:
            self.food_loss(10)
            self.happiness -= 6
        elif "baby" in raw_event:
            self.population += 2
            self.iq += 4
            self.happiness += 3
        elif "fog" in raw_event:
            self.iq -= 5
            self.happiness -= 3
        elif "flood" in raw_event:
            self.food_loss(8)
            self.happiness -= 4
        elif "floating cows" in raw_event:
            self.happiness += 5
            self.iq -= 2
        elif "hiccups" in raw_event:
            self.happiness -= 7
            self.population = max(1, self.population - 1)

        self.update_labels()

    # Hourly event
    def do_hourly_update(self, hour):
        i = random.randrange(len(self.raw_hourly_events))
        raw_event = self.raw_hourly_events[i]
        event = self.expanded_hourly[i] or raw_event
        self.send_message(f"🕒 **Hour {hour}**: {event}")

        if "gossip" in raw_event:
            effect = random.choice(["good", "bad", "weird"])
            if effect == "good":
                self.increase_happiness(2)
            elif effect == "bad":
                self.decrease_happiness(3)
            elif effect == "weird":
                self.iq -= 1

        if "chickens" in raw_event:
            self.food += 2

        self.update_labels()

    # Weather
    def do_weather(self):
        condition, effect = random.choice(self.weather_conditions)
        self.send_message(f"\n🌤️ **Weather Today**: {condition}")
        effect()

    # Special Events (run once)
    def run_special_events(self):
        self.send_message("---\n## 🌋 A volcano near Dumbville has started... voting?")
        self.send_message("1: Ask what it's voting on")
        self.send_message("2: Build a statue to gain favor")
        self.send_message("3: Ignore it, volcanoes are dumb")

        choice = self.receive_input("Choose your action (1-3): ")
        if choice == "1":
            self.send_message("### 🗳️ It was voting on whether to erupt. You accidentally swayed it to 'no'! Yay!")
            self.increase_happiness(5)
        elif choice == "2":
            self.send_message("### 🗿 The volcano is pleased. It sends down warm lava hugs. Slightly burns crops.")
            self.increase_happiness(2)
            self.food_loss(5)
        elif choice == "3":
            self.send_message("### 🌋 It erupts out of spite. Classic volcano behavior.")
            self.random_disaster()
        else:
            self.send_message("### 😐 You stood there doing nothing. Volcano got bored and wandered off.")

        self.update_labels()

        self.send_message("---\n## 👽 An alien arrives and asks to attend Dumbville Elementary.")
        self.send_message("1: Welcome them with a muffin basket")
        self.send_message("2: Challenge them to an IQ test")
        self.send_message("3: Panic and run in circles")

        choice = self.receive_input("Choose your action (1-3): ")
        if choice == "1":
            self.send_message("### 🧁 They loved the muffins and taught quantum agriculture.")
            self.iq += 5
            self.food += 10
        elif choice == "2":
            self.send_message("### 🧠 They scored 9000. Villagers feel dumb but inspired.")
            self.iq += 3
            self.happiness -= 2
        elif choice == "3":
            self.send_message("### 😵 Chaos ensued. Alien confused, left with mild disgust.")
            self.decrease_happiness(6)
        else:
            self.send_message("### 🤖 The alien got bored and turned into a cow.")

        self.update_labels()

    # Main Simulation
    def run_simulation(self):
        self.send_message("By daredevilmonkeyface")

        self.year = 1

        def start_special_events():
            self.run_special_events()
            self.special_events_triggered = True
            QTimer.singleShot(YEAR_DELAY, run_year)  # Wait before starting the first year

        def run_year():
            if self.population > 0 and self.iq > 0 and self.happiness > 0:
                self.send_message(f"\n---")
                self.send_message(f"📆 Year {self.year} Begins")
                self.send_message(f"Population: {self.population}, Food: {self.food}, IQ: {self.iq}, Happiness: {self.happiness}")
                self.send_message("---")

                self.do_weather()

                def run_hourly_updates(hour=1):
                    if hour <= 24:
                        self.do_hourly_update(hour)
                        QTimer.singleShot(HOUR_DELAY, lambda: run_hourly_updates(hour + 1))  # Wait before the next hour
                    else:
                        self.do_yearly_event()
                        self.food -= self.population
                        if self.food < 0:
                            self.food = 0
                            self.happiness -= 10
                            self.update_labels()
                            self.send_message("⚠️ Not enough food! People are sad.")

                        self.send_message(f"\n📊 End of Year {self.year}:")
                        self.send_message(f"Population: {self.population}, Food: {self.food}, IQ: {self.iq}, Happiness: {self.happiness}")

                        if self.population <= 0 or self.happiness <= 0 or self.iq <= 0:
                            self.send_message("\n💀 Dumbville has collapsed. Reality reboot recommended. Scroll to the top to read what happened in the civilization's era.")
                            self.send_message("""\nNotes: I used ChatGPT to help me write and improve the Python code for this project.
        I made sure I understood what the code was doing and changed things to make it my own.
        I also used books and YouTube to learn along the way.
        I'm still learning Python, so I couldn't have done this completely on my own — but I had a lot of fun figuring things out. 🙂""")
                            self.send_message("---\nPowered by Pollinations.AI free text APIs. [Support our mission](https://pollinations.ai/redirect/kofi) to keep AI accessible for everyone.")
                        else:
                            self.year += 1
                            QTimer.singleShot(1000, run_year)  # Wait 1 second before starting the next year

                run_hourly_updates()

        if not self.special_events_triggered:
            QTimer.singleShot(1000, start_special_events)  # Wait 1 second before starting special events
        else:
            run_year()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the main window
    window = Dumbville()
    window.show()

    # Execute the application
    sys.exit(app.exec_())

