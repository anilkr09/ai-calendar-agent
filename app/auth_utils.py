# app/auth_utils.py
import os
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config.logger_config import setup_logger

# Set up logger
logger = setup_logger(__name__)

# OAuth2 scopes for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "../credentials.json"
REDIRECT_URI = "http://localhost:8080/callback"

import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]  # Full access to manage calendar

def get_credentials() -> Credentials:
    """Get and refresh Google Calendar credentials.
    
    Returns:
        Credentials: Valid Google Calendar credentials
    """
    logger.info("Getting Calendar credentials")
    creds = None
    if os.path.exists("token.json"):
        logger.debug("Loading existing credentials from token.json")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired credentials")
            creds.refresh(Request())
        else:
            logger.info("Getting new credentials")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        logger.debug("Saving credentials to token.json")
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def is_logged_in() -> bool:
    """Check if user is authenticated with valid credentials."""
    logger.debug("Checking authentication status")
    if not os.path.exists("token.json"):
        logger.info("No token.json file found - user not authenticated")
        return False
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        is_valid = creds and creds.valid
        logger.info(f"Authentication status: {'valid' if is_valid else 'invalid'}")
        return is_valid
    except Exception as e:
        logger.error(f"Error checking authentication status: {str(e)}")
        return False

def logout() -> bool:
    """Remove the token.json file to logout the user."""
    logger.info("Attempting to logout user")
    if os.path.exists("token.json"):
        try:
            os.remove("token.json")
            logger.info("User logged out successfully")
            return True
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return False
    logger.info("No token.json file found - user already logged out")
    return False

# def get_auth_url() -> str:
#     """Generate the authorization URL for Google OAuth2."""
#     flow = InstalledAppFlow.from_client_secrets_file(
#         CREDENTIALS_FILE,
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI
#     )
#     auth_url, _ = flow.authorization_url(
#         access_type='offline',
#         prompt='consent'
#     )
#     return auth_url

# def get_credentials() -> Optional[Credentials]:
#     """Get or refresh Google OAuth2 credentials."""
#     creds = None
    
#     # Try to load existing token
#     if os.path.exists(TOKEN_FILE):
#         creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
#     # Refresh or get new credentials if needed
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             auth_url = get_auth_url()
#             print("\nPlease visit this URL to authorize the application:")
#             print(auth_url)
#             webbrowser.open(auth_url)
#             print("\nAfter authorizing, you'll be redirected to localhost.")
#             print("Please copy the full URL you're redirected to and paste it below.")
#             auth_response = input("Paste the full redirect URL here: ")
            
#             # Extract the authorization code from the redirect URL
#             from urllib.parse import urlparse, parse_qs
#             query = urlparse(auth_response).query
#             code = parse_qs(query).get('code')
            
#             if not code:
#                 print("Error: Could not extract authorization code from the URL.")
#                 return None
                
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 CREDENTIALS_FILE,
#                 scopes=SCOPES,
#                 redirect_uri=REDIRECT_URI
#             )
#             flow.fetch_token(code=code[0])
#             creds = flow.credentials
            
#             # Save the credentials for the next run
#             with open(TOKEN_FILE, 'w') as token:
#                 token.write(creds.to_json())
    
#     return creds

# def logout() -> bool:
#     """Logout by removing the token file."""
#     try:
#         if os.path.exists(TOKEN_FILE):
#             os.remove(TOKEN_FILE)
#             return True
#     except Exception as e:
#         print(f"Error during logout: {str(e)}")
#     return False

# def is_logged_in() -> bool:
#     """Check if user is logged in by checking for valid token."""
#     if not os.path.exists(TOKEN_FILE):
#         return False
    
#     try:
#         creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
#         return creds and creds.valid
#     except Exception:
#         return False