import json
import pandas as pd
from datetime import datetime

class ActivityLogger:
    """
    Logs USB activity, threats, and user actions.
    Supports export to PDF, Excel, and JSON formats.
    """
    def __init__(self):
        self.logs = []

    def log_event(self, event_type, details):
        """Log an event with type and details."""
        entry = {
            'type': event_type,
            'details': details,
            'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')
        }
        self.logs.append(entry)

    def export_logs(self, format='json', filename='activity_log'):
        """Export logs in the specified format (excel, json)."""
        if format == 'json':
            with open(f'{filename}.json', 'w') as f:
                json.dump(self.logs, f, indent=2)
            return f'{filename}.json'
        elif format == 'excel':
            df = pd.DataFrame(self.logs)
            df.to_excel(f'{filename}.xlsx', index=False)
            return f'{filename}.xlsx'
        else:
            raise ValueError('Unsupported format')
