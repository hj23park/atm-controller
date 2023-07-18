class BankService:
	def __init__(self):
		self.account_balance = {}
		self.account_list = []
		self.pin_to_token = {}

	def add_account(self, account_number, balance):
		self.account_list.append(account_number)
		self.account_balance[account_number] = balance

	def get_token_from_pin(self, pin):
		if pin in self.pin_to_token:
			raise RuntimeError("Token already issued for pin")
		return self.generate_token(pin)

	def generate_token(self, pin):
		token = f"token_is_here_{pin}"
		self.pin_to_token[pin] = token
		return token

	def get_account_list(self, token, pin):
		if pin not in self.pin_to_token:
			raise RuntimeError("No token issued for pin")

		if token!= self.pin_to_token[pin]:
			raise RuntimeError("Token does not match pin")

		return self.account_list

	def get_account_balance(self, selected_account_number):
		if selected_account_number not in self.account_balance:
			raise Exception("Invalid account number")
		return self.account_balance[selected_account_number]

	def deposit_to_account(self, selected_account_number, amount):
		assert amount > 0, "Amount must be a positive integer"

		if selected_account_number not in self.account_balance:
			raise Exception("Invalid account number")

		self.account_balance[selected_account_number] += amount

	def withdraw_from_account(self, selected_account_number, amount):
		assert amount > 0, "Amount must be a positive integer"

		if selected_account_number not in self.account_balance:
			raise Exception("Invalid account number")

		if self.account_balance[selected_account_number] < amount:
			raise Exception("Insufficient funds")

		self.account_balance[selected_account_number] -= amount
