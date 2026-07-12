import os

# ---- Cities to search ----
CITIES = ["Bangalore", "Chennai", "Trivandrum", "Coimbatore"]

# ---- Category 1: Manual Tester (primary) + Software Developer, 0-6 yrs ----
EXPERIENCED_KEYWORDS = [
    "Manual Tester",
    "Manual Testing",
    "QA Engineer",
    "Software Developer",
    "Software Engineer",
]

# ---- Category 2: Fresher jobs, any IT domain ----
FRESHER_KEYWORDS = [
    "Fresher IT",
    "Graduate Engineer Trainee",
    "Trainee Software Engineer",
    "Associate Software Engineer",
    "Entry Level Software",
]

# Max job listings shown per generated image
MAX_JOBS_PER_IMAGE = 6

# Only show jobs from companies in companies.py WHITELISTED_COMPANIES list
FILTER_BY_WHITELIST = True

# ---- Telegram (values come from GitHub Secrets, not stored here) ----
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
