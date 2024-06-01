#!/usr/bin/env bash

url="https://api.paystack.co/subaccount"
authorization="Authorization: Bearer sk_test_2f9f7bbe4eb351be854aa3a46b9c0277e4579b9a"
content_type="Content-Type: application/json"
data='{ 
  "business_name": "athconGroup", 
  "settlement_bank": "044", 
  "account_number": "1214280", 
  "percentage_charge": 18.2 
}'

curl "$url" -H "$authorization" -H "$content_type" -d "$data" -X POST