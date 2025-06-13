from setuptools import setup, find_packages

setup(
    name="ai_calendar_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langgraph",
        "langchain_google_community",
        "langchain_cohere",
        "streamlit>=1.30.0",
        "google-auth-oauthlib",
        "python-dotenv",
    ],
    python_requires=">=3.8",
)