import unittest
import logging
from atm_controller import ATMController
from bank_service import BankService
from cash_bin import CashBin

class ATMControllerTest(unittest.TestCase):
    PIN = "0123456789"

    def setUp(self):
        bank_service = BankService()
        bank_service.add_account("account_0", 350)
        bank_service.add_account("account_1", 10000)
        bank_service.add_account("account_2", 3000)
        cash_bin = CashBin()
        self.atm_controller = ATMController(bank_service, cash_bin)

    def test_pin_validation(self):
        try:
            self.atm_controller.validate_pin("0000000000")
        except RuntimeError as e:
            self.assertEqual("Invalid PIN", str(e))

        self.atm_controller.validate_pin(self.PIN)

    def test_get_account_list(self):
        self.atm_controller.validate_pin(self.PIN)
        account_list = self.atm_controller.get_account_list(self.PIN)
        self.assertEqual(3, len(account_list))

    def test_see_balance(self):
        self.atm_controller.validate_pin(self.PIN)
        self.atm_controller.get_account_list(self.PIN)
        
        balance = self.atm_controller.see_balance(0)
        self.assertEqual(350, balance)
        balance = self.atm_controller.see_balance(1)
        self.assertEqual(10000, balance)
        balance = self.atm_controller.see_balance(2)
        self.assertEqual(3000, balance)

    def test_deposit(self):
        self.atm_controller.validate_pin(self.PIN)
        self.atm_controller.get_account_list(self.PIN)
        self.atm_controller.see_balance(0)
        self.atm_controller.deposit_balance(0, 2000)
        balance = self.atm_controller.see_balance(0)
        self.assertEqual(2350, balance)

    def test_withdraw(self):
        self.atm_controller.validate_pin(self.PIN)
        self.atm_controller.get_account_list(self.PIN)
        self.atm_controller.see_balance(1)

        with self.assertRaises(Exception) as e:
            self.atm_controller.withdraw_balance(1, 10001)
        self.assertEqual("Not enough cash in cashbin", str(e.exception))

        balance = self.atm_controller.see_balance(1)
        self.assertEqual(10000, balance)

        balance = self.atm_controller.see_balance(0)
        self.assertEqual(350, balance)

        with self.assertRaises(Exception) as e:
            self.atm_controller.withdraw_balance(0, 400)
        self.assertEqual("Insufficient funds", str(e.exception))

        balance = self.atm_controller.see_balance(2)
        self.assertEqual(3000, balance)

        self.atm_controller.withdraw_balance(2, 2000)
        balance = self.atm_controller.see_balance(2)
        self.assertEqual(1000, balance)

    def test_is_valid_exception(self):
        self.atm_controller = ATMController(BankService(), CashBin())
        with self.assertRaises(Exception) as e:
            self.atm_controller.see_balance(-1)
        self.assertEqual("No Account List", str(e.exception))

        self.atm_controller.validate_pin(self.PIN)
        self.atm_controller.get_account_list(self.PIN)
        with self.assertRaises(Exception) as e:
            self.atm_controller.see_balance(0)
        self.assertEqual("No account exists at position 1", str(e.exception))

if __name__ == "__main__":
    unittest.main()
