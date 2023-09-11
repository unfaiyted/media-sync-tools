from structlog import PrintLogger
from structlog.dev import ConsoleRenderer


class CenteredConsoleRenderer(ConsoleRenderer):
    def __call__(self, _, __, event_dict):
        s = super(CenteredConsoleRenderer, self).__call__(_, __, event_dict)

        # Split the string to get the timestamp, log level, and event.
        date, time, start_log_level_segment, log_level, end_log_level_segment, event = s.split(' ', 5)
        start_log_level_segment = start_log_level_segment.strip().strip('[')
        # print(f'LOG------- {date} {time} st-> {start_log_level_segment} ll-> {log_level} , stlen=> {len(start_log_level_segment)} , ll=> {len(log_level)} , end-> {end_log_level_segment} , event-> {event}')
        # Get log level from the segment and center it within a space of 10 characters between brackets.
        log_level_centered = f"[{start_log_level_segment.strip().center(15)}"

        return f"{date} {time} {log_level_centered} {event.strip()}"

# Rest of the code remains the same...



class NamedPrintLoggerFactory(object):
    def __call__(self, name=None):
        return NamedPrintLogger(name)


class NamedPrintLogger(PrintLogger):
    def __init__(self, name=None):
        super(NamedPrintLogger, self).__init__()
        self.name = name or __name__

