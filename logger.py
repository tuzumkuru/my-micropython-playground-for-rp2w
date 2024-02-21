import time

# Define log levels
LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3

# Function to log messages
def log(message, level=LOG_LEVEL_INFO, file_path=None):
    timestamp = time.time()
    if level == LOG_LEVEL_DEBUG:
        prefix = "[DEBUG]"
    elif level == LOG_LEVEL_WARNING:
        prefix = "[WARNING]"
    elif level == LOG_LEVEL_ERROR:
        prefix = "[ERROR]"
    else:
        prefix = "[INFO]"
    
    log_line = f"{prefix} [{timestamp}]: {message}"
    print(log_line)
    
    if file_path:
        with open(file_path, 'a') as file:
            file.write(log_line + '\n')
