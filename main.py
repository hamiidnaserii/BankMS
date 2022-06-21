# Imports ---------------------
import json
import random
from os.path import exists

# Variable ---------------------
json_file = 'accounts_data.json'


# read data from json file and return object ---------------------
def read_data():
    if not exists(json_file):
        return {}
    f = open(json_file, "r")
    data = f.read()
    return json.loads(data)


# write data in json file ---------------------
def write_data(data):
    f = open(json_file, "w")
    json_data = json.dumps(data)
    f.write(json_data)


def line():
    print('─────────────────────────────────')


def header(title):
    print('── {} ────────────────────────────'.format(title))


# generate account number for new accounts ---------------------
def generate_account_number():
    account_number = ""
    for i in range(0, 11):
        random_number = random.randint(1, 9)
        account_number += str(random_number)

    return account_number


def check_empty_field(value):
    if not value and value != 'EMPTY':
        print("This field cannot be empty")
        return False
    elif value == 'EMPTY':
        return False
    else:
        return True


def check_exist_account(account_number):
    accounts = read_data()
    return list(accounts.keys()).__contains__(account_number)


def wait_action():
    input('Press ENTER to continue')


def print_account_info(account_number):
    accounts = read_data()
    account = accounts[account_number]
    line()
    print('Name : {}'.format(account['name']))
    print('Phone : {}'.format(account['phone']))
    print('Address : {}'.format(account['address']))
    print('Balance : {}'.format(account['balance']))
    print('Account Number : {}'.format(account['account_number']))
    line()


def create_account():
    accounts = read_data()
    header('Create Account')
    name = 'EMPTY'
    while not check_empty_field(name):
        name = str(input("Name: "))

    phone = 'EMPTY'
    while not check_empty_field(phone):
        phone = str(input("Phone: "))

    address = 'EMPTY'
    while not check_empty_field(address):
        address = str(input("Address: "))

    balance = 'EMPTY'
    while not check_empty_field(balance):
        balance = input("Balance: ")

    account_number = generate_account_number()

    accounts[account_number] = {
        'name': name,
        'phone': phone,
        'address': address,
        'balance': balance,
        'account_number': account_number
    }
    write_data(accounts)
    print("Account created successfully")
    print_account_info(account_number)
    wait_action()


def update_account():
    accounts = read_data()
    header('Update Account')
    account_number = 'EMPTY'
    while not check_empty_field(account_number):
        account_number = str(input("Account Number: "))
    if check_exist_account(account_number):
        account = accounts[account_number]
        name = str(input("Name [{}]: ".format(account['name'])))
        if not name:
            name = account['name']

        phone = str(input("Phone[{}]: ".format(account['phone'])))
        if not phone:
            phone = account['phone']

        address = str(input("Address[{}]: ".format(account['address'])))
        if not address:
            address = account['address']

        balance = str(input("Balance[{}]: ".format(account['balance'])))
        if not balance:
            balance = account['balance']

        accounts[account_number] = {
            'name': name,
            'phone': phone,
            'address': address,
            'balance': balance,
            'account_number': account_number
        }
        write_data(accounts)
        print("Account updated successfully")
        print_account_info(account_number)
        wait_action()
    else:
        print("There is no account with this number")
        wait_action()


def transaction():
    header('Transaction')
    print(
        "> 1. add amount to deposit\n"
        "> 2. withdraw from deposit\n"
        "> 3. back\n")
    choice = int(input("Enter your command :"))
    choice_dict = {
        1: add_amount_to_deposit,
        2: withdraw_from_deposit,
        3: show_menu,
    }
    choice_dict[choice]()


def add_amount_to_deposit():
    accounts = read_data()
    header('Add amount to deposit')
    account_number = 'EMPTY'
    while not check_empty_field(account_number):
        account_number = str(input("Account Number: "))
    if check_exist_account(account_number):
        amount = 'EMPTY'
        while not check_empty_field(amount):
            amount = input("Amount: ")
        balance = float(accounts[account_number]['balance'])
        balance = balance + float(amount)
        accounts[account_number]['balance'] = balance
        write_data(accounts)
        print("successfully")
        wait_action()
    else:
        print("There is no account with this number")
        wait_action()


def withdraw_from_deposit():
    accounts = read_data()
    header('Withdraw from deposit')
    account_number = 'EMPTY'
    while not check_empty_field(account_number):
        account_number = str(input("Account Number: "))
    if check_exist_account(account_number):
        amount = 'EMPTY'
        while not check_empty_field(amount):
            amount = input("Amount: ")
        balance = float(accounts[account_number]['balance'])
        if float(amount) > balance:
            print("Inventory is not enough")
            wait_action()
        else:
            balance = balance - float(amount)
            accounts[account_number]['balance'] = balance
            write_data(accounts)
            print("successfully")
            wait_action()

    else:
        print("There is no account with this number")
        wait_action()


def view_detail_account():
    header('View detail account')
    account_number = 'EMPTY'
    while not check_empty_field(account_number):
        account_number = str(input("Account Number: "))
    if check_exist_account(account_number):
        print_account_info(account_number)
        wait_action()

    else:
        print("There is no account with this number")
        wait_action()


def remove_account():
    accounts = read_data()
    header('Delete account')
    account_number = 'EMPTY'
    while not check_empty_field(account_number):
        account_number = str(input("Account Number: "))
    if check_exist_account(account_number):
        del accounts[account_number]
        write_data(accounts)
        print("successfully")
        wait_action()

    else:
        print("There is no account with this number")
        wait_action()


def view_list_account():
    header('View accounts list')
    accounts = read_data()
    list_account = []
    for user_account_number in accounts:
        user_data = accounts[user_account_number]
        user_data["account_number"] = user_account_number
        list_account.append(user_data)
    list_account = heap_sort(list_account)
    for account in list_account:
        line()
        print('Name : {}'.format(account['name']))
        print('Phone : {}'.format(account['phone']))
        print('Address : {}'.format(account['address']))
        print('Balance : {}'.format(account['balance']))
        print('Account Number : {}'.format(account['account_number']))


def heap_sort(list):
    n = len(list)
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(list, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        list[i], list[0] = list[0], list[i]  # swap
        heapify(list, i, 0)
    return list

def heapify(list, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n and float(list[i]['balance']) < float(list[l]['balance']):
        largest = l

    # See if right child of root exists and is
    # greater than root
    if r < n and float(list[largest]['balance']) < float(list[r]['balance']):
        largest = r

    # Change root, if needed
    if largest != i:
        list[i], list[largest] = list[largest], list[i]  # swap

        # Heapify the root.
        heapify(list, n, largest)


def show_menu():
    header('Main Menu')
    print(
        "> 1. Create new account\n"
        "> 2. Update information of existing account\n"
        "> 3. Transaction\n"
        "> 4. Check the details of existing account\n"
        "> 5. Removing existing account\n"
        "> 6. View accounts list\n"
        "> 7. Exit\n")
    choice = int(input("Enter your command :"))
    choice_dict = {
        1: create_account,
        2: update_account,
        3: transaction,
        4: view_detail_account,
        5: remove_account,
        6: view_list_account,
        7: exit
    }
    choice_dict[choice]()


if __name__ == '__main__':

    while True:
        show_menu()
