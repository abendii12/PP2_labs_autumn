class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner 
        self.balance = balance  
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"{amount} deposited. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                print(f"{amount} withdrawn. New balance: {self.balance}")
            else:
                print("Insufficient balance to complete the withdrawal.")
        else:
            print("Withdrawal amount must be positive.")

account = BankAccount("John Doe", 1000)  

account.deposit(500)  
account.withdraw(300)  
account.withdraw(1500) 