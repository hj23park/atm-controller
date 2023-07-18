class CashBin:
	def __init__(self):
		self.current_cash = 10000

	def deposit(self, amount):
		self.current_cash += amount

	def withdraw(self, amount):
		if amount > self.current_cash:
			raise Exception("Not enough cash in cashbin")

		self.current_cash -= amount
		return True