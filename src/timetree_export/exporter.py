"""Export TimeTree data to various formats."""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Union

from .models import Calendar, Event, User, ExportData

logger = logging.getLogger(__name__)


class TimeTreeExporter:
    """Export TimeTree data to various formats."""

    @staticmethod
    def export_to_csv(
        data: ExportData,
        output_path: Union[str, Path],
        calendar_id: Optional[str] = None
    ) -> Path:
        """Export events to CSV format."""
        output_path = Path(output_path)
        
        if calendar_id:
            events = [e for e in data.events if e.calendar_id == calendar_id]
            calendar_name = next(
                (c.name for c in data.calendars if c.id == calendar_id),
                "unknown"
            )
            filename = output_path / f"{calendar_name}_events.csv"
        else:
            events = data.events
            filename = output_path / "all_events.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'title', 'calendar_id', 'start_time', 
                'end_time', 'description', 'location', 'is_all_day'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for event in events:
                writer.writerow({
                    'id': event.id,
                    'title': event.title,
                    'calendar_id': event.calendar_id,
                    'start_time': event.start_time.isoformat() if event.start_time else '',
                    'end_time': event.end_time.isoformat() if event.end_time else '',
                    'description': event.description or '',
                    'location': event.location or '',
                    'is_all_day': event.is_all_day
                })
        
        logger.info(f"Exported {len(events)} events to {filename}")
        return filename

    @staticmethod
    def export_to_json(
        data: ExportData,
        output_path: Union[str, Path],
        pretty: bool = True
    ) -> Path:
        """Export data to JSON format."""
        output_path = Path(output_path)
        filename = output_path / "timetree_export.json"
        
        export_dict = {
            'calendars': [
                {
                    'id': c.id,
                    'name': c.name,
                    'color': c.color,
                    'owner_id': c.owner_id,
                    'is_public': c.is_public,
                    'description': c.description
                }
                for c in data.calendars
            ],
            'events': [
                {
                    'id': e.id,
                    'title': e.title,
                    'calendar_id': e.calendar_id,
                    'start_time': e.start_time.isoformat() if e.start_time else None,
                    'end_time': e.end_time.isoformat() if e.end_time else None,
                    'description': e.description,
                    'location': e.location,
                    'attendees': e.attendees,
                    'is_all_day': e.is_all_day
                }
                for e in data.events
            ],
            'users': [
                {
                    'id': u.id,
                    'name': u.name,
                    'email': u.email,
                    'avatar_url': u.avatar_url
                }
                for u in data.users
            ],
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(export_dict, f, indent=2, ensure_ascii=False)
            else:
                json.dump(export_dict, f, ensure_ascii=False)
        
        logger.info(f"Exported data to {filename}")
        return filename

    @staticmethod
    def export_to_ical(
        data: ExportData,
        output_path: Union[str, Path]
    ) -> Path:
        """Export events to iCalendar format."""
        output_path = Path(output_path)
        filename = output_path / "timetree_export.ics"
        
        ical_content = "BEGIN:VCALENDAR\n"
        ical_content += "VERSION:2.0\n"
        ical_content += "PRODID:-//TimeTreeExport//0.1.0//EN\n"
        
        for event in data.events:
            ical_content += "BEGIN:VEVENT\n"
            ical_content += f"UID:{event.id}\n"
            ical_content += f"SUMMARY:{event.title}\n"
            
            if event.description:
                ical_content += f"DESCRIPTION:{event.description}\n"
            if event.location:
                ical_content += f"LOCATION:{event.location}\n"
            
            if event.start_time:
                start_str = event.start_time.strftime("%Y%m%dT%H%M%S")
                ical_content += f"DTSTART:{start_str}\n"
            if event.end_time:
                end_str = event.end_time.strftime("%Y%m%dT%H%M%S")
                ical_content += f"DTEND:{end_str}\n"
            
            if event.is_all_day:
                ical_content += "X-MICROSOFT-CDO-ALLDAYEVENT:TRUE\n"
            
            ical_content += "END:VEVENT\n"
        
        ical_content += "END:VCALENDAR\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ical_content)
        
        logger.info(f"Exported {len(data.events)} events to {filename}")
        return filename
