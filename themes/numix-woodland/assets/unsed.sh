#!/bin/sh
sed -i \
         -e 's/rgb(0%,0%,0%)/#231e18/g' \
         -e 's/rgb(100%,100%,100%)/#cabcb1/g' \
    -e 's/rgb(50%,0%,0%)/#302b25/g' \
     -e 's/rgb(0%,50%,0%)/#9d8b70/g' \
 -e 's/rgb(0%,50.196078%,0%)/#9d8b70/g' \
     -e 's/rgb(50%,0%,50%)/#302b25/g' \
 -e 's/rgb(50.196078%,0%,50.196078%)/#302b25/g' \
     -e 's/rgb(0%,0%,50%)/#cabcb1/g' \
	*.svg
