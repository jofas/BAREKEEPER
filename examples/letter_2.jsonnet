local types = import '../jsonnet/types.libsonnet';

types.Letter(
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
  letter_date='2021-07-06',
  letter_nr=2,
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
  headline='Das ist die Überschrift des Briefs',
  content=|||
    Sehr geehrter Herr Mustermann,

    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
    nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
    erat, sed diam voluptua.
    At vero eos et accusam et justo duo dolores et ea rebum.
    Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum
    dolor sit amet.
    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam
    nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
    erat, sed diam voluptua.
    At vero eos et accusam et justo duo dolores et ea rebum.
    Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum
    dolor sit amet.
  |||,
  closing=|||
    Mit freundlichen Grüßen,

    Maike Musterfrau
  |||,
)
