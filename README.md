# password-checker
#api #hashlib #pwnedpasswords

The program **check_password.py** uses the [Have I Been Pwned](https://haveibeenpwned.com/Passwords) API to see if your password has been leaked online.
### The best part is... It doesn't send your password to any server!

User input is converted to a SHA1 hash, and this is what is checked against Have I Been Pwned's database of compromised passwords.
