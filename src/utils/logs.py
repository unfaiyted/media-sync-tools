import copy
from structlog import PrintLogger
from structlog.dev import ConsoleRenderer
import copy
import _thread
from src.models import ConfigClientFieldsValue

class CenteredConsoleRenderer(ConsoleRenderer):
    def __call__(self, _, __, event_dict):
        s = super(CenteredConsoleRenderer, self).__call__(_, __, event_dict)

        # Split the string to get the timestamp, log level, and event.
        date, time, start_log_level_segment, log_level, end_log_level_segment, event = s.split(' ', 5)
        start_log_level_segment = start_log_level_segment.strip().strip('[')
        # Get log level from the segment and center it within a space of 17 characters between brackets.
        log_level_centered = f"[{start_log_level_segment.strip().center(17)}"
        return f"{date} {time} {log_level_centered} {event.strip()}"


class NamedPrintLoggerFactory(object):
    def __call__(self, name=None):
        return NamedPrintLogger(name)


class NamedPrintLogger(PrintLogger):
    def __init__(self, name=None):
        super(NamedPrintLogger, self).__init__()
        self.name = name or __name__


def redact_keys_based_on_name(_, __, event_dict):
    REDACTED_KEYS = ["api_key", "password", 'apikey', 'bearer_token', 'client_secret', 'access_token', 'refresh_token']
    MAX_DEPTH = 5

    def manual_deepcopy(data):
        if isinstance(data, dict):
            return {key: manual_deepcopy(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [manual_deepcopy(item) for item in data]
        return data

    def recursive_redact(data, current_depth=0):
        if current_depth == MAX_DEPTH:
            return data

        if isinstance(data, dict):
            new_data = {}
            for key, value in manual_deepcopy(data).items():
                if isinstance(value, _thread.LockType):
                    continue

                if key in REDACTED_KEYS:
                    new_data[key] = "[REDACTED]"
                else:
                    new_data[key] = recursive_redact(value, current_depth + 1)
            return new_data

        elif isinstance(data, list):
            return [recursive_redact(item, current_depth + 1) for item in data if not isinstance(item, _thread.LockType)]

        elif hasattr(data, '__dict__') and not isinstance(data, type):
            new_obj = data  # Shallow copy (this won't change as we're avoiding deepcopy)
            for key, value in new_obj.__dict__.items():
                if key in REDACTED_KEYS:
                    setattr(new_obj, key, "[REDACTED]")
                else:
                    setattr(new_obj, key, recursive_redact(value, current_depth + 1))
            return new_obj

        return data

    return recursive_redact(manual_deepcopy(event_dict))  # start with a manual deep copy



def redact_sensitive_data(logger, log_method, event_dict):
    # The keys we're interested in deep copying and potentially redacting
    sensitive_keys = ["event"]

    # Only deep copy the keys of interest
    copied_data = {k: copy.deepcopy(v) for k, v in event_dict.items() if k in sensitive_keys}

    if isinstance(copied_data.get("event"), ConfigClientFieldsValue):
        # Redact the value in the copy
        copied_data["event"].value = "[REDACTED]"

    # Merge the redacted copy back into the original event_dict
    event_dict.update(copied_data)
    return event_dict


