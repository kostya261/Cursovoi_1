import os


ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOG_DIR = os.path.join(ROOT_DIR, "logs")


file_path = os.path.join(DATA_DIR, "operations.xlsx")
user_settings_file = os.path.join(ROOT_DIR, "user_settings.json")
logs_utils_file = os.path.join(LOG_DIR, "utils_logs.log")
logs_reports_file = os.path.join(LOG_DIR, "reports_logs.log")
logs_services_file = os.path.join(LOG_DIR, "services_logs.log")

print(ROOT_DIR)
print(DATA_DIR)