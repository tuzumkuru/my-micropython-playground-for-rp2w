import time
import os

# Define log levels
LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3

LOG_FILE_MAX_SIZE = 1024  # 1KB for example, adjust as needed
LOG_FILE_BACKUP_COUNT = 2  # Number of backup files to keep

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
        # Rotate log file if it's too large
        try:
            file_size = os.stat(file_path)[6]
            if file_size > LOG_FILE_MAX_SIZE:
                # Delete the oldest backup if it exists
                oldest_backup = f"{file_path}.{LOG_FILE_BACKUP_COUNT}"
                try:
                    os.remove(oldest_backup)
                except OSError:
                    pass

                # Shift the backup files
                for i in range(LOG_FILE_BACKUP_COUNT - 1, 0, -1):
                    source = f"{file_path}.{i}"
                    destination = f"{file_path}.{i + 1}"
                    try:
                        os.rename(source, destination)
                    except OSError:
                        pass

                # Rename the current log file to the first backup
                try:
                    os.rename(file_path, file_path + ".1")
                except OSError:
                    pass

        except OSError:
            # File doesn't exist yet
            pass

        with open(file_path, 'a') as file:
            file.write(log_line + '\n')
