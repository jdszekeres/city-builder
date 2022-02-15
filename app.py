import re
from flask import *
import db
import helper
import traceback

app = Flask(__name__)
app.secret_key = "134765434 4543"
possible_buildings = [
    ("road", 10),
    ("house", 50),
    ("apartment", 300),
    ("park", 1000),
    ("factory", 2500),
    ("skyscraper", 7000),
    ("train depot", 1000000),
    ("car showroom", 100000000),
    ("PeaR Store", 5000000000),
    ("zoo", 1000000000000),
    ("beach", 200000000000000),
    ("airport", 1000000000000000),
    ('bunker', 10000000000000000000)
]


@app.route("/favicon.ico")
def icon_favicon():
    return send_from_directory("static", "favicon.ico")


@app.route("/")
def index():
    if "user" in session:
        sel = request.args.get("selected")
        noti = request.args.get("notifications")
        sign = ""
        data = db.get_info(db.get_rowid(session["user"]))
        buildings = helper.load_buildings(data["buildings"])
        data["money"] = helper.human_format(round(data["money"], 2))

        return render_template(
            "index.html",
            data=data,
            buildings=buildings,
            pb=possible_buildings,
            sign=sign,
            selected=sel,
            notifications=noti,
            mode=db.get_mode(session["user"])
        )
    else:
        return redirect("/signup")


@app.route("/signup", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db.create_user(request.form["name"], request.form["password"])
        session["user"] = request.form["name"]
        return redirect("/?notifications=welcome")
    return render_template("login.html", name="Signup")


@app.route("/login", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            rid = db.get_rowid(request.form["name"])
            if db.getalldata(rid)[1] == request.form["password"]:
                
                if db.get_mode(request.form["name"]) == None:
                    db.set_modex(request.form["name"])
                session["user"] = request.form["name"]
                return redirect("/")
            else:
                return "incorrect password"
        except Exception as e:
            traceback.print_exc()
            print(e)
            return "No account found"

    return render_template("login.html", name="login")


@app.route("/buy/<building>/<x>/<y>")
def buy(building, x, y):
    building = helper.get_building(possible_buildings, building)
    d = db.buy(
        building[1], building[0], db.get_rowid(session["user"]), (int(x), int(y))
    )
    if d == "500":
        return redirect(
            "/?notifications=failed%20to%20purchase%20building&selected={}".format(
                building[0]
            )
        )
    if d != None:
        add = "&notifications={d}".format(d=d)
    else:
        add = ""
    return redirect("/?selected={0}{1}".format(building[0], add))


@app.route("/day/<build>")
def day(build):
    b = db.add_day(db.get_rowid(session["user"]), possible_buildings)
    if b != None:
        add = "&notifications={}".format(b)
    else:
        add = ""
    return redirect("/?selected={0}{1}".format(build, add))


@app.route("/sell/<x>/<y>/<build>")
def sell(x, y, build):
    db.sell(db.get_rowid(session["user"]), (int(x), int(y)), possible_buildings)
    return redirect("/?selected={}".format(build))
@app.route("/color/<out>")
def dark_mode(out):
    db.set_mode(session["user"], out)
    return redirect("/")
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(fmt=helper.human_format)
app.run(debug=True, host="0.0.0.0", port=6870)
