from flask import render_template, session, redirect, url_for
from welpurse.routes import app_routes
from welpurse.forms.donation_req import DonationRequestForm

@app_routes.route('/submit_donation', methods=['GET', 'POST'])
def submit_donation():
    form = DonationRequestForm()
    if form.validate_on_submit():
        # Process the form data
        # You can access form data using form.reason.data and form.amount_requested.data
        # Extract member_id and welfare_id from the session
        member_id = session.get('member_id')
        welfare_id = session.get('welfare_id')
        
        # Implement your logic to handle the donation request here
        
        return redirect(url_for('thank_you'))  # Redirect to a 'thank you' page, for example
    return render_template('donate.html', form=form)
