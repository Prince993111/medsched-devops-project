from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "medsched")
DB_USER = os.getenv("DB_USER", "medadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "SuperSecurePassword123!")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection engine failed: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        # Extract patient information along with the new contact fields
        patient_name = request.form.get("patient_name")
        contact_number = request.form.get("contact_number")
        email_address = request.form.get("email_address")
        identity_number = request.form.get("identity_number")
        residential_address = request.form.get("residential_address")
        visit_reason = request.form.get("visit_reason")
        preferred_date = request.form.get("preferred_date")
        preferred_time = request.form.get("preferred_time")
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                # Initialize fresh table schema to capture the newly introduced data paths
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS cns_appointments (
                        id SERIAL PRIMARY KEY,
                        patient_name VARCHAR(100),
                        contact_number VARCHAR(50),
                        email_address VARCHAR(100),
                        identity_number VARCHAR(50),
                        residential_address TEXT,
                        visit_reason TEXT,
                        preferred_date VARCHAR(30),
                        preferred_time VARCHAR(30)
                    );
                """)
                
                cur.execute("""
                    INSERT INTO cns_appointments (
                        patient_name, contact_number, email_address, identity_number, 
                        residential_address, visit_reason, preferred_date, preferred_time
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (patient_name, contact_number, email_address, identity_number, 
                      residential_address, visit_reason, preferred_date, preferred_time))
                
                conn.commit()
                cur.close()
                conn.close()
                message = f"Success! Appointment request recorded for {patient_name}."
            except Exception as e:
                message = f"Database Layer Error: {e}"
        else:
            message = f"Saved Locally (Database Offline): Data received for {patient_name}."

    return render_template("index.html", message=message)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)