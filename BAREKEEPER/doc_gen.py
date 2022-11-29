from dateutil import parser


class Invoice:
    def __init__(
            self,
            sender,
            tax_id,
            payment_details,
            invoice_date,
            invoice_nr,
            order_nr,
            recipient,
            entries,
            locale):
        self.sender = Person(**sender)
        self.tax_id = tax_id
        self.payment_details = PaymentDetails(**payment_details)
        self.invoice_date = parser.isoparse(invoice_date).date()
        self.invoice_nr = invoice_nr
        self.order_nr = order_nr
        self.recipient = Person(**recipient)
        self.entries = [Entry(**e) for e in entries]
        self.locale = locale
        self.total = sum([e.price for e in self.entries])
        self.tax = self.total * 0.19


class Letter:
    def __init__(
            self,
            sender,
            letter_date,
            letter_nr,
            recipient,
            headline,
            content,
            closing):
        self.sender = Person(**sender)
        self.letter_date = parser.isoparse(letter_date).date()
        self.letter_nr = letter_nr
        self.recipient = Person(**recipient)
        self.headline = headline
        self.content = content
        self.closing = closing


class Person:
    def __init__(self, address, company, name, phone, email, VAT_no, meta):
        self.address = Address(**address)
        self.company = company
        self.name = name
        self.phone = phone
        self.email = email
        self.VAT_no = VAT_no
        self.meta = meta


class Address:
    def __init__(self, street, house_number, postal_code, place, country):
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.place = place
        self.country = country


class PaymentDetails:
    def __init__(self, bank, iban, bic):
        self.bank = bank
        self.iban = iban
        self.bic = bic


class Entry:
    def __init__(self, description, price, start, end):
        self.start = parser.isoparse(start).date()
        self.end = parser.isoparse(end).date() if end is not None else None
        self.description = description
        self.price = price
