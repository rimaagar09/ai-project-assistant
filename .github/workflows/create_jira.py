name: Create Jira Tickets from JSON

on:
  push:
    paths:
      - 'jira_tickets.json'

jobs:
  create-jira:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: pip install requests

      - name: Run Jira Script
        env:
          JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
          JIRA_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
          JIRA_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_ASSIGNEE_ID: ${{ secrets.JIRA_ASSIGNEE_ID }}
        run: python create_jira.py
