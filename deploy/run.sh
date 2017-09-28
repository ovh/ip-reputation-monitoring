#!/bin/bash
docker run -it -p 5000:5000 -e AS_NUMBER=16276 -e EMAIL_HOST=fixme.org -e FBL_USER=fixme -e FBL_PASSWORD=fixme -e FBL_PARTNER_HEADER=fixme -e REPORTING_TARGET='fixme@fixme.org' -e REPORTING_SENDER='noreply@fixme.org' -e SNDS_KEY=fixme -e SPAMHAUS_DOMAIN_NAME=ovh.net -e SPAMHAUS_DB=fixme -e SPAMHAUS_DB_USER=fixme -e SPAMHAUS_DB_PASSWORD=fixme -e SPAMHAUS_DB_HOST=fixme -e SPAMHAUS_DB_PORT=5432 -e DB_NAME=ip_bls -e DB_USER=hugo -e DB_PASSWORD=hugo -e DB_HOST=10.19.64.207 -e DB_PORT=27017 ip-reputation

