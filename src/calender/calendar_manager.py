import os
import os.path
import datetime
from datetime import timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarManager:
    def __init__(self, credentials_file='credentials.json', token_file='token.json', scopes=["https://www.googleapis.com/auth/calendar"]):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = scopes
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        service = build("calendar", "v3", credentials=creds)
        return service

    def get_events(self, time_min=None, time_max=None, max_results=10):
        """Henter hendelser fra Google Calendar innenfor et gitt tidsintervall."""
        try:
            # Formatere tidsangivelser for API-forespørsel
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])
            
            event_dict = {}
            if not events:
                print('Ingen kommende hendelser funnet.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_dict[start] = event['summary']
            return event_dict
        except HttpError as error:
            print(f'En feil oppstod: {error}')
            
            
    def show_calendar_events(self, query):
        """Viser brukerens kommende hendelser basert på en spesifikk forespørsel."""
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indikerer UTC-tid
        if query == "i dag":
            start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_today = start_of_today + timedelta(days=1)
            self.get_events(time_min=start_of_today.isoformat() + 'Z', time_max=end_of_today.isoformat() + 'Z')
        elif query == "denne uken":
            start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
            end_of_week = start_of_week + timedelta(days=7)
            self.get_events(time_min=start_of_week.isoformat() + 'Z', time_max=end_of_week.isoformat() + 'Z')
        elif query == "neste avtale":
            self.get_events(time_min=now, max_results=1)
        else:
            print("Kan ikke tolke tidsperiode fra forespørselen.")

    def create_event(self, event_details):
        # Implementasjon for å opprette en hendelse
        pass

    # Ytterligere metoder som update_event, delete_event osv.

