from .AmountTypes import PaidAmount
from .util import Xmleable, default_document, createElementContent


class PrepaidPaymentID(Xmleable):
    def __init__(self, id):
        self.id = id
        self.schemeName = "Anticipo"
        self.schemeAgencyName = "PE:SUNAT"

    def generate_doc(self):
        self.doc = createElementContent("cbc:ID", self.id)
        self.doc.setAttribute("schemeName", self.schemeName)
        self.doc.setAttribute("schemeAgencyName", self.schemeAgencyName)


class PaidDate(Xmleable):
    def __init__(self, date):
        self.date = date

    def generate_doc(self):
        self.doc = createElementContent("cbc:PaidDate", self.date)


class PaidTime(Xmleable):
    def __init__(self, time):
        self.time = time

    def generate_doc(self):
        self.doc = createElementContent("cbc:PaidTime", self.time)


class PrepaidPayment(Xmleable):
    def __init__(self, id=None, paid_amount=None, currency = None, paid_date=None, paid_time=None):
        self.id = id
        self.paid_amount = paid_amount
        self.paid_date = paid_date
        self.paid_time = paid_time
        self.currency = currency

    def fix_values(self):
        if type(self.id) == str:
            self.id = PrepaidPaymentID(self.id)
        if type(self.paid_date) == str:
            self.paid_date = PaidDate(self.paid_date)
        if type(self.paid_time) == str:
            self.paid_time = PaidTime(self.paid_time)
        if type(self.paid_amount) in [float,int]:
            self.paid_amount = PaidAmount(self.paid_amount,self.currency)

    def validate(self, errs, obs):
        assert self.currency not in ["PEN","USD"], "Las monedas permitidas son PEN o USD"
        assert type(self.id) != PrepaidPaymentID,"El ID de PrepaidPayment es Obligatorio"
        assert type(self.paid_amount) != PaidAmount,"El Monto de PrepaidPayment es Obligatorio"
        assert self.paid_date is None or type(self.paid_date) != PaidDate, "El valor de la fecha de pago debe ser None o PaidDate"
        assert self.paid_time is None or type(self.paid_time) != PaidTime,"El valor de la fecha de pago debe ser None o PaidTime"

    def generate_doc(self):
        self.doc = default_document.createElement("cac:PrepaidPayment")
        self.doc.appendChild(self.id.get_document())
        self.doc.appendChild(self.paid_amount.get_document())
        if self.paid_date:
            self.doc.appendChild(self.paid_date.get_document())
        if self.paid_time:
            self.doc.appendChild(self.paid_time.get_document())
