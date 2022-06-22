import os
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from cap.api.balloons import BalloonApi
from cap.api.schemas import BalloonModel
from cap.forms import AddBalloonForm

balloon_api = BalloonApi(os.environ['BACKEND_URL'])

stock = Blueprint('stock', __name__)


@stock.get('/')
def all_balloons():
    context = {
        'title': 'Balloons',
        'list_balloons': balloon_api.get_all(),
        'form': AddBalloonForm(),
    }
    for balloon in context['list_balloons']:
        balloon.acceptance_date = balloon.acceptance_date.strftime('%m/%d/%Y %H:%M:%S')
    return render_template('stock.html', context=context)


@stock.post('/')
def add_balloon():
    balloon = BalloonModel(**request.form)
    balloon.acceptance_date = datetime.now()
    balloon_api.add(balloon)
    return redirect(url_for('stock.all_balloons'))


@stock.delete('/<int:uid>')
def del_balloon(uid):
    balloon_api.delete(uid)
    return {}, 204
