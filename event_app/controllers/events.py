from crypt import methods
from datetime import datetime
import os
from flask import Blueprint, redirect, render_template, abort, request, url_for
from event_app.models import Event
from flask_login import login_required, current_user
from event_app import app, db

events = Blueprint('events', __name__,)

@events.route('/', methods=['GET'])
def index():
  all_events = Event.query.all()
  currentUser = current_user
  return(render_template('events/index.html', events=all_events, currentUser=currentUser))

@events.route('/<id>', methods=['GET'])
def show(id):
  event = Event.query.filter_by(id=id).one()
  currentUser = current_user
  currentUserOwnsEvent = current_user.is_authenticated and event.owner_id == currentUser.id
  currentUserNotInRsvps = currentUser not in event.rsvps
  return(render_template('events/show.html', event=event, currentUser=currentUser, currentUserOwnsEvent=currentUserOwnsEvent, currentUserNotInRsvps=currentUserNotInRsvps))

@events.route('/new', methods=['GET'])
@login_required
def new():
  currentUser = current_user
  return(render_template('events/new.html', currentUser=currentUser, event=None))

@events.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
  event = Event.query.filter_by(id=id).one()
  currentUser = current_user
  currentUserOwnsEvent = event.owner_id == currentUser.id
  if (currentUserOwnsEvent):
    return(render_template('events/edit.html', event=event, currentUser=currentUser))
  else:
    return(redirect(f'/events/{id}'))

@events.route('/create', methods=['POST'])
@login_required
def create():
  currentUser = current_user
  owner_id = currentUser.id
  title = request.form.get('title')
  desc = request.form.get('desc')
  imgUrl = request.form.get('imgUrl')
  date = request.form.get('date')
  location = request.form.get('location')

  new_event = Event(
    owner_id=owner_id,
    title=title,
    desc=desc,
    imgUrl=imgUrl,
    date=date,
    location=location,
  )

  db.session.add(new_event)
  db.session.commit()

  return(redirect(f'/events/{new_event.id}'))

@events.route('/<id>/update', methods=['POST'])
def update(id):
  event = Event.query.filter_by(id=id).one()

  if (current_user.id == event.owner_id):
    title = request.form.get('title')
    desc = request.form.get('desc')
    imgUrl = request.form.get('imgUrl')
    date = request.form.get('date')
    location = request.form.get('location')

    event.title = title
    event.desc = desc
    event.imgUrl = imgUrl
    event.date = date
    event.location = location

    db.session.add(event)
    db.session.commit()

  return(redirect(f'/events/{id}'))

@events.route('/<id>/delete', methods=['POST'])
def destroy(id):
  event = Event.query.filter_by(id=id).one()
  
  if (current_user.id == event.owner_id):
    db.session.delete(event)
    db.session.commit()
    return(redirect('/'))
  else:
    return(redirect(f'/events/{id}'))

@events.route('/<id>/rsvp/', methods=['POST'])
@login_required
def rsvp(id):
  event = Event.query.filter_by(id=id).one()
  event.rsvps.append(current_user)

  db.session.add(event)
  db.session.commit()

  return(redirect(f'/events/{id}'))

@events.route('/<event_id>/rsvp/<id>/delete', methods=['POST'])
@login_required
def delete_rsvp(event_id, id):
  event = Event.query.filter_by(id=event_id).one()
  id = int(id)

  if (current_user.id == event.owner.id or current_user.id == id):
    for user in event.rsvps:
      if user.id == id:
        event.rsvps.remove(user)
        break

    db.session.add(event)
    db.session.commit()

  return(redirect(f'/events/{event_id}'))
