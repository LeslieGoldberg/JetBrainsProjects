import random
from sqlalchemy import Column, Integer, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

db_id = 0

engine = create_engine('sqlite:///card.s3db?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()


class Account(declarative_base()):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    number = Column(Text)
    pin = Column(Text)
    balance = Column(Integer, default=0)

    def __repr__(self):
        return self.number


def database_update(num, p):
    new_row = Account(number=num, pin=p)
    session.add(new_row)
    session.commit()


def confirm_account(user_acct_num):
    confirm = session.query(Account).filter(Account.number == user_acct_num).exists()
    return confirm


def confirm_pin(user_acct, user_pin):
    all_accounts = session.query(Account).all()
    confirm = False
    for account in all_accounts:
        if account.number == user_acct and account.pin == user_pin:
            confirm = True
    return confirm


def check_balance(numb):
    account = session.query(Account).filter(Account.number == numb)
    for a in account:
        balance = a.balance
    return balance


def luhn_algorithm(card_num):
    algorithm_number = [int(num) for num in card_num[0:-1]]
    index = 0
    second_index = 0
    for number in algorithm_number:
        if index % 2 == 0:
            number *= 2
            algorithm_number.pop(index)
            algorithm_number.insert(index, number)
        index += 1
    for number in algorithm_number:
        if number > 9:
            number -= 9
            algorithm_number.pop(second_index)
            algorithm_number.insert(second_index, number)
        second_index += 1
    sum_luhn = sum(algorithm_number)
    if (sum_luhn + int(card_num[-1])) % 10 == 0:
        return True
    else:
        return False


def add_income(account_number):
    print('Enter income:')
    additional_income = int(input())
    account = session.query(Account).filter(Account.number == account_number)
    for a in account:
        a.balance += additional_income
    session.commit()


def do_transfer(account_number):
    print('''Transfer
Enter card number:''')
    transfer_account = input()
    all_accounts = session.query(Account).all()
    account_number_list = [account.number for account in all_accounts]
    if transfer_account == account_number:
        return "You can't transfer money to the same account!"
    elif luhn_algorithm(transfer_account) is False:
        return '''Probably you made mistake in the card number. 
Please try again!'''
    elif transfer_account not in account_number_list:
        return 'Such a card does not exist.'
    else:
        print('Enter how much money you want to transfer: ')
        transfer_amount = int(input())
        account = session.query(Account).filter(Account.number == account_number)
        for a in account:
            if a.balance - transfer_amount < 0:
                return 'Not enough money!'
            else:
                a.balance -= transfer_amount
                other_account = session.query(Account).filter(Account.number == transfer_account)
                for b in other_account:
                    b.balance += transfer_amount
                session.commit()
                return 'Success!'


def close_account(account_number):
    session.query(Account).filter(Account.number == account_number).delete()
    session.commit()
    if confirm_account(account_number) is False:
        return 'The account has been closed!'
    else:
        return 'There has been an error.'


def acct_num():
    ind = 0
    dex = 0
    iin = [4, 0, 0, 0, 0, 0]
    can_list = [random.randint(0, 9) for x in range(9)]
    partial = []
    for x in iin:
        partial.append(x)
    for x in can_list:
        partial.append(x)
    for x in partial:
        if ind % 2 == 0:
            x *= 2
            partial.pop(ind)
            partial.insert(ind, x)
        ind += 1
    for x in partial:
        if x > 9:
            x -= 9
            partial.pop(dex)
            partial.insert(dex, x)
        dex += 1
    if sum(partial) % 10 == 0:
        checksum = 0
    else:
        remainder = sum(partial) % 10
        checksum = 10 - remainder
    account = ''.join(str(elem) for elem in iin) + ''.join(str(elem) for elem in can_list) + str(checksum)
    return account


def create_account():
    account_num = acct_num()
    pin_list = [random.randint(0, 9) for x in range(4)]
    pin = ''.join(str(elem) for elem in pin_list)
    database_update(account_num, pin)
    num = session.query(Account).filter(Account.number == account_num)
    for n in num:
        p = n.pin
    acct_answer = f'''
Your card has been created
Your card number:
{num[0]}
Your card PIN:
{p}
'''
    print(acct_answer)


def acct_menu():
    print('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
    acct_choice = int(input())
    return acct_choice


def bank_menu():
    print('''
1. Create an account
2. Log into an account
0. Exit''')
    bank_choice = int(input())
    return bank_choice


def user_account(num):
    answer = 0
    x = 1
    while x > 0:
        account_choice = acct_menu()
        if account_choice == 1:
            answer = f"Balance: {check_balance(num)}"
        elif account_choice == 2:
            add_income(num)
            answer = 'Income was added!'
        elif account_choice == 3:
            answer = do_transfer(num)
        elif account_choice == 4:
            answer = close_account(num)
            x -= 1
        elif account_choice == 5:
            answer = 'You have successfully logged out!'
            x -= 1
        elif account_choice == 0:
            print('Bye!')
            session.close()
            exit()
        print(answer)


def acct_log_in():
    print('Enter your card number:')
    user_num = input()
    print('Enter your PIN: ')
    user_pin = input()
    if confirm_account(user_num) is False:
        print('Wrong card number or PIN!')
    elif confirm_pin(user_num, user_pin) is False:
        print('Wrong card number or PIN!')
    else:
        print('You have successfully logged in!')
        user_account(user_num)


def banking_system():
    user = True
    while user is True:
        user_choice = bank_menu()
        if user_choice == 1:
            create_account()
        elif user_choice == 2:
            acct_log_in()
        elif user_choice == 0:
            print('Bye!')
            user = False
    session.close()


if __name__ == '__main__':
    try:
        Account.__table__.create(engine)
    except:
        pass
    banking_system()
