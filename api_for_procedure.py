from flask import Flask, request, jsonify
import pyodbc
import sys
import threading

app = Flask(__name__)

def get_db_connection():
    # Update these details with your SQL Server Express credentials
    server = 'MOE-KT-4710547\SQLEXPRESS' 
    database = 'YK_SAFEME' 
    username = 'sa' 
    password = 'Mafat1234' 
    driver = 'SQL Server' # This might change based on your ODBC driver version # This might change based on your ODBC driver version
    return pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
def core_procedure_logic(data):
    # Check if data is a dictionary and has the required keys
    required_keys = [
        'request_id', 'client_name', 'client_address', 'client_vat_id', 'Role',
        'deal_id', 'client_id', 'payment_reference', 'document_notes',
        'client_email', 'client_phone', 'fee_discount_percentage',
        'total_deposit_amount', 'total_fee_amount_before_discount',
        'total_fee_amount_include_discount', 'fee_discount_amount',
        'payment_method', 'representative_name', 'summary_document_url',
        'deal_unique_url'
    ]

    if not isinstance(data, dict) or not all(key in data for key in required_keys):
        raise ValueError("Invalid data format or missing keys")
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            DECLARE @return_value int
            EXEC @return_value = [dbo].[yk_create_recipt]
            @request_id = ?,
            @client_name = ?,
            @client_address = ?,
            @client_vat_id = ?,
            @Role = ?,
            @deal_id = ?,
            @client_id = ?,
            @payment_reference = ?,
            @document_notes = ?,
            @client_email = ?,
            @client_phone = ?,
            @fee_discount_percentage = ?,
            @total_deposit_amount = ?,
            @total_fee_amount_before_discount = ?,
            @total_fee_amount_include_discount = ?,
            @fee_discount_amount = ?,
            @payment_method = ?,
            @representative_name = ?,
            @summary_document_url = ?,
            @deal_unique_url = ?
        """, 
        data['request_id'], 
        data['client_name'],
        data['client_address'],
        data['client_vat_id'],
        data['Role'],
        data['deal_id'],
        data['client_id'],
        data['payment_reference'],
        data['document_notes'],
        data['client_email'],
        data['client_phone'],
        data['fee_discount_percentage'],
        data['total_deposit_amount'],
        data['total_fee_amount_before_discount'],
        data['total_fee_amount_include_discount'],
        data['fee_discount_amount'],
        data['payment_method'],
        data['representative_name'],
        data['summary_document_url'],
        data['deal_unique_url'])
        if cursor.rowcount > 0:
         #result = cursor.fetchone()[0]
         connection.commit()
         #return result
    
 
    

@app.route('/execute_procedure', methods=['POST'])
def execute_procedure():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400
    try:
        result = core_procedure_logic(data)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
@app.route('/shutdown', methods=['POST'])


def run_on_start():
    print("Executing procedure on start...")
    # Example data for testing
    default_data = {
    "request_id": 123334,
    "client_name": "יוסי יעקובוביץ",
    "client_address": "גרניט 6 פתח תקווה",
    "client_vat_id": 531111111,
    "Role": "Seller",
    "deal_id": 66778899,
    "client_id": 7012356,
    "payment_reference": 987654,
    "document_notes": "בדיקה",
    "client_email": "shimi@yk.co.il",
    "client_phone": "0546627304",
    "fee_discount_percentage": 0,
    "total_deposit_amount": 0,
    "total_fee_amount_before_discount": 1000,
    "total_fee_amount_include_discount": 1000,
    "fee_discount_amount": 0,
    "payment_method": 1,
    "representative_name": "שימי",
    "summary_document_url": "www.yk.co.il",
    "deal_unique_url": "www.yk.co.il"
    }

    try:
        core_procedure_logic(default_data)
    except ValueError as e:
        print("Error:", e)

if __name__ == '__main__':
    threading.Thread(target=run_on_start).start()
    app.run(debug=True)

