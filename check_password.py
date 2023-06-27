'''This program accepts any number of passwords typed into the terminal. It checks them against
a database containing hundreds of millions of compromised passwords and lets the user know
how many times their password has been compromised.'''

import requests
import hashlib 
import sys

#Accepts the first 5 characters of a SHA1 hash and connects to the pwnedpasswords API
def req_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching {response.status_code}. Check API and try again.')
    else:
        return response
    
#Reads the hash list from pwnedpasswords and sees if the hash tail matches any of the input passwords
def count_leaks(hashes, hash_tail):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_tail:
            return count
    return 0

#Converts the inputted passwords into SHA1 hashes then feeds it to count_leaks function
def pwned_api_check(password):
    #utf-8 needed because need to encode before hashing
    #hexdigest turns into hexidecimal, double in length. can read python docs for more.
    #uppercase so that it conforms with requirements of API
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    api_res = req_api_data(first5_char)
    return count_leaks(api_res, tail)

#Prints the results of the above functions so that the user knows which input passwords were compromised and which weren't
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'The password <{password}> was found {count} times. Time to change it!')
        else:
            print (f'The password <{password}> was not found. Carry on!')

#Runs the 'main' function accepting any number of passwords input into the terminal.
#Only runs the program if this is the main file.
#Closes it afterwards.
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))