from calendar_manager import CalendarManager

def main():
    calendar_manager = CalendarManager()
    events = calendar_manager.get_events()
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

if __name__ == "__main__":
    main()
