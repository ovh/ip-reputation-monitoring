#!/bin/bash
docker run -it -p 5000:5000 -e AS_NUMBER=16276 -e EMAIL_HOST=fixme.org -e FBL_USER=fixme -e FBL_PASSWORD=fixme -e FBL_PARTNER_HEADER=fixme -e REPORTING_TARGET='fixme@fixme.org' -e REPORTING_SENDER='noreply@fixme.org' -e SNDS_KEY=fixme -e SPAMHAUS_DOMAIN_NAME=ovh.net -e SPAMHAUS_DB=fixme -e POSTGRES_USER=fixme -e POSTGRES_PASSWORD=fixme -e POSTGRES_HOST=fixme -e POSTGRES_PORT=5432 -e MONGO_DB_NAME=ip_bls -e MONGO_USER=hugo -e MONGO_PASSWORD=hugo -e MONGO_HOST=10.19.64.207 -e MONGO_PORT=27017 ip-reputation

