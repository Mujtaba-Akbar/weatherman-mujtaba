from flask import Flask, request, render_template, redirect, url_for
import json
import os
from calculator import Calculator
from report_generator import ReportGenerator
from weather_data_parser import WeatherDataParser
from consts import DATA_DIR
app = Flask(__name__)

parser = WeatherDataParser(DATA_DIR)
weather_data = parser.populate_data()
calculator = Calculator(weather_data)


@app.route('/', methods=['GET'])
def help():
    return render_template("index.html")


@app.route('/yearly-extremes', methods=['GET'])
def yearly_extremes_query():
    year = request.args.get('year')
    calculations_results = calculator.find_extremes_for_year(year)
    report = ReportGenerator(calculations_results)
    return render_template("yearly_extremes.html", report=report.get_yearly_extremes_object())


@app.route('/monthly-averages', methods=['GET'])
def monthly_averages_query():
    year = request.args.get('year')
    month = request.args.get('month')
    print(year, month)
    calculation_results = calculator.calculate_month_averages(year, int(month))
    report = ReportGenerator(calculation_results)
    return render_template("monthly_avg.html", report=report.get_month_avg_object())


@app.route('/basic-chart', methods=['GET'])
def basic_chart_query():
    year = request.args.get('year')
    month = request.args.get('month')
    calculation_results = calculator.populate_temp_extremes_for_month(
        int(year), int(month))
    report = ReportGenerator(calculation_results)
    return render_template('basic_chart.html', data=report.get_month_extremes_data())


@ app.route('/net-chart', methods=['GET'])
def net_chart_query():
    year = request.args.get('year')
    month = request.args.get('month')
    calculation_results = calculator.populate_temp_extremes_for_month(
        int(year), int(month))
    report = ReportGenerator(calculation_results)
    return report.print_net_month_extremes_bar_chart()


USERS_FILE = 'users.json'


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return []


def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    # if the request is POST, then the form has been submitted
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']

        users = load_users()

        users.append({
            'name': name,
            'email': email,
            'age': age
        })

        save_users(users)

        return redirect(url_for('create_user'))
    # if the request is GET, then the form should be rendered
    return render_template('create_user.html')


@app.route('/show_users', methods=['GET'])
def show_users():
    users = load_users()
    return render_template('show_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
