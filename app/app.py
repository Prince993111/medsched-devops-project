from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extracting all the new form options
        patient_name = request.form.get('name')
        id_card = request.form.get('id_card')
        address = request.form.get('address')
        disease = request.form.get('disease')
        appointment_date = request.form.get('date')
        appointment_time = request.form.get('time')
        
        # Comprehensive log inside terminal container outputs
        print("\n" + "="*40)
        print("[NEW APPOINTMENT RECEIVED]")
        print(f"Patient: {patient_name}")
        print(f"ID Card: {id_card}")
        print(f"Address: {address}")
        print(f"Symptom/Disease: {disease}")
        print(f"Schedule: {appointment_date} at {appointment_time}")
        print("="*40 + "\n")
        
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; margin-top: 50px; background-color: #f4f7f6;">
                <div style="background: white; display: inline-block; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: left; max-width: 400px;">
                    <h2 style="color: #28a745; text-align: center;">🎉 Appointment Confirmed!</h2>
                    <hr style="border: 0; border-top: 1px solid #eee;">
                    <p><strong>Patient Name:</strong> {patient_name}</p>
                    <p><strong>ID Card Checked:</strong> {id_card}</p>
                    <p><strong>Condition Noted:</strong> {disease}</p>
                    <p><strong>Time Slot:</strong> {appointment_date} @ {appointment_time}</p>
                    <hr style="border: 0; border-top: 1px solid #eee;">
                    <div style="text-align: center; margin-top: 20px;">
                        <a href="/" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold;">Book Another</a>
                    </div>
                </div>
            </body>
        </html>
        """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    