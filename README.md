# ipwfl - IP webservice frontend list generator

Build IP address list of web services like google, slack, github... Then generate iptables or other firewall rules.

**Version:** 0.01 Experimental


## Features:
 - [x] Generate rules from static IP list
 - [x] Convert custom IP/Net list to ipconfig template (firewall rule)
 - [x] ASN list lookup
 - [x] Autodiscover ASN, based on hostname. [eg. github.com, youtube.com, ...]

 


## Why?
- Imagine you want to block all traffic on your home network, but you want your Android TV to access google services.
- Imagine you want to block all traffic on your work network, but you want to access github.com, Slack.com, and some other custom IPs.
- This scripts generates IPs list based on the following input parameters: IP list, ASN, Domain2ASN


## Usage


- 1. Git clone
- 2. Edit or remove content from 'prefix.txt' (in the ./data directory)
- 3. Edi the line 'OUTPUT_COMMAND_TEMPLATE' in 'ipwfl.py' to match your network FW rules (allow/drop...)
- 5. Then run:

> 'python ./ipwfl.py'

When everything works fine. List with IP-ranges will bee generated.
Customise the content of .txt files in the /data directory to match your needs.



## Input Files:


### - 'prefix.txt'
Basic iptables/FW rules. Will be used as RAW 1:1 output on start.


### -static_list.txt  
Static IP/Network list - can put IP/Networks one per line. Lines starting on '#' are comments.


### - 'asn_list.txt'
List of ASN to lookup and add to final IP list.
https://en.wikipedia.org/wiki/Autonomous_system_(Internet)


### - 'services_list.txt'
List of domain names. (github.com, facebook.com, ...) will try to resolve IP/ASN/IP-ranges, routes... for the domain.


# Sample Output

```
#HOSTNAME/ASN/IPs for : github.com
#ASN: AS36459
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.108.0/22
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.252.0/22
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.108.0/22
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.108.0/23
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.110.0/23
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.108.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.109.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.110.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 185.199.111.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.252.0/22
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.252.0/23
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.252.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.253.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.254.0/24
iptables -YOUR -RULE -HERE -j ALLOW -d 192.30.255.0/24
```


Some notes: Services like slack.com are hosted on Amazon, that's why ASN covers other services, when using file 'services_list.txt'




## TODO:
 - [ ] TODO: remove duplicates in output!
 - [ ] normalize readme.md check typos, ...
