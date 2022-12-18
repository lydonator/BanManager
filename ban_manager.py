import time
import re
import csv

import googleapiclient.discovery
import googleapiclient.errors

class BanManager:
  def __init__(self, api_key, channel_id, patterns, wait_time, log_file):
    # Compile the regular expression patterns
    self.patterns = [re.compile(pattern) for pattern in patterns]

    # Create a YouTube API client
    self.youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Store the YouTube channel ID
    self.channel_id = channel_id

    # Set the number of seconds to wait between API calls
    self.wait_time = wait_time

    # Store the path and filename of the CSV file
    self.log_file = log_file

    # Set the field names for the CSV file
    self.field_names = ['timestamp', 'error']

  def ban_users(self):
    while True:
      errors = []

      try:
        # Retrieve the list of live chat messages
        request = self.youtube.liveChatMessages().list(
            liveChatId=self.channel_id,
            part='authorDetails'
        )
        response = request.execute()
      except googleapiclient.errors.HttpError as error:
        # Append the error to the list of errors
        errors.append(error)

      # Iterate through the list of chat messages
      for message in response['items']:
        username = message['authorDetails']['displayName']
        # Check if the username matches any of the patterns
        for pattern in self.patterns:
          if pattern.match(username):
            try:
              # Ban the user from the live chat
              self.youtube.liveChatBans().insert(
                  liveChatId=self.channel_id,
                  part='id',
                  banDurationSeconds=3600,
                  banReason='Spamming'
              ).execute()
            except googleapiclient.errors.HttpError as error:
              # Append the error to the list of errors
              errors.append(error)
            # Exit the loop
            break

      # Check if there are any errors to log
      if errors:
        # Log the errors to the CSV file
        with open(self.log_file, 'a', newline='') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
          for error in errors:
            writer.writerow({
                'timestamp': time.time(),
                'error': error
            })

      # Wait for the specified number of seconds before making the next API call
      time.sleep(self.wait_time)

