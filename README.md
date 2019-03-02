# x-kom.pl Hot Shot Deal Scrapper

Module `XKomProcessor` contains logic for reading the current hot shot deal from [x-kom.pl](https://www.x-kom.pl/) and posting it to Slack.
Module expects Slack token and channel name to be passed to it as script parameters.

Script `xks` reads parameters from environment variables and uses XKomProcessor module to process [x-kom.pl](https://www.x-kom.pl/) as described above. 

Both the module and the script save the data read from the website in a CSV-formatted log file. In debug mode the data is also written to STDOUT.

In production script (or module) should be run by CRON or similar software twice a day at - after the deal changes. Currently the deal changes at 10 AM and 10 PM CET.
CRON configuration example (runs the script one minute after the new deal is posted): `01 10,22 * * * python3 -O /path/to/xks.py`