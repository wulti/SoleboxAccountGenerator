# -------------------------------------------------------------------------------- SETUP & IMPORTS -------------------------------------------------------------------------------- #


from colorama import Fore, Style, init
import threading
import time
import random

from bonzay_pkg.solebox import SoleboxGen
from bonzay_pkg.reusable import readFile, logMessage, loadProxies

init(autoreset=True)
print_lock = threading.Lock()

print('\n'*50)
print(Fore.YELLOW + r'''       ,.,
      MMMM_    ,..,
        "_ "__"MMMMM          ,...,,
 ,..., __." --"    ,.,     _-"MMMMMMM
MMMMMM"___ "_._   MMM"_."" _ """"""
 """""    "" , \_.   "_. ."
        ,., _"__ \__./ ."
       MMMMM_"  "_    ./
        \'\'\'\'      (    )
 ._______________.-\'____"---._.
  \                          /
   \________________________/
   (_)                    (_)''')
print(Fore.YELLOW + "   BONZAY Tools™ · Solebox tool")
print(r'''-----
https://github.com/rtunaboss/SoleboxAccountGenerator
• developed by: rtuna#4321 | @rtunazzz
• for personal use only
-----''')

# -------------------------------------------------------------------------------- FUNCTIONS -------------------------------------------------------------------------------- #

print_lock = threading.Lock()
PROXY_LIST = None
SUCCESS_COUNT = 0
def initialize_gen():
    if not PROXY_LIST:
        logMessage("ERROR", "You did not load proxies. Put your proxies into the proxies.txt file before running.")
        exit()
    return SoleboxGen(PROXY_LIST)

def SoleboxGenerateAccount():
    global SUCCESS_COUNT
    gen = initialize_gen()
    create_status = gen.generateAccount(print_lock)
    if create_status:
        s = gen.updateShippingAddress(print_lock, new_account=True)
        if s:
            SUCCESS_COUNT += 1

def SoleboxGenerateAccountNoShipping():
    global SUCCESS_COUNT
    gen = initialize_gen()
    create_status = gen.generateAccount(print_lock, no_shipping=True)
    if create_status:
        SUCCESS_COUNT += 1

def SoleboxCheckAccount(email, passwd):
    gen = initialize_gen()
    gen.checkAccount(print_lock, email, passwd)

def SoleboxCheckShippingAddress(email, passwd):
    gen = initialize_gen()
    gen.checkShippingAddress(print_lock, email=email, passwd=passwd)

def SoleboxUpdateShippingExistingAccount(email, passwd):
    gen = initialize_gen()
    gen.updateShippingAddress(print_lock, new_account=False, email=email, passwd=passwd)

def start():
    print(Style.BRIGHT + Fore.CYAN + "Welcome to BONZAY Tools™!")
    print(Fore.LIGHTYELLOW_EX + "Please select an option:")
    print(Fore.LIGHTYELLOW_EX + "[1] - Generate Solebox accounts (with a shipping address)")
    print(Fore.LIGHTYELLOW_EX + "[2] - Generate Solebox accounts (with " + Style.BRIGHT + Fore.LIGHTYELLOW_EX + "NO shipping address" + Style.NORMAL + Fore.LIGHTYELLOW_EX + ")")
    print(Fore.LIGHTYELLOW_EX + "[3] - Check Solebox accounts' shipping addresses")
    print(Fore.LIGHTYELLOW_EX + "[4] - Check valid Solebox accounts")
    print("------")

    # ----- Get input (which option) ----- #
    while(1):
        option = input()
        try:
            option = int(option)
            if type(option) is int and option in range(1,5):
                break
            else:
                print(f"{option} is not a valid option. Try again with a number from 1 to 4:")
        except:
            print("Not an integer. Try again:")


    # ---------------------------------------- [1] - Solebox Account Generator (with a shipping address) ---------------------------------------- #
    if option == 1:
        # print("\n"*100)
        print(Style.BRIGHT + Fore.CYAN + "SOLEBOX ACCOUNT GENERATOR")
    
        # ----- Get input (how many accs to generate) ----- #
        how_many = None
        while(1):
            try:
                how_many = int(input("How many accounts would you like to create?\n"))
            except ValueError:
                print("That is not an integer. Try again...")
            if type(how_many) == int:
                break
        print(Style.BRIGHT + "Starting to generate Solebox accounts...")
        threads = []
        for _ in range(how_many):
            t = threading.Thread(target=SoleboxGenerateAccount)
            threads.append(t)
            t.start()
            time.sleep(random.randint(1,3))
                
        for t in threads:
            t.join()
        print("\nFinished generating Solebox accounts.")
        print(Style.BRIGHT + f"\nGenerated {SUCCESS_COUNT}/{how_many} accounts!")

     # ---------------------------------------- [1] - Solebox Account Generator (with NO shipping address) ---------------------------------------- #
    if option == 2:
        # print("\n"*100)
        print(Style.BRIGHT + Fore.CYAN + "SOLEBOX ACCOUNT GENERATOR")
    
        # ----- Get input (how many accs to generate) ----- #
        how_many = None
        while(1):
            try:
                how_many = int(input("How many accounts would you like to create?\n"))
            except ValueError:
                print("That is not an integer. Try again...")
            if type(how_many) == int:
                break
        print(Style.BRIGHT + "Starting to generate Solebox accounts...")
        threads = []
        for _ in range(how_many):
            t = threading.Thread(target=SoleboxGenerateAccountNoShipping)
            threads.append(t)
            t.start()
            time.sleep(random.randint(1,3))
                
        for t in threads:
            t.join()
        print("\nFinished generating Solebox accounts.")
        print(Style.BRIGHT + f"\nGenerated {SUCCESS_COUNT}/{how_many} accounts!")

    # ---------------------------------------- [3] - Solebox Shipping Address Checker ---------------------------------------- #
    elif option == 3:
        print(Style.BRIGHT + Fore.CYAN + "SOLEBOX SHIPPING ADDRESS CHECKER")
        # ----- Load all accounts with shipping ----- #
        print("Loading accounts from solebox-valid.txt")
        f = readFile("./accounts/solebox-valid.txt")
        accounts = f.split('\n')
    
        print(Style.BRIGHT + "Starting to check Solebox account's shipping addresses.")
        # ----- Create one thread for each account ----- #
        threads = []
        for account in accounts:
            if account.strip() == '':
                continue
            username, password = account.split(':')
            t = threading.Thread(target=SoleboxCheckShippingAddress, args=(username, password))
            threads.append(t)
            t.start()
            time.sleep(random.randint(1,3))
                
        for t in threads:
            t.join()
        print(Style.BRIGHT + "\nFinished checking Solebox account's shipping addresses.")
    
    # ---------------------------------------- [4] - Solebox Valid Account Checker ---------------------------------------- #
    elif option == 4:
        print(Style.BRIGHT + Fore.CYAN + "SOLEBOX VALID ACCOUNT CHECKER")
        # ----- Load all accounts with shipping ----- #
        print("Loading accounts from solebox-valid.txt")
        f = readFile("./accounts/solebox-valid.txt")
        accounts = f.split('\n')

        print(Style.BRIGHT + "Starting to check valid Solebox accounts...")
        # ----- Create one thread for each account ----- #
        threads = []
        for account in accounts:
            if account.strip() == '':
                continue
            # check if there's no newline in password
            username, password = account.split(':')
            t = threading.Thread(target=SoleboxCheckAccount, args=(username, password))
            threads.append(t)
            t.start()
            time.sleep(random.randint(1,3))
            
                
        for t in threads:
            t.join()
        print(Style.BRIGHT + "\nFinished checking Solebox accounts.")


# -------------------------------------------------------------------------------- RUNNING -------------------------------------------------------------------------------- #

if __name__ == "__main__":
    PROXY_LIST = loadProxies("./proxies.txt")
    print("-----")
    start()