# AI Calendar Assistant 🤖📅

An intelligent calendar management system that allows natural language interaction with Google Calendar. Built with Streamlit, LangChain, and Google Calendar API.

## Project Structure

```
ai-calendar-agent/
├── main.py                 # Main Streamlit application
├── app/
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Core application logic
│   ├── auth_utils.py       # Google OAuth2 authentication
│   └── calendar_tools.py   # Calendar operation tools
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features ✨

- **Natural Language Processing**: Interact with your calendar using everyday language
- **Secure Authentication**: Google OAuth2 for secure access to your calendar
- **Full CRUD Operations**:
  - ✅ Create events
  - 🔍 Search events
  - ✏️ Update existing events
  - ❌ Delete events
- **Modern Web Interface**: Built with Streamlit for a responsive, user-friendly experience

## Demo 

<img width="1371" alt="image" src="https://github.com/user-attachments/assets/7bf8d352-29f8-48f1-9ee1-3cb317a20af6" />





<img width="1082" alt="image" src="https://github.com/user-attachments/assets/fa24339e-62bc-472a-81ef-5233b1cfc786" />



<img width="1371" alt="image" src="https://github.com/user-attachments/assets/2be902e5-ac9f-4b80-b6f0-a79ec8de5786" />


<img width="1256" alt="image" src="https://github.com/user-attachments/assets/794ba546-dd32-4378-9a47-247270c8b5c6" />




## Prerequisites

- Python 3.8+
- Google Cloud Platform account with Calendar API enabled
- Google OAuth 2.0 credentials

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-calendar-agent.git
   cd ai-calendar-agent
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google OAuth**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project and enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download the credentials and save as `credentials.json` in the project root

## Configuration

1. Create a `.env` file in the project root with your configuration:

   ```env

   # Cohere API Key 
   COHERE_API_KEY=your_cohere_api_key
   ```

## Running the Application

1. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Open your browser to `http://localhost:8501`

3. Click "Login with Google" to authenticate

## Usage Examples

- "What's on my calendar today?"
- "Schedule a meeting tomorrow at 2pm about project update"
- "Do I have any meetings with John next week?"
- "Cancel my 3pm meeting"
- "Move my 2pm meeting to 3pm"

## Development



### Code Formatting

```bash
black .
```

## Troubleshooting

- **Authentication Issues**: Delete `token.json` and restart the app
- **Module Not Found**: Ensure you've activated your virtual environment and installed dependencies
- **API Errors**: Check your Google Cloud Console to ensure the Calendar API is enabled

## License

MIT

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [LangChain](https://langchain.com/) for LLM integration
- [Google Calendar API](https://developers.google.com/calendar) for calendar functionality
