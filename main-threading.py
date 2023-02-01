from customer import *

def deposit(customer, amount):
    customer.deposit(amount)

def withdraw(customer, amount):
    customer.withdraw(amount)
def main():
    customer = Customer("Mariam", "123456789", "1234")
    customer_ = Customer("Mariamu", "123456788", "1234")
    customer.deposit(100)

    deposit_thread = threading.Thread(target=deposit, args=(customer, 100))
    withdraw_thread = threading.Thread(target=withdraw, args=(customer, 50))
    deposit_thread_ = threading.Thread(target=deposit, args=(customer_, 100))
    withdraw_thread_ = threading.Thread(target=withdraw, args=(customer_, 50))

    withdraw_thread.start()
    deposit_thread.start()
    deposit_thread_.start()
    withdraw_thread_.start()

    deposit_thread.join()
    withdraw_thread.join()
    deposit_thread_.join()
    withdraw_thread_.join()


if __name__ == "__main__":
    main()
