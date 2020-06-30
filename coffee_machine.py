money = 550
water = 400
milk = 540
coffee_beans = 120
cups = 9


def remaining():
    global water, milk, coffee_beans, cups, money
    print('The coffee machine has:')
    print(str(water) + ' of water')
    print(str(milk) + ' of milk')
    print(str(coffee_beans) + ' of coffee beans')
    print(str(cups) + ' of disposable cups')
    print(str(money) + ' of money')


def espresso():
    global water, coffee_beans, cups, money
    for i in range(1):
        if water >= 250:
            water -= 250
        else:
            print('Sorry, need more water.')
            break
        if coffee_beans >= 16:
            coffee_beans -= 16
        else:
            print('Sorry, need more coffee.')
            break
        if cups >= 1:
            cups -= 1
        else:
            print('Sorry, need more cups.')
            break
        money += 4
        print('I have enough resources, making you a coffee!')


def latte():
    global water, milk, coffee_beans, cups, money
    for i in range(1):
        if water >= 350:
            water -= 350
        else:
            print('Sorry, need more water.')
            break
        if milk >= 75:
            milk -= 75
        else:
            print('Sorry, need more milk.')
            break
        if coffee_beans >= 20:
            coffee_beans -= 20
        else:
            print('Sorry, need more coffee.')
            break
        if cups >= 1:
            cups -= 1
        else:
            print('Sorry, need more cups')
            break
        money += 7
        print('I have enough resources, making you a coffee!')


def cappucino():
    global water, milk, coffee_beans, cups, money
    for i in range(1):
        if water >= 200:
            water -= 200
        else:
            print('Sorry, need more water.')
            break
        if milk >= 100:
            milk -= 100
        else:
            print('Sorry, need more milk.')
            break
        if coffee_beans >= 12:
            coffee_beans -= 12
        else:
            print('Sorry, need more coffee.')
            break
        if cups >= 1:
            cups -= 1
        else:
            print('Sorry, need more cups.')
            break
        money += 6
        print('I have enough resources, making you a coffee!')


def buy():
    print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappucino: ')
    purchase = input()
    if '1' in purchase:
        return espresso()
    elif '2' in purchase:
        return latte()
    elif '3' in purchase:
        return cappucino()
    else:
        pass


def fill():
    global water, milk, coffee_beans, cups
    print('Write how many ml of water do you want to add: ')
    water += int(input())
    print('Write how many ml of milk do you want to add: ')
    milk += int(input())
    print('Write how many grams of coffee beans do you want to add: ')
    coffee_beans += int(input())
    print('Write how many disposable cups of coffee do you want to add: ')
    cups += int(input())


def take():
    global money
    print('I gave you ' + str(money))
    money = 0


class CoffeeMachine:


    def __init__(self):
        self.action = None
        self.buy = None
        self.take = None
        self.remaining = None
        self.fill = None


my_coffee = CoffeeMachine()
print('Write action (buy, fill, take, remaining, exit): ')
action = input()
while 'exit' not in action:
    if "buy" in action:
        buy()
    elif "fill" in action:
        fill()
    elif "take" in action:
        take()
    elif "remaining" in action:
        remaining()
    print('Write action (buy, fill, take, remaining, exit): ')
    action = input()
