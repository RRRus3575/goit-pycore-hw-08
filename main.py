from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else: 
            raise ValueError("Phone number must be a 10-digit number.")
            

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        del self.data[name]

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None
    
    def get_upcoming_birthdays(self):
        new_users = {}
        current_date = datetime.today().date()
        finish_date = current_date + timedelta(days=7)

        for user, record in self.data.items():
            if record.birthday:
                date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                now_year_date = date.replace(year=current_date.year)
                if current_date <= now_year_date <= finish_date:
                    new_users[user] = date
        sorted_dates_dict = {key: value for key, value in sorted(new_users.items(), key=lambda item: item[1])}
        return sorted_dates_dict

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Give me name and phone please.")
        except KeyError:
            print("Enter correct user name")
        except IndexError:
            print('Please provide a contact name')


    return inner



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    try:
        name, phone, *_ = args
        record = book.find(name)
        if record is None:
            record = Record(name)
            book.add_record(record)
        record.add_phone(phone)
        return "Contact updated."
    except ValueError as e:
        return str(e)

@input_error
def show_phone(args, book: AddressBook):        
    name = args[0]      
    record = book.find(name)
    if record:
        return str(record)
    else:
        return "Contact not found."

@input_error
def show_all_contacts(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    else:
        result = ""
        for name, record in book.data.items():
            result += str(record) + "\n"
        return result

@input_error
def add_birthday(args, book: AddressBook):
    try:
        name, date = args
        record = book.find(name)
        if record is None:
            return 'Condact does not exist'
        else:
            record.add_birthday(date)
            return 'Birthday has been added to the contact'
    except ValueError as e:
        return str(e)
    except:
        return 'Enter name and birthday date'

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]      
    record = book.find(name)
    if record:
        return f'Name: {record.name}, birthday: {record.birthday}'
    else:
        return "Contact not found."

@input_error
def birthdays(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    else:
        result = ''
        books_birthday = book.get_upcoming_birthdays()
        if len(books_birthday) > 0:
            for name, birthday in books_birthday.items():
                result += f'Name: {name}, Birthday: {birthday}' + "\n"
            return result
        else:
            return 'There are no birthdays in the next week'
        

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("Hello! How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(add_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()