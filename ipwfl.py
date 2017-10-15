#!/usr/bin/python
# -*- coding: utf-8 -*-

#template for ipconfig line generator
# OUTPUT_COMMAND_TEMPLATE='%%NETWORK%%' # TO OUTPUT IP/RANGES ONLY.
OUTPUT_COMMAND_TEMPLATE='iptables -YOUR -RULE -HERE -j ALLOW -d %%NETWORK%%' # CHANGE THIS TO YOUR IPCONFIG RULE!!!

TMP_FILE='./tmp.work.txt'
AS_ROUTE_LOOKUP_CMD_TEMPLATE="whois -h whois.radb.net -- '-i origin %%AS%%' | grep 'route:' > "+TMP_FILE
IP_TO_ASN_LOOKUP_CMD_TEMPLATE="whois -h whois.radb.net -- '-i origin %%IP%%' | grep 'origin:' > "+TMP_FILE

import os
import socket


def append_to_output(LINE):
    print LINE


def add_line_to_output(NETWORK):

    if (NETWORK[:1] != '#' and NETWORK[:1] != ''):
        OUTPUT_LINE_TMP=OUTPUT_COMMAND_TEMPLATE.replace('%%NETWORK%%',str(NETWORK))
        append_to_output(OUTPUT_LINE_TMP)
    else:
        append_to_output(NETWORK)



def read_txt(FILE):
    FILE_FULLPATH=str(FILE)
    text_file = open(FILE_FULLPATH, "r")
    LINES = text_file.readlines()
    for line in LINES:
        append_to_output(line.strip())
    text_file.close()
    add_line_to_output('')

def find_asn_in_whois_output(FILE):
    text_file = open(FILE, "r")
    LINES = text_file.readlines()
    for line in LINES:
        line=line.strip()
        if (line[:7].strip()=='origin:'):
            text_file.close()
            return line.replace('origin:','').strip()




def read_txt_static(FILE):
    FILE_FULLPATH=str(FILE)

    text_file = open(FILE_FULLPATH, "r")
    LINES = text_file.readlines()
    for line in LINES:
        line=line.strip()
        if (line[:1]!='#' and line[:1]!=''):
            line = line.replace('route:', '').strip()
            add_line_to_output(line)
    text_file.close()
    add_line_to_output('')


def read_asn_file_and_lookup_routes(FILE):
    FILE_FULLPATH=str(FILE)

    text_file = open(FILE_FULLPATH, "r")
    LINES = text_file.readlines()
    for line in LINES:
        line=line.strip()
        if (line[:1]!='#' and line[:1]!=''):
            lookup_asn_route(line)
    text_file.close()
    add_line_to_output('')

def read_service_by_domain(FILE_FULLPATH):
    text_file = open(FILE_FULLPATH, "r")
    LINES = text_file.readlines()
    for line in LINES:
        line=line.strip()
        if (line[:1]!='#' and line[:1]!=''):
            ip_to_asn(hostname_to_asn_routes(line.strip()))
    text_file.close()
    add_line_to_output('')


def lookup_asn_route(NET_AS_LINE):
    NET_AS=NET_AS_LINE.split('#')[0].strip()
    add_line_to_output('#ASN: '+str(NET_AS_LINE))
    COMMAND=AS_ROUTE_LOOKUP_CMD_TEMPLATE
    COMMAND=COMMAND.replace('%%AS%%',str(NET_AS))
    os.system(COMMAND)
    read_txt_static(TMP_FILE)
    add_line_to_output('')
    remove_file(TMP_FILE)

def ip_to_asn(IP):
    COMMAND=IP_TO_ASN_LOOKUP_CMD_TEMPLATE
    COMMAND=COMMAND.replace('%%IP%%',str(IP))
    os.system(COMMAND)
    ASN=find_asn_in_whois_output(TMP_FILE)
    lookup_asn_route(str(ASN))
    add_line_to_output('')
    remove_file(TMP_FILE)


def hostname_to_asn_routes(DOMAIN):
    add_line_to_output('#HOSTNAME/ASN/IPs for : ' + str(DOMAIN))
    return str(socket.gethostbyname(DOMAIN))

def remove_file(FILE):
    try:
        os.remove(FILE)
    except:
        pass


#---------------------------start-----------------------------

remove_file(TMP_FILE)

read_txt('./data/prefix.txt')
read_txt_static('./data/static_list.txt')
read_asn_file_and_lookup_routes('./data/asn_list.txt')
read_service_by_domain('./data/services_list.txt')

remove_file(TMP_FILE)



