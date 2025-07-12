# oidcheck/server.py
from flask import Flask, render_template, request
from .validator import validate_config
from .models import AppConfig

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    config_text = ""
    if request.method == "POST":
        config_text = request.form.get("config", "")
        
        config_dict = {}
        for line in config_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                config_dict[key.strip()] = value.strip()

        config = AppConfig.parse_obj(config_dict)
        results = validate_config(config)

    return render_template("index.html", results=results, config_text=config_text)

if __name__ == "__main__":
    app.run(debug=True)