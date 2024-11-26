from flask import render_template, redirect, url_for, flash, session, Blueprint
import uuid
from welpurse.create_group.form import WelfareGroupForm
from welpurse.utils import login_required, get_current_user
from welpurse.utils import is_logged_in
from welpurse.helper_functions.utils import (
    fetch_members,
    join_group,
    add_role,
    fetch_a_role,
    fetch_roles,
)
import requests
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
create_group = Blueprint("create_group", __name__)

@create_group.route("/create_group", methods=["GET", "POST"])
@login_required
def create_welfare_group():
    url = "http://127.0.0.1:5001/api/v1/welfares"
    current_user = get_current_user()
    title = "Create Group"
    headers = {"Authorization": f"Bearer {session['access_token_cookie']}"}

    if not is_logged_in():
        return redirect(url_for("members.login"))

    form = WelfareGroupForm()
    members = fetch_members(headers=headers)
    member_choices = [
        (member.get("id"), member.get("email")) for member in members
    ]
    choices = [("", "Select Member")] + member_choices

    form.administrator.choices = choices
    form.treasurer.choices = choices
    form.secretary.choices = choices
    form.youth_rep.choices = choices
    form.chairperson.choices = choices
    form.vice_chairperson.choices = choices

    if form.validate_on_submit():
        data = {
            "administrator": form.administrator.data,
            "chairperson": form.chairperson.data,
            "contribution_frequency": form.contribution_frequency.data,
            "contribution_modes": form.contribution_modes.data,
            "description": form.description.data,
            "eligibility_requirements": form.eligibility_requirements.data,
            "group_visibility": "Public",
            "membership_approval": form.membership_approval.data,
            "min_contribution": form.min_contribution.data,
            "name": form.welfare_name.data,
            "notification_preferences": form.notification_preferences.data,
            "preferred_communication_channel": form.preferred_communication_channel.data,
            "purpose": form.purpose.data,
            "role_descriptions": {
                "chairperson": form.role_description_chairperson.data,
                "treasurer": form.role_description_treasurer.data,
                "secretary": form.role_description_secretary.data,
                "vice_chairperson": form.role_description_vice_chair.data,
                "youth_rep": form.role_description_youth_rep.data,
            },
            "searchable": form.searchable.data,
            "secretary": form.secretary.data,
            "special_events": form.special_events.data,
            "treasurer": form.treasurer.data,
            "vice_chairperson": form.vice_chairperson.data,
            "youth_rep": form.youth_rep.data,
        }

        res = requests.post(url=url, headers=headers, json=data)
        logging.info("STATUS CODE: %s", res.status_code)

        if res.status_code == 201:
            welfare_data = res.json()
            logging.info("WELFARE DATA: %s", welfare_data)
            member_id = current_user.get("id")
            # db_roles = fetch_a_role()
            #  value == member id
            # we will be saving ods of members in there roles
            # i.e "admininstrator": "adabc-gdt3-46635-62353ye-hgsyt"
            roles = fetch_roles(headers=headers)
            welfare_id = welfare_data.get("id")
            if welfare_id:
                for key, value in welfare_data.items():
                    for role in roles:
                        if value and key == role.get("name"):
                            data = {
                                "member_id": value,
                                "welfare_id": welfare_id,
                            }
                            if join_group(headers=headers, data=data):
                                create_role = add_role(
                                    headers=headers,
                                    member_id=value,
                                    role_id=role.get("id"),
                                )
                                logging.info(
                                    "SUCCESS: Added member %s of role_id %s",
                                    value,
                                    role.get("id"),
                                )
                            else:
                                flash("Failed creating a group", "danger")
                                logging.error(
                                    "FAILED: Could not add member %s", value
                                )
                                return redirect(
                                    url_for("create_group.create_welfare_group")
                                )
                flash("Succesfuly created a group", "success")
        else:
            flash("Failed creating a group", "danger")
            logging.error("ERROR OF CREATION: %s", res)
            return redirect(url_for("main.home"))

    return render_template(
        "creategroup.html", current_user=current_user, form=form, title=title
    )
