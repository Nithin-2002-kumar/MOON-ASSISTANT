🌙 MOON Assistant
A futuristic voice-controlled AI assistant with multimodal capabilities, built in Python. MOON combines speech recognition, natural language processing, computer vision, and various AI services to create a comprehensive personal assistant experience.

✨ Features
Voice Interaction: Speech-to-text and text-to-speech capabilities

Natural Language Understanding: Intent recognition and processing

Computer Vision: Object detection, face recognition, and color detection

AI Integration: Grok AI (xAI) for advanced reasoning

Productivity Tools: Email, reminders, weather, and app control

Modern HUD Interface: Futuristic graphical interface with real-time logging

🛠️ Installation
Clone the repository:

bash
git clone <repository-url>
cd moon-assistant
Install required dependencies:

bash
pip install -r requirements.txt
Set up your API keys in config.py:

OpenWeatherMap API key for weather functionality

xAI API key for Grok integration

Email credentials for email functionality

## Model Files Setup

Download the required YOLO model files:

1. Download `yolov3.weights` from [Official YOLO website](https://pjreddie.com/darknet/yolo/)
2. Place it in the `models/` directory
3. Download `yolov3.cfg` from the same source
4. Download `coco.names` from [COCO dataset](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

📁 Project Structure
text
moon-assistant/
├── core/
│   ├── config.py          # Configuration and API keys
│   ├── memory.py          # Persistent memory system
│   ├── nlp.py            # Natural language processing
│   ├── speech.py         # Speech recognition and synthesis
│   └── vision.py         # Computer vision capabilities
├── skills/
│   ├── apps.py           # Application management
│   ├── browser.py        # Web browsing functionality
│   ├── emailer.py        # Email sending
│   ├── grok.py           # Grok AI integration
│   ├── reminders.py      # Reminder system
│   └── weather.py        # Weather information
├── ui/
│   └── hud.py            # Graphical user interface
└── main.py               # Main application entry point
🚀 Usage
Run the assistant with:

bash
python main.py
Voice Commands
MOON responds to the wake phrase "hey moon" followed by commands like:

"open notepad" - Launches applications

"search python tutorials" - Performs web searches

"what time is it" - Tells current time and date

"set a reminder" - Creates timed reminders

"check weather in London" - Gets weather information

"scan the room" - Performs object detection

"ask Grok about AI" - Queries the Grok AI model

⚙️ Configuration
Edit config.py to customize:

API keys for various services

Email settings for notification functionality

File paths for YOLO model files

Speech synthesis parameters

🔧 Dependencies
Key dependencies include:

speechrecognition - Speech-to-text functionality

pyttsx3 - Text-to-speech synthesis

opencv-python - Computer vision capabilities

scikit-learn - NLP intent classification

xai-sdk - Grok AI integration

tkinter - Graphical user interface

🎯 Future Enhancements
Planned improvements:

Enhanced vision capabilities with proper YOLO model integration

Advanced face recognition with DeepFace

Emotion detection from facial expressions

Multi-language support

Plugin system for extendable functionality

Mobile app companion

📝 License
This project is for educational and personal use. Please ensure you comply with the terms of service for all integrated APIs and services.

🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

Note: This project requires proper API keys and model files for full functionality. Some features may require additional setup beyond the basic installation.