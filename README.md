# Mail Killer

## Description

Mail Killer is a small script that can delete emails in your Gmail account. It uses the Gmail API to authenticate and delete emails based on a specified query. The script is designed to be run from the command line.   There are many paid services that will help you clean up your Gmail account and if you end up with too much email google will offer to charge you.  I chose to just purge old emails with a script which cost me nothing.

This first version is super simple, it deletes all emails in the inbox older than 2 years.  Thats what I needed at the time.  I may update it to allow for more complex queries in the future.  White lists of labels or senders I never want to delete.  If you end up needing that I accept pull requests.  :)

## Requirements

- Python 3.x
- Python Virtual Environment (optional but recommended)
- Gmail API credentials (see [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/python) for instructions on how to set this up)

## Installation

First install python 3.X then create a virtual environment and install the required packages.

```shell
python3.12 -m venv venv
source venv/bin/activate
pip --isolated install --upgrade pip
pip --isolated install -r requirements.txt
```

You will need your own `credentials.json` file from the Gmail API. You can get this by following the instructions in the [Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/python). Place the `credentials.json` file in the same directory as the script.  You will need to ensure that the scopes '<https://www.googleapis.com/auth/gmail.modify>', '<https://mail.google.com/>' are enabled for your Application.

In most cases when you create a new project in the Google Cloud Console, the scopes are enabled by default.  However you will need to enable the scopes and add any users you want to use the application.  You can do this by going to the Google Cloud Console, selecting your project, and then going to the "OAuth consent screen" tab.  From there you can add any users you want to use the application.  You will also need to enable the Gmail API for your project.  You can do this by going to the Google Cloud Console, selecting your project, and then going to the "APIs & Services" tab.  From there you can search for the Gmail API and enable it.
