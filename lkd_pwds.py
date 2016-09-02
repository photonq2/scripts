#!/usr/bin/env python3.5

import sys, argparse, requests, json,re
from io import StringIO
from pprint import pprint

#___________________________________________________________________IMPORTS
parser = argparse.ArgumentParser(prog='lkd_pwds',description="Looks for possible leaked passwords of an account or nickname with help of http://haveibeenpwned.com")

group = parser.add_mutually_exclusive_group()
group.add_argument('-a','--account',dest='account', type=str, help="Email or nickname you look for")
group.add_argument('-s','--src',dest="src_file",type=str,help="Proccess list of emails")

parser.add_argument('-o', '--output', dest='out_file', type=str, help="Path/file to save to")
parser.add_argument('-v','--verbose',dest='verb',type=bool,help="Increases program verbosity")

args = parser.parse_args()

#___________________________________________________________________ARGPARSE
def grep(foo,raw):

    count = 0
    for line in raw.split("\n"):
        count = count +1
        if count > 400000:
            break
        if foo in line:
            return line.strip()



def do_search(account):

    got = requests.get('https://haveibeenpwned.com/api/v2/pasteaccount/' + account)

    if got.status_code == 200:
        print("[+] Request OK \n")
    elif got.status_code == 400:
        print("[!] Bad request")
        exit()
    elif got.status_code == 403:
        print("[!] Forbidden")
        exit()
    elif got.status_code == 404:
        print("[!] Not found")
        exit()
    elif got.status_code == 500:
        print("[!] Unreacheable")
        exit()
    else:
        print("[!] Err at request")
        exit()

        #Loads gotten json to pastes list of dictionaries
    pastes_ld = json.loads(got.text)


    stdout_ = sys.stdout
    myout = StringIO()
    sys.stdout = myout

    i=1
    print("[+] Analyzing "+ account + " ...\n")
    for paste_d in pastes_ld:
        if args.verb:
            print("["+str(i)+"/"+str(len(pastes_ld))+"]"+" - ################################")
            i=i+1
            pprint(paste_d)
            print("########################################")


    #PASTEBIN
        if paste_d['Source'] == 'Pastebin':
            pastebin_res = requests.get('http://pastebin.com/raw/' + paste_d['Id'])
            if "This page has been removed!" in pastebin_res.text:
                if args.verb:
                    print("Paste removed!")
                    print("\n")
            else:
                lkd = grep(account,pastebin_res.text)
                print("[**] " + lkd )
                print("\n")
    #OTHERS
    	#elif:

        else:
            if args.verb:
                print("[!] Not supported url")
                print("\n")


    sys.stdout = stdout_
    return myout.getvalue()

#___________________________________________________________________FUNCTIONS
if args.src_file != None:
    try:
        print("[+] Opening file " + args.src_file + " ...")
        f_src= open(args.src_file,'r')
        pattern = re.compile(r"([\w\-\.]+[@]\w[\w\-]+\.+[\w\-]+)")

        src_list = re.findall(pattern, f_src.read())
        pprint(src_list)
        for item in src_list:
            found = do_search(item)
            print(found)

        f_src.close()

    except FileNotFoundError:
        print("[!] Not valid data source path")
        exit()


if args.account != None:
    found = do_search(args.account)
    print(found)

if args.out_file != None:
    print("[+] Saving to "+args.out_file + " ...")
    fd = open(args.out_file,'w')
    fd.write(found)
    fd.close()
