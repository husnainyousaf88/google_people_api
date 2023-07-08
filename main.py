import csv
import os
import pickle
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes required for accessing Google contacts
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

# Define the path to the token file
TOKEN_FILE = 'token.pickle'


def write_to_csv(data):
    file_name = f" output- {str(datetime.now())}.csv"
    # Open the CSV file in 'append' mode and create a CSV writer
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write each tuple as a new row
        for item in data:
            writer.writerow(item)


def authenticate():
    """Authenticate with Google API using OAuth 2.0"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials_1.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_all_contacts(service):
    contacts = []
    page_token = None

    while True:
        # Fetch the user's contacts
        results = service.people().connections().list(
            pageSize=1000,
            sources=['READ_SOURCE_TYPE_CONTACT', 'READ_SOURCE_TYPE_PROFILE'],
            resourceName='people/me',
            pageToken=page_token,
            personFields='names,emailAddresses,phoneNumbers,photos').execute()

        connections = results.get('connections', [])
        contacts.extend(connections)

        page_token = results.get('nextPageToken')
        print(page_token)
        print(len(contacts))

        if not page_token:
            break

    return contacts


def fetch_contacts():
    """Fetch the user's Google contacts"""
    result = []
    creds = authenticate()
    service = build('people', 'v1', credentials=creds)

    connections = get_all_contacts(service)

    if not connections:
        print('No contacts found.')
    else:
        print('Contacts:')
        for person in connections:
            row = []
            names = person.get('names', [])
            name = None
            if names:
                name = names[0].get('displayName')
                row.append(name)

            email_addresses = person.get('emailAddresses', [])
            if email_addresses:
                if email_addresses == "05moyes@sbcglobal.net":
                    print('sdf')
                email = email_addresses[0].get('value')
                if name is None or len(names) < 1:
                    row.append(email)
                row.append(email)

            photos = person.get('photos', [])
            if len(photos) > 1 and photos[0]['metadata']['source']['type'] == "PROFILE":
                print(photos)
                print(email)
                row.append("Google Profile Photo")
            else:
                row.append("NA")

            # print(row)
            result.append(row)

        write_to_csv(result)


if __name__ == '__main__':
    fetch_contacts()
