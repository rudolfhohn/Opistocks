define({ "api": [
  {
    "type": "get",
    "url": "/index/:index",
    "title": "Check if index exists",
    "name": "check_index",
    "group": "index",
    "description": "<p>Check wheter an index exists.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "index",
            "description": "<p>Index to check the existence.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "valid",
            "description": "<p>Return true if index exists, else false</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"valid\": true,\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "server/opistocks/views.py",
    "groupTitle": "index"
  },
  {
    "type": "get",
    "url": "/stocks/<index>",
    "title": "Request all stocks values from <index>",
    "name": "get_stocks",
    "group": "stocks",
    "description": "<p>Get all historic values for stocks. The value is the adjusted closing price of the day.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "index",
            "optional": false,
            "field": "index",
            "description": "<p>Intex to request the historic from</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>Date related to the value</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "value",
            "description": "<p>Adjusted closing price of the stock for the related date</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\": \"20160112\",\n    \"value\": \"15.04\"\n},\n{\n    \"date\": \"20160113\",\n    \"value\": \"19.04\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "server/opistocks/views.py",
    "groupTitle": "stocks"
  },
  {
    "type": "get",
    "url": "/stocks/:index/:date_start/:date_end",
    "title": "Request stocks values of <index> between <date_start> and <date_end>",
    "name": "get_stocks_between_date",
    "group": "stocks",
    "description": "<p>Get all historic values for stocks. The value is the adjusted closing price of the day.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "index",
            "optional": false,
            "field": "index",
            "description": "<p>Index to request the historic from</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "date_start",
            "description": "<p>Start date for the historic</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "date_end",
            "description": "<p>End date for the historic</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\": \"20160112\",\n    \"value\": \"15.04\"\n},\n{\n    \"date\": \"20160113\",\n    \"value\": \"19.04\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "server/opistocks/views.py",
    "groupTitle": "stocks"
  }
] });
