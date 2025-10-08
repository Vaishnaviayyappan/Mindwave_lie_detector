NeuroSky Lie Detector using Brain-Computer Interface
A Python application that uses a NeuroSky MindWave EEG headset to simulate a lie detection test. This project demonstrates a fundamental Brain-Computer Interface (BCI) concept by measuring the brain's response to significant stimuli, a simplified version of the Oddball Paradigm often used in neuroscience research.

🧠 How It Works
This application is based on the principle that the brain produces a stronger electrical response to an unexpected but meaningful stimulus. We measure this using NeuroSky's proprietary "Attention" metric.

The "Secret": The user is instructed to think of a specific playing card (e.g., the Ace of Spades).
The Stimulus: The application displays a sequence of random playing cards, including the "secret" card.
The Brain Response: When the secret card appears, the user's brain recognition of this significant stimulus is expected to cause a spike in the "Attention" value measured by the MindWave headset.
The Analysis: The application records the average "Attention" level for each card. It then compares the response to the secret card against the average response to all other cards to determine if a significant difference exists.
Disclaimer: This is an educational project and a scientific demonstration, not a forensic-grade or validated lie detector. The results are for illustrative purposes only and should not be used to make real-world judgments about honesty.

✨ Features
Real EEG Hardware Integration: Connects directly to the NeuroSky MindWave headset.
Oddball Paradigm Simulation: Implements a classic BCI experiment design.
Real-time Data Collection: Acquires and processes live brainwave data.
Visual Stimuli Display: A clean Pygame interface for presenting the card sequence.
Automated Analysis: Provides a simple, automated conclusion based on the collected data.
🔧 Hardware Requirements
Required Equipment
NeuroSky MindWave Mobile 1 or 2: The core EEG sensor for this project.
A Computer: Windows, macOS, or Linux with built-in or USB Bluetooth.
Bluetooth Adapter: If your computer does not have built-in Bluetooth.
Supported Headsets
NeuroSky MindWave Mobile 1
NeuroSky MindWave Mobile 2
⚙️ Software Setup
Step 1: Install Python Dependencies
First, install the necessary Python library for the GUI.

pip install pygame
BASH
Step 2: Install BlueMuse (Critical Step)
BlueMuse is the essential bridge that connects your MindWave headset to Python applications.

Download: Get the installer from the official NeuroSky BlueMuse page.
Install: Run the installer and follow the on-screen instructions.
Connect:
Power on your MindWave headset.
Open BlueMuse.
Click "Search" to find your headset.
Once found, click Connect. You should see data values like "Attention" and "Meditation" updating in real-time.
Keep BlueMuse Running: Leave BlueMuse open in the background while you run the Python script.
🚀 Running the Application
Step 1: Prepare the Hardware
Ensure your MindWave headset is fully charged.
Turn on the headset and pair it with your computer via Bluetooth.
Open BlueMuse and connect to your headset. Confirm that you see a live data stream.
Step 2: Run the Experiment
Execute the main script from your terminal:

python main.py
BASH
Step 3: Follow the Instructions
The screen will prompt you to "Think of this card: [Secret Card]". Memorize the card shown.
Press the SPACE key to begin the experiment.
A sequence of cards will be displayed. Try to remain calm and focused. A fixation cross (+) will appear between each card.
The experiment will automatically conclude after all cards have been shown.
An analysis screen will appear, comparing the brain's response to the secret card versus the other cards and providing a simple conclusion.
📁 Project Structure
mindwave_lie_detector/
│
├── main.py              # Main application with GUI and experiment logic
├── config.py            # Configuration for cards, timing, and thresholds
├── requirements.txt     # Python dependencies
└── README.md            # This file
BASH
config.py Explained
SECRET_CARD: The card the user is instructed to think of.
DECK: The list of all cards that will be shown.
CARD_DISPLAY_TIME: How long (in milliseconds) each card is shown.
ATTENTION_THRESHOLD: The minimum attention value that is considered a "significant" response. You can adjust this if you find the system is too sensitive or not sensitive enough.
🔬 Understanding the Code
main.py
MindWaveDataCollector: A separate thread that handles the socket connection to BlueMuse, ensuring the GUI doesn't freeze while waiting for data. It parses the JSON stream from BlueMuse.
LieDetectorApp: The main application class. It manages the Pygame window, the experiment state, and the final analysis. It calls the data collector to get attention readings during the experiment.
🐛 Troubleshooting
Error: Connection refused. Is BlueMuse running and connected to the headset?
Problem: The script cannot connect to BlueMuse.

Solutions:

Is BlueMuse running? Make sure the BlueMuse application is open.
Is the headset connected? In BlueMuse, ensure your headset shows a green "Connected" status.
Restart everything: Close the Python script, disconnect/reconnect the headset in BlueMuse, and then run the script again.
No Significant Difference is Detected
Problem: The analysis concludes "No significant response detected," even when you are thinking of the card.

Solutions:

Adjust Threshold: Try lowering the ATTENTION_THRESHOLD in config.py to a value like 50. This makes the system more sensitive.
Check Sensor Contact: Ensure the ear clip and forehead sensor are making good, clean contact with your skin. Dry skin or hair can interfere with the signal.
Minimize Movement: Try to stay very still, minimize blinking, and avoid clenching your jaw during the card presentation. These muscle movements create electrical noise that can obscure the brain signal.
Be Patient: The "Attention" metric is an approximation and can vary. You may need to run the experiment a few times to get a feel for it.
random is not defined Error
Problem: A NameError occurred in the script.

Solution: Ensure you are using the latest version of the code from the repository. The random module must be imported at the top of main.py.
📸 Screenshots

🔮 Future Enhancements
 Raw EEG Analysis: Connect directly to the EEG data stream to perform a true P300 wave analysis instead of relying on the proprietary "Attention" metric.
 User Calibration: A training phase to establish a personalized baseline for each user.
 More Complex Paradigms: Implement the Guilty Knowledge Test with more than one target stimulus.
 Improved Analysis: Use statistical tests (like a t-test) to determine if the difference between responses is statistically significant.
📚 Scientific Background
Oddball Paradigm: A classic experimental design where a participant is presented with a sequence of stimuli, a standard one and a rare "oddball" one, to elicit a P300 brain response.
P300 Wave: An event-related potential (ERP) component that is positive in voltage and peaks around 300-600ms after the presentation of a stimulus. It is associated with processes like decision-making and context updating.
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


📧 Contact
Vaishnavi A - vaishnaviayyappan16@gmail.com

Project Link: https://github.com/yourusername/mindwave-lie-detector

⚠️ Final Disclaimer
This application is a tool for learning and experimentation. The concept of "lie detection" is ethically complex and scientifically controversial. This project should not be used to make any serious judgments about a person's honesty or for any security purpose.
