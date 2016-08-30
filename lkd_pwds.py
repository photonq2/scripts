import sys, argparse, requests, json
from io import StringIO
from pprint import pprint

#___________________________________________________________________IMPORTS



parser = argparse.ArgumentParser(prog='lkd_pwds',description="Looks for possible leaked passwords of an account or nickname with help of http://haveibeenpwned.com")
parser.add_argument('account', type=str, help="Email or nickname you look for")
parser.add_argument('-o', '--output', dest='out_file', type=str, help="Path/file to save to")
args = parser.parse_args()
#___________________________________________________________________ARGPARSE




def grep(foo,raw):

    count = 0
    for line in raw.split("\n"):
        count = count +1
        if count > 499999:
            break
        if foo in line:
            return line.strip()


def do_search(account, pastes_ld):

    stdout_ = sys.stdout
    myout = StringIO()
    sys.stdout = myout


    i=1
    for paste_d in pastes_ld:
    	print("["+str(i)+"/"+str(len(pastes_ld))+"]"+" - ################################")
    	i=i+1
    	pprint(paste_d)
    	print("########################################")

    #PASTEBIN
    	if paste_d['Source'] == 'Pastebin':
    		pastebin_res = requests.get('http://pastebin.com/raw/' + paste_d['Id'])
    		if "This page has been removed!" in pastebin_res.text:
    			print("Paste removed!\n")
    		else:
    			lkd = grep(account,pastebin_res.text)
    			print("[**] " + lkd +"\n\n\n")
    #OTHERS
    	#elif:

    	else:
    		print("[!] Not supported url\n")


    sys.stdout = stdout_
    return myout.getvalue()

#___________________________________________________________________FUNCTIONS





if args.account == None:
    print("Please enter email")
    exit()

got = requests.get('https://haveibeenpwned.com/api/v2/pasteaccount/' + args.account)

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


found = do_search(args.account, pastes_ld)
print(found)
if args.out_file != None:
    print("[+] Saving to "+args.out_file + " ...")
    fd = open(args.out_file,'w')
    fd.write(found)
    fd.close()
