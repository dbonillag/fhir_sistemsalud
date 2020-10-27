# -*- coding: utf-8 -*-

## AADTokenCredentials for multi-factor authentication
from msrestazure.azure_active_directory import AADTokenCredentials

## Other required imports
import adal, uuid, time

import json


import requests




from openerp import fields, models, api

import logging
_logger = logging.getLogger(__name__)



class I15dPatient(models.Model):
	_name = 'fhir.i15d.patient'

	_inherit = 'fhir.i15d.base'

	# def authenticate_client_key(self):
	#     """
	#     Authenticate using service principal w/ key.
	#     """
	#     authority_host_uri = 'https://login.microsoftonline.com'
	#     tenant = '59e07b78-8abd-4f0c-ab90-f8bdd2b2d530'
	#     authority_uri = authority_host_uri + '/' + tenant
	#     resource_uri = 'https://sistemsalud-fhir.azurehealthcareapis.com'
	#     client_id = 'e4b31336-af16-491d-84ae-25f2cafc0b3d'
	#     client_secret = 'K~G0hcTshz_58_B8IA~KA6ba76wXZktsCK'

	#     context = adal.AuthenticationContext(authority_uri, api_version=None)
	#     mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)
	#     credentials = AADTokenCredentials(mgmt_token, client_id)

	#     return credentials


	def test_post_patient(self):
		
		json_m = '''
		{
	    "resourceType": "Patient",
	    "active": true,
    	"name": [
    		{
    			"use": "official",
    			"family": "qqq",
    			"given": [
    				"james",
    				"kirk"
    			]
    		},
    		{
    			"use": "usual",
    			"given": [
    				"jim"
    			]
    		}
    	],
	    "gender": "male",
	    "birthDate": "2000-12-25"
    	}
		'''

		url = "https://sistemsalud-fhir.azurehealthcareapis.com/Patient"

		# credentials = self.authenticate_client_key()
		headers = {
		  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiJodHRwczovL3Npc3RlbXNhbHVkLWZoaXIuYXp1cmVoZWFsdGhjYXJlYXBpcy5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81OWUwN2I3OC04YWJkLTRmMGMtYWI5MC1mOGJkZDJiMmQ1MzAvIiwiaWF0IjoxNjAzNjQ3NjU5LCJuYmYiOjE2MDM2NDc2NTksImV4cCI6MTYwMzY1MTU1OSwiYWNyIjoiMSIsImFpbyI6IkFXUUFtLzhSQUFBQWt2VklDcXEyU2VsQ1lUcGw4YVhER2J0SldXNFZEWHM0TU5JL0dUNU5sMGVMTmpnZGpKcFVEK2hFMVhHVVlUbVkvNllxQzRORjhTRlkwdG1uUFZKd3J6dHF3SkdYN2U4akZlU0dvaHJkeSs0aFkxWUlFREhISGxMd09uWVFPQU5FIiwiYWx0c2VjaWQiOiIxOmxpdmUuY29tOjAwMDMwMDAwMjZEMUZBNTgiLCJhbXIiOlsicHdkIiwibWZhIl0sImFwcGlkIjoiMDRiMDc3OTUtOGRkYi00NjFhLWJiZWUtMDJmOWUxYmY3YjQ2IiwiYXBwaWRhY3IiOiIwIiwiZW1haWwiOiJkYW5pdmFyYTIwMDhAb3V0bG9vay5lcyIsImZhbWlseV9uYW1lIjoiQm9uaWxsYSIsImdpdmVuX25hbWUiOiJEYW5pZWwiLCJpZHAiOiJsaXZlLmNvbSIsImlwYWRkciI6IjE5MS44OS4xNDIuODgiLCJuYW1lIjoiRGFuaWVsIEJvbmlsbGEiLCJvaWQiOiJjYWQ3ZjUyOS0yMWIwLTQ4N2MtOTZkMS04NDgxMzI1Njc0YWYiLCJwdWlkIjoiMTAwMzIwMDBFQTIxREFGOCIsInJoIjoiMC5BQUFBZUh2Z1diMktERS1ya1BpOTByTFZNSlYzc0FUYmpScEd1LTRDLWVHX2UwWjFBT1EuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoiU0dmNFY2NHBrdE13NlZkUlpod2k5RzNTSW5zcTR0bFNoeW5iVHY0YmFLQSIsInRpZCI6IjU5ZTA3Yjc4LThhYmQtNGYwYy1hYjkwLWY4YmRkMmIyZDUzMCIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jZGFuaXZhcmEyMDA4QG91dGxvb2suZXMiLCJ1dGkiOiJyY0pJSG1QeURFU051ZTFfclhWeUFBIiwidmVyIjoiMS4wIn0.YVYpJAVpaBHwzO82Tj27HRlJR5pAeruHP3dY7dvSeyYo0BaQBF6ZlpGrZmWG5L3AQBoyu2MYwy5HB4appe-xhcpsCQNxSzfljvzXNBkr1WO84d86CjzkgG1rgj3p5bLXpW8K84NUF0Mn9Cm_X5baNFliPgQbSA1KlLqgIxHcPECu2jftUn9OJ5HmxfRhS0Hv2jyy5sVULRWx0uMTwWQ8tSuHuo-Ml5LluhdqI-pEoS1wObKecXrnUNI48lLCWaJLPLQWTCy_Ov5MScbbuYfBcfJxItcNiADeg-agKa6mj4MQOX8inVcLGQ5ZdpqWx_9Jg2pcKAHPH6wbDFSnSqK7Qw',
		  'Content-Type': 'application/json'
		}

		#_logger.info(json.dumps(credentials.token))

		response = requests.request("POST", url, headers=headers, data = json_m)

		_logger.info(response.text.encode('utf8'))

		return 

