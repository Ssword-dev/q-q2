from flask import Flask, jsonify
from holidays import country_holidays
import datetime

app = Flask(__name__)

@app.route("/api/holidays/<string:country>/<int:year>", methods=["GET"])
def getHolidays(country: str, year: int):
    from flask import request

    country = country.upper()
    subdiv = request.args.get("sub")
    subdiv = subdiv.upper() if subdiv else subdiv

    hols = country_holidays(country=country, subdiv=subdiv, years=[year])

    results = {}

    for date, name in hols.items():
        results[str(f"{date.year}-{date.month}-{date.day}")] = name

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=False)
