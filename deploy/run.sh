#!/bin/bash
docker run -it -p 5000:5000 --env-file=deploy/vars.env ip-reputation

