from flask import Flask, jsonify
from flask_caching import Cache
from holidays import country_holidays
from desc import get_description_for

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
cache = Cache(app=app)

def formatHelper(n: int): 
  return f"0{n}" if n < 10 else str(n)

@app.route("/api/holidays/<string:country>/<int:year>", methods=["GET"])
@cache.cached(timeout=300) # 300 seconds
def getHolidays(country: str, year: int):
    from flask import request

    country = country.upper()
    subdiv = request.args.get("sub")
    subdiv = subdiv.upper() if subdiv else subdiv

    hols = country_holidays(country=country, subdiv=subdiv, years=[year])

    results = {}

    for date, name in hols.items():
        results[str(f"{formatHelper(date.year)}-{formatHelper(date.month)}-{formatHelper(date.day)}")] = {
            'name': name,
            'description': get_description_for(name)
        }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=False)
