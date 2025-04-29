import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']

def authenticate_gmail():
    """Authenticate and return the Gmail API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def delete_old_emails(service, verbose=False):
    """Delete emails older than two years and optionally print their date and subject."""
    # Calculate the date two years ago
    two_years_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=730)).strftime('%Y/%m/%d')
    query = f"before:{two_years_ago}"

    # Initialize variables for pagination
    next_page_token = None
    total_deleted = 0

    while True:
        # Search for emails matching the query
        results = service.users().messages().list(userId='me', q=query, pageToken=next_page_token).execute()
        messages = results.get('messages', [])
        next_page_token = results.get('nextPageToken')

        if not messages:
            if total_deleted == 0:
                print("No emails found older than two years.")
            break

        print(f"Found {len(messages)} emails on this page. Deleting...")

        for message in messages:
            try:
                if verbose:
                    # Get the email details
                    msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
                    headers = msg.get('payload', {}).get('headers', [])
                    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '(No Subject)')
                    date = next((header['value'] for header in headers if header['name'] == 'Date'), '(No Date)')

                    # Print the email's date and subject if verbose mode is enabled
                    print(f"Deleting email - Date: {date}, Subject: {subject}")
                else:
                    # Print a simple message if verbose mode is disabled
                    print(f"Deleting email with ID: {message['id']}")

                # Delete the email
                service.users().messages().delete(userId='me', id=message['id']).execute()
                total_deleted += 1
            except Exception as e:
                print(f"An error occurred: {e}")

        # Break the loop if there are no more pages
        if not next_page_token:
            break

    print(f"Total emails deleted: {total_deleted}")

def main():
    """Main function to authenticate and delete old emails."""
    service = authenticate_gmail()
    # Set verbose to True or False based on your preference
    delete_old_emails(service, verbose=True)

if __name__ == '__main__':
    main()