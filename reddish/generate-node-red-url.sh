#!/bin/bash
curl -s -X POST 10.10.10.94:1880 | echo http://10.10.10.94:1880/red/$(jq .id | sed 's/"//g')

