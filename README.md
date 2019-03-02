# x-kom.pl Hot Shot Deal Scrapper

Simple script that reads the current hot shot deal from [x-kom.pl](https://www.x-kom.pl/) and posts it to Slack.

The script also writes the data to STDOUT and saves it in a CSV-formatted log file for debugging purposes.

It should be run by cron or similar software twice a day at - after the deal changes. Currently the deal changes at 10 AM and 10 PM CET