from bank_service import BankService
from cash_bin import CashBin
import logging

class ATMController:
	def __init__(self, bank_service, cash_bin):
		self.bank_service = bank_service
		self.cash_bin = cash_bin
		self.token = None
		self.account_list = None

	def validate_pin(self, pin_from_user):
		try: 
			self.token = self.bank_service.get_token_from_pin(pin_from_user)
			logging.info("Valid pin")
		except RuntimeError as e:
			logging.warning(e)

	def get_account_list(self, pin):
		if self.token is None:
			logging.warning("No Token Issued")
			return None

		self.account_list = self.bank_service.get_account_list(self.token, pin)
		logging.info("")
		return self.account_list

	def see_balance(self, index: int):
		try:
			self.is_account_valid(index)
			balance = self.bank_service.get_account_balance(self.account_list[index])
			logging.info("Your Balance: {balance}")
			return balance
		except RuntimeError as e:
			logging.warning(e)
			return -1
	
	def is_account_valid(self, index):
		if self.account_list is None:
			raise Exception("No Account List")

		if index < 0 or index >= len(self.account_list):
			raise Exception("No account exists at position " + str(index + 1))

	def deposit_balance(self, index: int, amount: int):
		assert amount > 0, "Amount must be a positive integer"

		try:
			self.is_account_valid(index)
			self.bank_service.deposit_to_account(self.account_list[index], amount)
			self.cash_bin.deposit(amount)
			logging.info("Successful deposit of {amount}")
		except RuntimeError as e:
			logging.warning(e)

	def withdraw_balance(self, index: int, amount: int):
		assert amount > 0, "Amount must be a positive integer"

		try:
			self.is_account_valid(index)
			self.cash_bin.withdraw(amount)
			self.bank_service.withdraw_from_account(self.account_list[index], amount)
			logging.info("Successful withdrawl of {}")

		except RuntimeError as e:
			logging.warning(e)

