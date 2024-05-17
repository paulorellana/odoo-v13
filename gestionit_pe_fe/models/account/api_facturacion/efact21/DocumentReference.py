from .util import Xmleable, default_document
from .Party import PartyIdentification
from .BasicGlobal import ID


# Catalogo 12
class DocumentTypeCode(Xmleable):
    def __init__(self, document_type_code):
        self.document_type_code = document_type_code
        self.listName = "Documento Relacionado"
        self.listAgencyName = "PE:SUNAT"
        self.listURI = "urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo12"

    def generate_doc(self):
        self.doc = default_document.createElement("cbc:DocumentTypeCode")
        self.doc.setAttribute('listName', self.listName)
        self.doc.setAttribute('listAgencyName', self.listAgencyName)
        self.doc.setAttribute('listURI', self.listURI)

        text = default_document.createTextNode(self.document_type_code)
        self.doc.appendChild(text)
        return self.doc


class IssuerParty(Xmleable):
    def __init__(self,party_identification):
        self.party_identification = party_identification

    def validate(self, erros, observs):
        assert type(self.party_identification) == PartyIdentification

    def generate_doc(self):
        self.doc = default_document.createElement("cac:IssuerParty")
        self.doc.appendChild(self.party_identification.get_document())

class DocumentStatusCode(Xmleable):
    def __init__(self,document_status_code):
        self.document_status_code = document_status_code
    
    def generate_doc(self):
        self.doc = default_document.createElement("cbc:DocumentStatusCode")
        text = default_document.createTextNode(self.document_status_code)
        self.doc.appendChild(text)

class AdditionalDocumentReference(Xmleable):
    def __init__(self, id, document_type_code,document_status_code=None,issuer_party=None):
        self.id = ID(id)
        self.document_type_code = document_type_code
        self.document_status_code = document_status_code
        self.issuer_party = issuer_party

    def fix_values(self):
        if type(self.document_type_code) == str:
            self.document_type_code = DocumentTypeCode(self.document_type_code)
        if type(self.document_status_code) == str:
            self.document_status_code = DocumentStatusCode(self.document_status_code)

    def validate(self, errs, obs):
        assert type(self.document_type_code) == DocumentTypeCode
        assert self.document_status_code is None or type(self.document_status_code) == DocumentStatusCode
        assert self.issuer_party is None or type(self.issuer_party) == IssuerParty

    def generate_doc(self):
        self.doc = default_document.createElement("cac:AdditionalDocumentReference")
        self.doc.appendChild(self.id.get_document())
        if self.document_type_code:
            self.doc.appendChild(self.document_type_code.get_document())
        if self.document_status_code:
            self.doc.appendChild(self.document_status_code.get_document())

        if self.issuer_party:
            self.doc.appendChild(self.issuer_party.get_document())

        return self.doc


class DespatchDocumentReference(Xmleable):
    def __init__(self, id, document_type_code=None):
        self.id = ID(id)
        self.document_type_code = document_type_code

    def fix_values(self):
        if type(self.document_type_code) == str:
            self.document_type_code = DocumentTypeCode(self.document_type_code)

    def validate(self, errs, obs):
        assert self.document_type_code is None or type(self.document_type_code) == DocumentTypeCode

    def generate_doc(self):
        self.doc = default_document.createElement("cac:DespatchDocumentReference")
        self.doc.appendChild(self.id.get_document())
        if self.document_type_code:
            self.doc.appendChild(self.document_type_code.get_document())
        return self.doc
