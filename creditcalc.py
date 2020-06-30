import argparse
from sys import argv
from math import log, ceil

parser = argparse.ArgumentParser(description='credit calculator')
parser.add_argument("--type", choices=['annuity', 'diff'], help='type of payment')
parser.add_argument("--payment", help='monthly payment')
parser.add_argument('--principal', help='total principal')
parser.add_argument('--periods', help='number of months to repay credit')
parser.add_argument('--interest', help='must be included, no percentage sign')
args = parser.parse_args()


def calculate_diff(principal, periods, interest):
    m = 1
    n = periods
    total_paid = 0
    while n > 0:
        d = ceil((principal / periods) + interest * (principal - (principal * (m - 1)) / periods))
        n -= 1
        print(f'Month {m}: paid out {d}')
        m += 1
        total_paid += d
    over = int(total_paid - principal)
    if over != 0:
        print(f'Overpayment = {over}')


def calculate_payments(payment, principal, interest):
    n_payments = ceil(log(payment / (payment - interest * principal), 1 + interest))
    over = int((n_payments * payment) - principal)
    return n_payments, over


def calculate_principal(payment, interest, periods):
    principal = int(payment / ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1)))
    over = int((payment * periods) - principal)
    return principal, over


def calculate_annuity(principal, interest, periods):
    a_monthly = ceil(principal * ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1)))
    over = int((a_monthly * periods) - principal)
    return a_monthly, over


user_payment = 0.0
user_principal = 0.0
user_interest = 0.0
user_periods = 0.0
overpayment = 0
error_message = "Incorrect parameters"

if args.payment is not None:
    user_payment = float(args.payment)
if args.principal is not None:
    user_principal = float(args.principal)
if args.interest is not None:
    user_interest = (float(args.interest) / 100) / 12
if args.periods is not None:
    user_periods = float(args.periods)

if args.type is False:
    print(error_message + ' type')
elif args.type == 'diff' and args.payment is not None:
    print(error_message + ' diff/pay')
elif args.interest is None:
    print(error_message + ' no interest')
elif user_payment < 0:
    print(error_message + 'payment')
elif user_principal < 0:
    print(error_message + 'principal')
elif user_periods < 0:
    print(error_message + 'periods')
elif user_interest < 0:
    print(error_message + 'interest')
elif len(argv) < 4:
    print(error_message + ' need more args')
elif args.type == 'diff':
    calculate_diff(user_principal, user_periods, user_interest)
elif args.type == 'annuity':
    if args.payment is None:
        monthly_annuity, overpayment = calculate_annuity(user_principal, user_interest, user_periods)
        print(f'Your annuity payment = {monthly_annuity}!')
    elif args.principal is None:
        total_principal, overpayment = calculate_principal(user_payment, user_interest, user_periods)
        print(f'Your credit principal = {total_principal}!')
    elif args.periods is None:
        number_payments, overpayment = calculate_payments(user_payment, user_principal, user_interest)
        years = str(int(number_payments / 12)) + ' years'
        months = str(number_payments % 12) + ' months'
        if '1' in years:
            years = '1 year'
        elif '1' in months:
            months = '1 month'
        if '0' in months:
            print(f'You need {years} to repay this credit!')
        elif '0' in years:
            print(f'You need {months} to repay this credit!')
        else:
            print(f'You need {years} and {months} to repay this credit!')
    if overpayment != 0:
        print(f'Overpayment = {overpayment}')
