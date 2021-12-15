# Niche Notifier
Scrap niche allocation site and send email on row and column info
https://vgoffice.catholic.org.hk/cemetery/niche_eng.aspx

Email Example
![email example](assets/email-sample.png)
The time in the email content is in HKT.
The code is set to get the row and column info for `Holy Cross Catholic Cemetery（Chai Wan）- Standard Niche`. You could change it.

## How to use

First, clone the repo.

### Install dependencies
Install following python 3 packages gloablly with `pip3 install <package_name>`
- requests
- bs4
- pytz

### Get Sendgrid API key

Follow the sendgrid documentation to create an api key
https://docs.sendgrid.com/ui/account-and-settings/api-keys

Do `cp config.py.example config.py`

Paste in the api key.

### Set your sender and receiver email

Sender email at
[line 62](https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L62) and [line 66](https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L66)
Receiver email at [line 57](https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L57)

### Set Cemetry Location (optional)
It is set to `Holy Cross Catholic Cemetery（Chai Wan）- Standard Niche` currently. 

Inspect the webpage, and get the corresponding span id for each box (morning row and column, evening row and column)
morning row: https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L30
morning column: https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L31

evening row: https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L43
evening column: https://github.com/agathanatasha/niche-notifier/blob/main/niche-notifier.py#L43

### Create a log file
You could create the log file wherever you want. I created my in the same directory.

### set up cron job
`crontab -e`
set cron time based on local time
The information updates Monday to Saturday at noon and 4:30pm HKT. Adjust your cron job timing based on your server's timezone. The 4:30pm updates are usually late from my experience.

e.g. EST server where cron job runs at 0004 and 0523.  That's why I set it to 5:23pm.
```bash
5 23 * * * python3 <path/to/niche-notifier.py> >> <path/to/log_file.log> 2>&1
0 4 * * * python3 <path/to/niche-notifier.py> >> <path/to/log_file.log> 2>&1
```
