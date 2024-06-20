from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    DateField,
    SubmitField,
    HiddenField,
)
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    welfare_group_name = StringField(
        "Welfare Group Name",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    event_date = DateField(
        "Event Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    end_date = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    donation_purpose = TextAreaField(
        "Event Description",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    title = StringField("Event Title", validators=[DataRequired()])
    welfare_id = HiddenField("Welfare ID")
    request_id = HiddenField("Request ID")
    target_amount = DecimalField(
        "Amount Needed",
        validators=[DataRequired()],
        render_kw={"readonly": True},
    )
    submit = SubmitField("Create Event")
