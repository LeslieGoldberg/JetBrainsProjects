from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


# create Table named 'task'
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default=None)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# used for weekly tasks
def show_dates(date):
    month = date.strftime('%b')
    day = date.day
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday = date.weekday()
    print(f'{days_of_the_week[weekday]} {day} {month}:')


# used for returning tasks in today's and weekly tasks
def show_rows(tasks):
    if not tasks:
        print('Nothing to do!')
    else:
        for i, task in enumerate(tasks):
            print(f'{i + 1}. {task}')


# used for
def show_tasks(tasks):
    for i, task in enumerate(tasks):
        date = task.deadline
        day = date.day
        mon = date.strftime('%b')
        i += 1
        print(f'{i}. {task}. {day} {mon}')


class ToDo:
    def __init__(self):
        self.session = None
        self.init_db()

    def init_db(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def create_row(self, task, deadline) -> str:
        new_row = Table(task=task, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()
        return 'The task has been added!'

    def show_rows_today(self):
        today = datetime.today().date()
        month = today.strftime('%b')
        day = today.day
        tasks = self.session.query(Table).filter(Table.deadline == today).all()
        print(f'\nToday {day} {month}:')
        show_rows(tasks)

    def show_rows_week(self):
        day1 = datetime.today()
        days = 1
        week = [day1]
        while days < 7:
            week.append(day1 + timedelta(days=days))
            days += 1
        for date in week:
            date = datetime.date(date)
            tasks = self.session.query(Table).filter(Table.deadline == date).all()
            print()
            show_dates(date)
            show_rows(tasks)

    def missed_tasks(self):
        missed_tasks = self.session.query(Table).filter(Table.deadline < datetime.today()).all()
        print('\nMissed tasks:')
        if not missed_tasks:
            print('Nothing is missed!')
        else:
            for i, task in enumerate(missed_tasks):
                print(f'{i + 1}. {task}')

    def delete_tasks(self):
        all_tasks = self.session.query(Table).order_by(Table.deadline).all()
        print('\nChoose the number of the task you want to delete:')
        show_tasks(all_tasks)
        choice = int(input())
        choice -= 1
        if all_tasks:
            to_delete = all_tasks[choice]
            self.session.delete(to_delete)
            self.session.commit()
            if to_delete not in self.session.query(Table).all():
                print('The task has been deleted!')
        else:
            print('Nothing to delete')

    def menu(self) -> None:
        while True:
            print()
            choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                           "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
            if choice == '1':
                self.show_rows_today()
            elif choice == '2':
                self.show_rows_week()
            elif choice == '4':
                self.missed_tasks()
            elif choice == '6':
                self.delete_tasks()

            elif choice == '3':
                all_tasks = self.session.query(Table).all()
                print('All tasks:')
                show_tasks(all_tasks)

            elif choice == '5':
                print('Enter task')
                task = str(input())
                print('Enter deadline')
                dead = str(input())
                date = datetime.strptime(dead, '%Y-%m-%d')
                print(self.create_row(task, date))

            else:
                print('\nBye!')
                exit()


todo = ToDo()
todo.menu()
