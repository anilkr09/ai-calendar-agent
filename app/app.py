# app.py
import os
import sys
from pprint import pprint

from datetime import datetime
from dotenv import load_dotenv
from langchain_google_community.calendar.utils import build_resource_service
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from typing import Dict, Any

from app.auth_utils import get_credentials, logout as auth_logout, is_logged_in
from app.calendar_tools import (
    create_calendar_event,
    search_calendar_events,
    update_calendar_event,
    delete_calendar_event,
    get_calendars_info,
    get_current_datetime
)

class CalendarAgent:
    def __init__(self):
        """Initialize the Calendar Agent with required tools and LLM."""
        # Load environment variables
        load_dotenv()
        
        # Initialize LLM
        if not os.environ.get("COHERE_API_KEY"):
            os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY", "")
        
        # Import required modules here to avoid circular imports
        from langchain.chat_models import init_chat_model
        from langgraph.prebuilt import create_react_agent
        
        # Initialize LLM
        self.llm = init_chat_model("command-r-plus", model_provider="cohere")
        
        # Initialize tools
        self.tools = [
            search_calendar_events,
            create_calendar_event,
            update_calendar_event,
            delete_calendar_event,
            get_calendars_info,
            get_current_datetime
        ]
       
       
            
        def custom_instructions_hook(state):
            # Add a system instruction only once
            messages = state.get("messages", [])
            if not any("Important formatting rules" in m.content for m in messages):
                messages = messages + [HumanMessage(content="Important formatting rules:\n- Use format '%Y-%m-%d %H:%M:%S' , if event max_datetime not provided take it 1 hour after min_datetime.\n- ")]
            return {"messages": messages}

        self.agent_executor = create_react_agent(
            model=self.llm,
            tools=self.tools,
            pre_model_hook=RunnableLambda(custom_instructions_hook),
           
        )
    
    def process_message(self, query: str) -> str:
        """
        Process a user query and return the AI's response.
        
        Args:
            query: The user's query string
            
        Returns:
            str: The AI's response
        """
        # Get current datetime for context
        now_str = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
        try:
            # Initialize messages list
            all_messages = []
            
            # Stream the response
            for chunk in self.agent_executor.stream(
                {"messages": [
                    HumanMessage(content=f"current datetime is {now_str}"),
                    HumanMessage(content=query)
                ]},
                stream_mode="values"
            ):
                if isinstance(chunk, dict) and "messages" in chunk:
                    all_messages = chunk["messages"]
            
            # Extract AI messages from the final state
            ai_messages = [
                msg.content for msg in all_messages 
                if isinstance(msg, AIMessage) and 
                not msg.additional_kwargs.get("finish_reason") == "TOOL_CALL"
            ]
            
            
        # Return the last complete response
            return ai_messages[-1] if ai_messages else "I couldn't generate a response. Please try again."
    
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return "An error occurred while processing your request."
        # Process the query
        # response = self.agent_executor.stream(
        #     {"messages": [
        #         ("user", "current datetime is " + now_str),
        #         ("user", query)
        #     ]},
        #     stream_mode="values",
        # )
        # # Extract and return the AI's response
        # streamed_outputs = response["messages"]
        # ai_messages = [msg for msg in streamed_outputs if isinstance(msg, AIMessage)]
    
        # if ai_messages:
        #     return ai_messages[-1].content
        # return "I couldn't generate a response. Please try again."
