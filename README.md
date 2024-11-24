# Sample AI Assistant

This project provides two AI assistants:

1. Webcam Assistant: Interact with an AI assistant that captures video using your webcam
2. Desktop Assistant: Interact with an AI assistant that captures your desktop screen

## Requirements

### API Keys

You need the following API keys to run the project:

- OPENAI_API_KEY: Required for OpenAI GPT models
- GOOGLE_API_KEY: Optional, only needed if you use Google's AI models

Store these keys in a `.env` file in the root directory of the project or set them as environment variables.

### System Requirements

- Python: Version 3.7 or later
- Apple Silicon Users: If you're running this on Apple Silicon, install PortAudio:

```bash
brew install portaudio
```

## Installation

### Step 1: Clone the Repository

Clone the repository and navigate into the project directory:

```bash
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Create a Virtual Environment

Create a virtual environment to keep dependencies isolated:

```bash
python3 -m venv .venv
```

### Step 3: Activate the Virtual Environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Upgrade pip

Ensure you have the latest version of `pip`:

```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

Install all the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Assistants

### Option 1: Webcam Assistant

Run the assistant that uses your webcam:

```bash
python webcamAssistant.py
```

### Option 2: Desktop Assistant

Run the assistant that captures your desktop:

```bash
python desktopAssistant.py
```

## Configuration

### .env File

Create a `.env` file in the root directory and add your API keys:

```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Stopping the Program

For both assistants, press the `ESC` key or `q` in the display window to quit.

## Notes

- Virtual Environment: Always activate the virtual environment before running the assistants to ensure dependencies are available
- Desktop Assistant Features: The desktop assistant takes screenshots of your screen to provide context for the AI assistant
- Webcam Assistant Features: The webcam assistant uses live video feed from your webcam to interact with the AI assistant

## Troubleshooting

- Audio Issues: Ensure your microphone and speakers are configured correctly for speech recognition and TTS (Text-to-Speech)
- Dependency Issues: If you encounter errors while installing packages, ensure you're inside the virtual environment and using Python 3.7 or later
- PortAudio on macOS: If `pyaudio` fails to install, ensure `portaudio` is installed via Homebrew (`brew install portaudio`)

## Contributing

Feel free to fork this repository, open issues, or submit pull requests to improve the assistants or add new features.

## License

This project is licensed under the MIT License.