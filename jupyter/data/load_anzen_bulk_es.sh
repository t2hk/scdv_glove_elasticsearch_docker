#!/bin/bash

for FILE in `find ./json/ -maxdepth 1 -type f`; do
	echo ${FILE}
	curl -X POST -H "Content-Type: application/json" "elasticsearch:9200/anzen/_bulk?pretty" --data-binary @${FILE}
done
