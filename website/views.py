from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from .models import WeeklyData, db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from datetime import datetime

my_view = Blueprint("my_view", __name__)

@my_view.route('/')
def home():
    weekly_data = WeeklyData.query.all()
    generate_weekly_income_chart(weekly_data)
    return render_template('webapp.html', weekly_data=weekly_data)

def generate_weekly_income_chart(weekly_data):
    weeks = [data.day for data in weekly_data]
    total_cost = [data.total_cost for data in weekly_data]
    weekly_totals = defaultdict(float)
    for data in weekly_data:
        weekly_totals[data.day] += data.total_cost
        days = list(weekly_totals.keys())
    total_costs = list(weekly_totals.values())
    mvps = [data.most_popular_staff for data in weekly_data if data.most_popular_staff]
    mvp_counts = Counter(mvps)
    staff_names = list(mvp_counts.keys())
    staff_counts = list(mvp_counts.values())

    plt.figure(figsize=(8, 6))
    plt.pie(staff_counts, labels=staff_names, autopct='%1.1f%%', startangle=140)
    plt.title('Most Valuable Staff Members (MVPs)')
    plt.axis('equal')

    plt.savefig("website/static/mvp_pie_chart.png", format='png')

    plt.clf()


    plt.bar(weeks, total_cost, color='skyblue')
    plt.xlabel('Week')
    plt.ylabel('Total Cost')
    plt.title('Weekly Total Cost')

    plt.savefig("website/static/mainplot.png", format='png')

    plt.bar(days, total_costs, color='skyblue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Revenue')
    plt.title('Weekly Total Revenue')

    plt.savefig("website/static/weekly_income_chart.png", format='png')
@my_view.route('/weekly_data', methods=['POST'])
def submit_weekly_data():
    day = request.form['day']
    total_items = float(request.form['total_items'])
    most_popular_item = request.form['most_popular_item']
    least_popular_item = request.form['least_popular_item']
    total_cost = float(request.form['total_cost'])
    max_cost = float(request.form['max_cost'])
    min_cost = float(request.form['min_cost'])
    average_cost = float(request.form['average_cost'])
    least_popular_payment = request.form['least_popular_payment']
    most_popular_staff = request.form['most_popular_staff']

    new_weekly_data = WeeklyData(
    day = day,
    total_items = total_items,
    most_popular_item = most_popular_item,
    least_popular_item = least_popular_item,
    total_cost = total_cost,
    max_cost = max_cost,
    min_cost = min_cost,
    average_cost = average_cost,
    least_popular_payment = least_popular_payment,
    most_popular_staff = most_popular_staff
    )

    db.session.add(new_weekly_data)
    db.session.commit()
    weekly_data = WeeklyData.query.all()
    generate_weekly_income_chart(weekly_data)
    return redirect(url_for('my_view.home'))



@my_view.route("/edit/<weeklydata_id>", methods=["POST"])
def edit(weeklydata_id):
    try:
        weekly_data = WeeklyData.query.filter_by(id=weeklydata_id).first()
        edited_day = request.form.get("edited_day")
        weekly_data.day = edited_day
        weekly_data.date_edited = datetime.utcnow()
        db.session.commit()
        message_type = "success"
        message = "Data edited successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while editing data."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))

@my_view.route("/delete/<weeklydata_id>", methods=["POST"])
def delete(weeklydata_id):
    try:
        weekly_data = WeeklyData.query.filter_by(id=weeklydata_id).first()
        db.session.delete(weekly_data)
        db.session.commit()
        message_type = "success"
        message = "Task deleted successfully."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))
    except:
        message_type = "error"
        message = "An error occurred while deleting a task."
        return redirect(url_for("my_view.home", message=message, message_type=message_type))