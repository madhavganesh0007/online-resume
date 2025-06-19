import os
import smtplib
from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config  # Import your config class

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# --- Page Routes ---

@app.route('/')
def home():
    return render_template('home.html', active_page='home')

@app.route('/skills-and-projects')
def skills():
    return render_template('skills.html', active_page='skills')

@app.route('/resume')
def resume():
    return render_template('resume.html', active_page='resume')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

# --- Form Submission Logic ---

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            my_email = app.config['MY_EMAIL']
            my_password = app.config['MY_PASSWORD']

            if not my_email or not my_password:
                flash('Server error: Email configuration is missing.', 'danger')
                return redirect(url_for('contact'))

            recipient_email = "jstvamsikrishna@gmail.com"
            subject = f"New Portfolio Contact from {name}"
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            msg = f"Subject:{subject}\n\n{email_body}".encode('utf-8')

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=recipient_email,
                    msg=msg
                )

            flash('Your message has been sent successfully! I will get back to you soon.', 'success')

        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Sorry, there was an error. Please try again or contact me directly via email.', 'danger')

        return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)