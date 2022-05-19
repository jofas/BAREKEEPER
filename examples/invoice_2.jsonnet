local types = import '../types.libsonnet';

types.Invoice(
  sender=types.Person(
    address=types.Address(
      street='Hauptstraße',
      house_number='69',
      postal_code='45257',
      place='Essen',
    ),
    company='Thyssen Krupp',
    name='Maike Musterfrau',
    phone='02218/224466',
    email='xyz@abc.de',
  ),
  tax_id='LMN/OPQ/RSTU',
  payment_details=types.PaymentDetails(
    bank='Deutsche Bank',
    iban='DE5454545454545454545454',
    bic='SOMEBICXXX',
  ),
  invoice_date='2021-07-06',
  invoice_nr=2,
  recipient=types.Person(
    address=types.Address(
      street='Am Hinseldaunenweg',
      house_number='18',
      postal_code='50667',
      place='Köln',
    ),
    company='Siemens AG',
    name='Max Mustermann',
  ),
  entries=[
    types.Entry(
      description='Irgendeine Dienstleistung',
      price=25000.0,
      start='2021-03-03',
      end='2021-07-06',
    ),
    types.Entry(
      description='Irgendeine andere Dienstleistung',
      price=20170.0,
      start='2021-05-05',
      end='2021-06-06',
    ),
    types.Entry(
      description='Irgendeine coole Machine',
      price=80000.0,
      start='2021-07-06',
    ),
  ],
)
