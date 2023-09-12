import copy
from structlog import PrintLogger
from structlog.dev import ConsoleRenderer

from src.models import ConfigClientFieldsValue

class CenteredConsoleRenderer(ConsoleRenderer):
    def __call__(self, _, __, event_dict):
        s = super(CenteredConsoleRenderer, self).__call__(_, __, event_dict)

        # Split the string to get the timestamp, log level, and event.
        date, time, start_log_level_segment, log_level, end_log_level_segment, event = s.split(' ', 5)
        start_log_level_segment = start_log_level_segment.strip().strip('[')
        # print(f'LOG------- {date} {time} st-> {start_log_level_segment} ll-> {log_level} , stlen=> {len(start_log_level_segment)} , ll=> {len(log_level)} , end-> {end_log_level_segment} , event-> {event}')
        # Get log level from the segment and center it within a space of 10 characters between brackets.
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
    REDACTED_KEYS = ["api_key", "password",'apikey']

    def recursive_redact(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key in REDACTED_KEYS:
                    data[key] = "[REDACTED]"
                else:
                    recursive_redact(value)
        elif isinstance(data, list):
            for item in data:
                recursive_redact(item)

    # Make a deep copy of event_dict and then modify that
    event_copy = copy.deepcopy(event_dict)
    recursive_redact(event_copy)
    return event_copy


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


