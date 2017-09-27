# ip-reputation-monitoring #

[![Build Status](https://travis-ci.org/ovh/ip-reputation-monitoring.svg)](https://travis-ci.org/ovh/ip-reputation-monitoring)
[![Coverage Status](https://coveralls.io/repos/github/ovh/ip-reputation-monitoring/badge.svg)](https://coveralls.io/github/ovh/ip-reputation-monitoring)

## Summary ##

This tool aims to monitor the reputation of a network in order
to easily detect blacklisted IPs or IPs sending suspicious e-mails.
Every day an e-mail is sent telling you the 10th IPs having the
worst reputation among the network.

The monitoring is based over both RBL and FBL as described below.

An API is provided in order to query the reputation of a single
IP using RBL and FBL aggregation. The API also offers an endpoint
that checks DNS black list.

### RBL ###

A Realtime Blackhole List is composed of IP addresses considered as
spammers. Several organizations are maintaining such list and this tool
supports some of them: Microsoft SNDS, BlockList, CleanTalk, StopForumSpam.

Generally, those lists are released under CSV format. Unfortunately,
CleanTalk does only release this list in HTML, so a HTML to CSV
parser has been written to do so.

### FBL ###

A feedback loop is a realtime feedback about mails sent from observed
network. Those mails can be sent by e-mail hosting providers or by
foundations fighting against spams in order to give a feedback about
suspicious mails issued from the network.
The tool supports Abuse Reporting Format (ARF) which is a standard
to report suspicious mails used by AOL and SignalSpam feedbacks.

SpamCop feedbacks are also supported by the tool, even if their mails
do not follows ARF guidelines.

### DNS BL ###

The DNS-based blackhole list is a subset of RBL and, instead of being a
CSV file containing an IP list, is a software mechanism allowing anyone
to query the database using the DNS protocol whether an IP is blacklist.

Supported DNS BL are the following:
 - Abuse combined
 - Abuseat
 - Msrbl
 - Sorbs
 - Spamhaus ZEN
 - SpamCop
 - UCE Protect
 - Wpbl

### Spamhaus BL ###

Spamhaus is an organization tracking spam over Internet. Their website
provides an easy way to keep an eye over active issues on a network giving
the domain responsible of an IP set.

This tool provides a script able to parse the issues raised by Spamhaus to
track network reputation.

## Installation ##

### Important note ###

As you can see, `ip-reputation-monitoring` supports various way to monitor your IPs.
Feel free to use only one of them if you don't need everything.
If you think you don't need all the different ways to monitor your IPs (RBL, FBL, DNS BL), you might not need every single steps in the following installation.

### Requirements ###

To setup this little tool, you'll need:

 * A Linux environment (it might work under Windows but you'll need to rewrite
 shell scripts)
 * Python 3
 * Packages `python3-dev` and `python3-pip`
 * A MongoDB database (2.6.x or greater with TLS support*)
 * A PostgreSQL database (9.2+ or greater or greater with TLS support*)
 * A MX supporting IMAPS
 * A scheduler (cron, supervisor, ...)

*TLS support can be disabled by editing `settings/config.py`.

### Step by step ###

When all of these requirements are met, you can install the tool:

 1. Download the zipfile or checkout the sources.
 2. Install python dependencies (apt-get install python3-dev python3-pip)
 3. Run `make install-deps`.
 4. Install MongoDB, add a DB and an user:
    ```bash
    sudo apt-get install mongodb
    db
    use db_name
    db.addUser('user', 'password')
    ```

## Configuration ##

### General settings ###

For security purpose, most of setting values must be defined as VARENV.
So, to configure the tool, you just have to export following environment
variables:

 * `AS_NUMBER`: your AS number, i.e.: OVH one is 16276
 * `EMAIL_HOST`: ip or domain of your MX
 * `FBL_USER`: username used to poll incoming e-mails
 * `FBL_PASSWORD`: password for previous username
 * `FBL_PARTNER_HEADER`: Name of the header defining e-mail source (see next
 section)
 * `POSTGRES_HOST`: ip or domain of your PostgreSQL DB host
 * `POSTGRES_PORT`: port to reach PostgreSQL
 * `POSTGRES_DB_NAME`: name of the PostgreSQL database
 * `POSTGRES_USER`: PostgreSQL user
 * `POSTGRES_PASSWORD`: PostgreSQL password
 * `MONGO_HOST`: ip or domain of your MongoDB host
 * `MONGO_PORT`: port to reach MongoDB
 * `MONGO_DB_NAME`: name of the Mongo database
 * `MONGO_USER`: MongoDB user
 * `MONGO_PASSWORD`: MongoDB password
 * `REPORTING_TARGET`: e-mail address where a daily report about ips with the
 worst reputation must be sent
 * `REPORTING_SENDER`: `From:` header value of the dail report e-mail
 * `SNDS_KEY`: your personal SNDS key
 * `SPAMHAUS_DOMAIN_NAME`: the domain your IPs are attached to, i.e.: OVH one
 is `ovh.net`

### Tagging incoming e-mails ###

As you can see, a required varenv is called `FBL_PARTNER_HEADER`.
Since everybody is able to send an email pretending being Microsoft SNDS,
NSA or whatever, it's important to check the identity of the mail send with
a well-kept secret. The easier way to do so is to assign a single e-mail
address per organization you keep secret.

Using the MX features, the mail must be validated and tagged with the previous
 `FBL_PARTNER_HEADER` header. We recommend to keep this header name secret too.
The value of this header is the name of the FBL. (currently supported values:
AOL, SignalSpam, SpamCop)

An example should help you to understand:

    OVH wants to received spam report from AOL.

    OVH creates a new e-mail address for AOL: fbl-55eb4d8efa1@ovh.net.
    AOL uses it to send all spam report.
    OVH adds a new rule attached to this address: when receiving a new e-mail
    from  <scomp@aol.net>, add header "X-PARTNER-HEADER: AOL" and forward this
    e-mail to the FBL_USER varenv mailbox.

    The monitoring tool is polling MX the FBL_USER varenv mailbox on EMAIL_HOST
    server and its "FBL_PARTNER_HEADER" has been set to "X-PARTNER-HEADER`.


### Network IPs ###

At last, you need add your network addresses CIDRs (only one per line) in the
`config/ips.list` file.

## Running ##

You can now insert theses entries in your favorite scheduler:

 * Schedule `reputation-rbl.sh` to be run once a day.
 * Schedule `spamhaus-bl.sh` to be run every hour.
 * Schedule `reputation-fbl.sh` and `api.sh` to be run as a daemon.

## API ##

Once everything is running, you can start using the API. By default, it's
listening to the port 5000.
Here are the few available endpoints:

 * `GET /reputation/(ip)`: Query reputation of an IP for each registered source.
 * `GET /reputation/(ip)/details/(source)`: Query the detailed reputation of an
 IP for a given source. You must use the shortened name of the source (or its
   name if no shortened one has been provided). Default available source: AOL,
   BLCK, CTALK SCOP SFS, SGS, SNDS.
 * `GET /blacklist/(ip)`: Query DNS BL to know whether this IP is black listed
 or not.
 * `GET /spamhaus/active`: Query recorded Spamhaus active issues.
 * `GET /spamhaus/resolved`: Query recorded Spamhaus resolved issues.


Enjoy

## Development

### Implementing its own RBL storage class ###

As you can see in the `config.py`, there is a way to customize the tool by
providing its own implementation to store RBL parsed documents.
By default, a basic implementation is provided and store everything on
the filesystem, using the property `RBL_STORAGE_CONTEXT` to determine the
root path to use.

You can code your own RBL storage service by implementing
`adapters.service.storage.StorageServiceBase` and then, tell the tool to
use this implementation by editing the property `CUSTOM_IMPLEMENTATIONS`.

### Implementing new parsers ###

Implementing new parsers is painless and you'll only have to implement an
interface. If your parser is valid enough, it should be automatically
registered and enabled as long as daemons are restarted.

**1. Implementing a new CSV parser**

For a brand new CSV parser, you'll need to implement
`parser.csv.csvparser.CSVParser`. Here are the explanations of methods that
must be implemented:

    # -*- encoding: utf-8 -*-

    from datetime import datetime
    from parser.csv.csvparser import CSVParser

    class MyNewParser(CSVParser):

        def __init__(self, path):
            # Consider the delimiter is a comma.
            CSVParser.__init__(self, path, ',')

        def compute_weight(self, data):
            # The weight of this entry. All the weights are then summed to rank IPs.
            # Notice data is an array containing the splitted line.
            return 1

        def get_date(self, data):
            # Date to use for this entry
            return datetime.now()

        def get_source(self, data):
            # Source name
            return 'My new parser'

        def get_ip(self, data):
            # IP the entry is talking about
            return data[0]

        def get_description():
            # Mandatory method to be automatically registered !
            return {
                'name': 'My new parser',
                'shortened': 'MNP'  # Shortened name, optionnal
            }

        get_description # staticmethod(get_description)

**2. Implementing a new mail reader**

Unlike CSV parsers, mail reader are not automatically registered.
That's why if you only want  to add a new provider using ARF,
you'll have to edit `parsing.mails.mailfactory.MailReaderFactory` and add the
new source name. (This code can be greatly improved, your PR are welcomed !)

For a brand new mail reader, you'll need to edit this file too to add your
source. And, you'll have to implement an abstract class to be able to read
mails. Here is the default format:

    # -*- encoding: utf-8 -*-

    from datetime import datetime
    from parsing.mails.mailreader import AbstractMailReader

    class MyNewReader(MailReader):

        def __init__(self, raw):
            AbstractMailReader.__init__(self)
            # Raw is the received e-mail.
            self._data # raw

        def compute_weight(self):
            # The weight of this entry. All the weights are then summed to rank IPs.
            return 1

        def get_date(self):
            # Date to use for this entry.
            return datetime.now()

        def get_source(self):
            # Source name
            return 'My new mail reader'

        def get_ip(self):
            # IP the mail is talking about
            return "1.2.3.4"

### Extending DNS BL support ###

If you want to add new DNS BL that are not supported by default, you just have
to edit the file `config/dnsbl.py` and add a new dictionary providing needed
information about the DNS BL.

Note that the shortened name is mandatory.

