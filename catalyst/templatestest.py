medicaid_delivery = {
  "name": "Sample Document",
  "template_uuid": "7y6ioQAPryGxUYz3pqSZTB",
  "recipients": [
    {
	  "email":"nshea@catalystgroupdevelopment.com",
      "first_name": "Test",
      "last_name": "Test",
    }
  ],
  "fields": {
    "patientname": {
      "value": ""
    },
  }
}



test_doc_create = {
  "name": "Sample Document",
  "template_uuid": "rKXyioeScisZR8siLAsDWh",
  "recipients": [
    {
	  "email":"nshea@catalystgroupdevelopment.com",
      "first_name": "Test",
      "last_name": "Test",
    }
  ],
  "fields": {
    "patientname": {
      "value": "Test"
    },
	"patientaddress": {
      "value": "Test"
    },
	"patientphone": {
      "value": "Test"
    },
	"patientdob": {
      "value": "12/13/20"
    }
  },
    "pricing_tables": [
    {
	  "name": "PricingTable1",
      "sections": [
        {
        "title": "Sample Section",
        "default": "true",
          "rows": [
            {
              "options": {
                "optional": "false",
                "optional_selected": "true",
                "qty_editable": "true"
              },
              "data": {
                "qty": "1",
                "name": "This is a headrest, test",
                "price": "10",
              },
			  "custom_fields": {
			    "manufacturer":"Headrests Inc",
				"model":"E-type",
				"partno":"11H",
				"hcpcs": "304004043",
				"allowable": "10"
			  }
            },
			            {
              "options": {
                "optional": "false",
                "optional_selected": "true",
                "qty_editable": "true"
              },
              "data": {
                "qty": "1",
                "name": "This is a headrest, test",
                "price": "10",
              },
			  "custom_fields": {
			    "manufacturer":"Headrests Inc",
				"model":"E-type",
				"partno":"11H",
				"hcpcs": "304004043",
				"allowable": "10"
			  }
            }
          ]
        }
      ]
    }
  ]
}