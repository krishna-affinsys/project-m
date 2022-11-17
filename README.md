# project-m
**A simple messaging system for bank**

A messaging system makes it easier to authenticate an user and lets the bank extend specialised services and offers to their consumers. 
The convenience of executing simple transactions and sending out information or alerting a customer on the mobile phone is often the 
overriding factor that dominates over the skeptics who tend to be overly bitten by security concerns.


### Setting up local environment

- Clone the repository 
```bash
git clone https://github.com/krishna-affinsys/project-m.git
```

- Create virtual environment
```python
python -m venv venv
source /venv/bin/activate
```

- Install dependencies
```python
python -m pip install -r requirements.txt
```

- Setting up the database
```bash
python manage.py makemigrations && python manage.py migrate
```

- Running the server
```bash
python manage.py runserver
```

### Functionalities

#### Available features:

- Messaging is done through SMS only for now.
- Send notification on account creation.
- Send notification on transaction.
- Send a message on request for a card.
- Wish users on particular events.
- Broadcast bank offers.

#### What more could be added?

##### Push and Pull services

Typical push services would include:

- Periodic account balance reporting (say at the end of month)
- Reporting of salary and other credits to the bank account
- Successful or un-successful execution of a [standing order](https://en.wikipedia.org/wiki/Standing_order_(banking) "Standing order (banking)")
- Successful payment of a [cheque](https://en.wikipedia.org/wiki/Cheque "Cheque") issued on the account
- [Insufficient funds](https://en.wikipedia.org/wiki/Insufficient_funds "Insufficient funds")
- Large value withdrawals on an account
- Large value withdrawals on the ATM or [EFTPOS](https://en.wikipedia.org/wiki/EFTPOS "EFTPOS") on a [debit card](https://en.wikipedia.org/wiki/Debit_card "Debit card")
- Large value payment on a [credit card](https://en.wikipedia.org/wiki/Credit_card "Credit card") or out of country activity on a credit card.
- [One-time password](https://en.wikipedia.org/wiki/One-time_password "One-time password") and authentication
- An alert that some payment is due.
- An alert that an e-statement is ready to be downloaded.

Typical pull services would include:

- Account balance enquiry
- Mini statement request
- [Electronic bill payment](https://en.wikipedia.org/wiki/Electronic_bill_payment "Electronic bill payment")
- Transfers between customer's own accounts, like moving money from a savings account to a current account to fund a cheque
- Stop payment instruction on a cheque
- Requesting for an [ATM card](https://en.wikipedia.org/wiki/ATM_card "ATM card") or [credit card](https://en.wikipedia.org/wiki/Credit_card "Credit card") to be suspended;
- De-activating a credit or debit card when it is lost or the [PIN](https://en.wikipedia.org/wiki/Personal_identification_number "Personal identification number") is known to be compromised
- Foreign currency exchange rates enquiry


### To-Do

- [ ] Need to add an efficient SMS module.

---

**Contact:** krishna.raj@affinsys.com
