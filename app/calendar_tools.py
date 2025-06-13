from langchain_core.tools import tool
from langchain_google_community.calendar.create_event import CalendarCreateEvent
from langchain_google_community.calendar.search_events import CalendarSearchEvents
from langchain_google_community.calendar.update_event import CalendarUpdateEvent
from langchain_google_community.calendar.delete_event import CalendarDeleteEvent
from langchain_google_community.calendar.get_calendars_info import GetCalendarsInfo
from langchain_google_community.calendar.current_datetime import GetCurrentDatetime
from datetime import datetime
from typing import Optional, Dict, List, Any
from config.logger_config import setup_logger
from app.auth_utils import get_credentials, logout as auth_logout, is_logged_in
from langchain_google_community.calendar.utils import (
    build_resource_service,
)


# Set up logger
logger = setup_logger(__name__)


# Initialize credentials at module level
credentials = get_credentials()

api_resource = build_resource_service(credentials=credentials)

@tool
def create_calendar_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    timezone: str = "UTC",
    calendar_id: str = "primary",
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    color_id: Optional[str] = None,
    conference_data: Optional[bool] = None,
    recurrence: Optional[Dict[str, Any]] = None,
    reminders: Optional[Dict[str, Any]] = None,
    transparency: Optional[str] = None
) -> Dict:
    """Create a new event in Google Calendar.

    Args:
        summary: The title of the event.
        start_datetime: The start datetime for the event in 'YYYY-MM-DD HH:MM:SS' format.
                      If the event is an all-day event, set the time to 'YYYY-MM-DD' format.
        end_datetime: The end datetime for the event in 'YYYY-MM-DD HH:MM:SS' format.
                     If the event is an all-day event, set the time to 'YYYY-MM-DD' format.
        timezone: The timezone of the event (default: "UTC").
        calendar_id: The calendar ID to create the event in (default: "primary").
        description: The description of the event.
        location: The location of the event.
        attendees: A list of attendees' email addresses for the event.
        color_id: The color ID of the event. '1': Lavender, '2': Sage, '3': Grape, etc.
        conference_data: Whether to include conference data.
        recurrence: The recurrence of the event. Format: 
                  {'FREQ': <'DAILY' or 'WEEKLY'>, 'INTERVAL': <number>, 
                   'COUNT': <number or None>, 'UNTIL': <'YYYYMMDD' or None>, 
                   'BYDAY': <'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU' or None>}.
        reminders: Reminders for the event. Set to True for default reminders, or 
                 provide a list like [{'method': 'email', 'minutes': <minutes>}, ...].
                 Valid methods are 'email' and 'popup'.
        transparency: User availability for the event: 'transparent' for available, 
                    'opaque' for busy.

    Returns:
        Dict: Created event details.
    """
    logger.info(f"Creating calendar event: {summary}")
    try:
        toolkit = CalendarCreateEvent(api_resource=api_resource)
        result = toolkit.invoke({
            "calendar_id": calendar_id,
            "summary": summary,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "timezone": timezone,
            "description": description,
            "location": location,
            "attendees": attendees,
            "color_id": color_id,
            "conference_data": conference_data,
            "recurrence": recurrence,
            "reminders": reminders,
            "transparency": transparency
        })
        logger.info(f"Successfully created event with ID: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        raise

@tool
def search_calendar_events(
    min_datetime: str,
    max_datetime: str,
    query: Optional[str] = None,
    max_results: int = 10,
    order_by: str = 'startTime',
    single_events: bool = True
) -> List[Dict]:
    """Search for events in Google Calendar.

    Args:
        min_datetime: The start datetime for the events in 'YYYY-MM-DD HH:MM:SS' format.
        max_datetime: The end datetime for the events search in 'YYYY-MM-DD HH:MM:SS' format.
        query: Free text search terms to find events that match these terms in 
              summary, description, location, attendee's displayName, etc.
        max_results: The maximum number of results to return (default: 10).
        order_by: The order of the events, either 'startTime' or 'updated' (default: 'startTime').
        single_events: Whether to expand recurring events into instances and only return 
                     single one-off events and instances of recurring events (default: True).

    Returns:
        List[Dict]: List of matching calendar events with their details.
    """
    logger.info(f"Searching calendar events from {min_datetime} to {max_datetime}")
    try:
        # Get calendars info first
        calendars_info_tool = GetCalendarsInfo(api_resource=api_resource)
        calendars_info = calendars_info_tool.invoke({})
        
        toolkit = CalendarSearchEvents(api_resource=api_resource)
        result = toolkit.invoke({
            "min_datetime": min_datetime,
            "max_datetime": max_datetime,
            "calendars_info": str(calendars_info),  # Convert to string as expected
            "query": query,
            "max_results": max_results,
            "order_by": order_by,
            "single_events": single_events
        })
        logger.info(f"Found {len(result) if result else 0} events")
        return result
    except Exception as e:
        logger.error(f"Error searching calendar events: {str(e)}")
        raise ValueError(f"Invalid datetime format. Expected 'YYYY-MM-DD HH:MM:SS': {str(e)}")
    
    # Validate order_by parameter
    if order_by not in ['startTime', 'updated']:
        raise ValueError("order_by must be either 'startTime' or 'updated'")

@tool
def update_calendar_event(
    event_id: str,
    calendar_id: str = "primary",
    summary: Optional[str] = None,
    start_datetime: Optional[str] = None,
    end_datetime: Optional[str] = None,
    timezone: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    color_id: Optional[str] = None,
    conference_data: Optional[bool] = None,
    recurrence: Optional[Dict[str, Any]] = None,
    reminders: Optional[Dict[str, Any]] = None,
    send_updates: Optional[str] = None,
    transparency: Optional[str] = None
) -> Dict:
    """Update an existing event in Google Calendar.

    Args:
        event_id: The event ID to update.
        calendar_id: The calendar ID containing the event (default: "primary").
        summary: The new title of the event.
        start_datetime: The new start datetime for the event in 'YYYY-MM-DD HH:MM:SS' format.
        end_datetime: The new end datetime for the event in 'YYYY-MM-DD HH:MM:SS' format.
        timezone: The new timezone of the event.
        description: The new description of the event.
        location: The new location of the event.
        attendees: A new list of attendees' email addresses for the event.
        color_id: The new color ID of the event.
        conference_data: Whether to include conference data.
        recurrence: The new recurrence rules for the event.
        reminders: The new reminders for the event.
        send_updates: Whether to send updates to attendees ('all', 'externalOnly', or 'none').
        transparency: The new user availability for the event ('transparent' or 'opaque').

    Returns:
        Dict: Updated event details.
    """
    logger.info(f"Updating calendar event {event_id}")
    try:
        toolkit = CalendarUpdateEvent(api_resource=api_resource)
        update_data = {
            "event_id": event_id,
            "calendar_id": calendar_id
        }
        
        # Only include fields that are provided
        if summary is not None:
            update_data["summary"] = summary
        if start_datetime is not None:
            update_data["start_datetime"] = start_datetime
        if end_datetime is not None:
            update_data["end_datetime"] = end_datetime
        if timezone is not None:
            update_data["timezone"] = timezone
        if description is not None:
            update_data["description"] = description
        if location is not None:
            update_data["location"] = location
        if attendees is not None:
            update_data["attendees"] = attendees
        if color_id is not None:
            update_data["color_id"] = color_id
        if conference_data is not None:
            update_data["conference_data"] = conference_data
        if recurrence is not None:
            update_data["recurrence"] = recurrence
        if reminders is not None:
            update_data["reminders"] = reminders
        if send_updates is not None:
            update_data["send_updates"] = send_updates
        if transparency is not None:
            update_data["transparency"] = transparency
            
        result = toolkit.invoke(update_data)
        logger.info(f"Successfully updated event {event_id}")
        return result
    except Exception as e:
        logger.error(f"Error updating calendar event: {str(e)}")
        raise

@tool
def delete_calendar_event(
    event_id: str, 
    calendar_id: str = "primary", 
    send_updates: Optional[str] = None
) -> Dict:
    """Delete an event from Google Calendar.

    Args:
        event_id: The event ID to delete.
        calendar_id: The calendar ID containing the event (default: "primary").
        send_updates: Whether to send updates to attendees ('all', 'externalOnly', or 'none').

    Returns:
        Dict: Confirmation message or success status.
    """
    logger.info(f"Deleting calendar event {event_id}")
    try:
        toolkit = CalendarDeleteEvent(api_resource=api_resource)
        delete_data = {
            "event_id": event_id,
            "calendar_id": calendar_id
        }
        
        if send_updates is not None:
            delete_data["send_updates"] = send_updates
            
        result = toolkit.invoke(delete_data)
        logger.info(f"Successfully deleted event {event_id}")
        return result
    except Exception as e:
        logger.error(f"Error deleting calendar event: {str(e)}")
        raise

@tool
def get_calendars_info(calendar_id: Optional[str] = None) -> Dict:
    """Retrieve information about available Google Calendars.

    Args:
        calendar_id: Optional specific calendar ID to get info for.
                    If not provided, returns all calendars.

    Returns:
        Dict: Calendar information with fields:
            - id: Calendar ID
            - summary: Calendar name/title
            - timeZone: Calendar timezone
            - accessRole: User's access role for the calendar
    """
    logger.info("Fetching calendar information")
    try:
        toolkit = GetCalendarsInfo(api_resource=api_resource)
        result = toolkit.invoke({"calendar_id": calendar_id} if calendar_id else {})
        
        # If a specific calendar was requested, ensure we return a list for consistency
        if calendar_id and isinstance(result, dict):
            result = [result]
            
        logger.info(f"Found {len(result) if isinstance(result, list) else 1} calendars")
        return result
    except Exception as e:
        logger.error(f"Error fetching calendar information: {str(e)}")
        raise

@tool
def get_current_datetime(calendar_id: str = "primary") -> str:
    """Get current datetime according to calendar timezone.

    Args:
        calendar_id: The calendar ID to get timezone from (default: "primary").

    Returns:
        str: String with timezone and current datetime in format:
            "Time zone: {timezone}, Date and time: {YYYY-MM-DD HH:MM:SS}"
    """
    logger.info(f"Getting current datetime for calendar {calendar_id}")
    try:
        toolkit = GetCurrentDatetime(api_resource=api_resource)
        result = toolkit.invoke({"calendar_id": calendar_id})
        logger.info(f"Current datetime: {result}")
        return result
    except Exception as e:
        logger.error(f"Error getting current datetime: {str(e)}")
        raise
