from ban_manager import BanManager

# Replace with your YouTube API key
API_KEY = 'YOUR_API_KEY'

# Replace with the YouTube channel ID of your channel
CHANNEL_ID = 'YOUR_CHANNEL_ID'

# Replace with the list of regular expression patterns you want to match
USERNAME_PATTERNS = ['^spammer.*$', '^hacker.*$']

# Set the number of seconds to wait between API calls
WAIT_TIME = 10

# Replace with the path and filename of the CSV file
LOG_FILE = 'ban_log.csv'

# Create an instance of the BanManager class
api = BanManager(API_KEY, CHANNEL_ID, USERNAME_PATTERNS, WAIT_TIME, LOG_FILE)

# Call the ban_users() method
api.ban_users()
