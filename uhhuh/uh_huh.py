from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from uhhuh.db import get_db
from uhhuh.functions import get_runners, crunch_the_numbers, is_url, get_table_name, is_time

bp = Blueprint('uh_huh', __name__)


@bp.route('/')
def form():
    return render_template('form.html')


@bp.route('/uh-huh', methods=['GET', 'POST'])
def uh_huh():
    if request.method == 'GET':
        return "The URL can't be accessed directly"

    if request.method == 'POST':
        usr_time = request.form['usr_time']
        url = request.form['url']
        err = None
        db = get_db()

        if not is_url(url):
            err = 'Invalid URL.'
        if not is_time(usr_time):
            err = 'Invalid time format.'
        if err is None:
            race_name = get_table_name(url)
            race = db.execute(
                "SELECT * FROM race WHERE race_name=?", (race_name,)).fetchall()

            if not race:
                db.execute(
                    "INSERT INTO race(race_name) VALUES(?)", (race_name,))
                runners = get_runners(url, race_name)
                db.executemany(
                    "INSERT INTO runner(race_name,rank,number,first_name,last_name,club,country,chip_time,gun_time,status,remark) VALUES(?,?,?,?,?,?,?,?,?,?,?)", runners)
                db.commit()
                times = db.execute(
                    "SELECT gun_time FROM runner JOIN race ON runner.race_name = race.race_name WHERE race.race_name = ? AND status IS 'OK'", (race_name,)).fetchall()
                gun_times = [time[0] for time in times]
                numbers_dict = crunch_the_numbers(gun_times, usr_time)
            else:
                times = db.execute(
                    "SELECT gun_time FROM runner JOIN race ON runner.race_name = race.race_name WHERE race.race_name = ? AND status IS 'OK'", (race_name,)).fetchall()
                gun_times = [time[0] for time in times]
                numbers_dict = crunch_the_numbers(gun_times, usr_time)
            return render_template('uh_huh.html', usr_time=usr_time, url=url, numbers=numbers_dict)
    flash(err)
    return redirect(url_for("uh_huh.form"))
