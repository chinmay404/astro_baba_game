from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from chains import AIResponse as Air  # Ensure the import alias matches the actual class name
from uuid import uuid4

app = Flask(__name__)
app.secret_key = str(uuid4())  # Convert UUID to a string
ai_instance = Air()
@app.route("/")
def index():
    return render_template("take_input.html")

@app.route('/submit', methods=['POST'])
def submit():
    try:
        session['name'] = request.form['name']
        session['dob'] = request.form['date_of_birth']
        session['birthplace'] = request.form['birthplace']
        session['gender'] = request.form['gender']
        session['period'] = '3 Months'
        session['fields'] = 'Health, Career, Relationship'
        session['PREDICTIONS'] = None
        session['IMAGE_DESCRIPTION'] = None

    except Exception as e:
        print("Form Validation Error: ", e)
        return render_template("take_input.html")
    return redirect(url_for('chat'))
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get('user_message', '')

        # Check if predictions are already made
        if session.get('PREDICTIONS'):
            # If predictions exist, use the chat chain
            ai_response = ai_instance.chat_chain(session, user_message)
            return jsonify({'ai_response': ai_response})
        else:
            # If no predictions are made yet, generate predictions
            try:
                ai_response = ai_instance.get_response(session=session)
                ai_prediction = ai_response[0] if ai_response else "Prediction could not be generated."
                return jsonify({'ai_response': ai_prediction})
            except Exception as e:
                print("AI Response Error: ", e)
                return jsonify({'ai_response': "An error occurred while generating the prediction."})
    
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)
