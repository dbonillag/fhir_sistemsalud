# * coding: utf8 *
{
    "name": "fhir_sistemsalud",
    "summary": "Sistema para realización de consulta medicas enfocado a la interoperabilidad por medio del estandar FHIR",
    "version": "0.1",
    "author": "Daniel Bonilla",
    "category": "Medical",
    "website": "https://github.com/dbonillag/fhir_sistemsalud",
    #"depends": [],
    "data": [
        "security/ir.model.access.csv",
        "views/service_request_view.xml",
        "views/clinical_record_view.xml",
        "views/diagnostic_type_view.xml",
        "views/diagnostic_view.xml",
        "views/partner_view.xml",
        "views/priority_view.xml",
        "views/clinical_menu.xml",
        "views/configuration_menu.xml"
    ],
    # "demo": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}