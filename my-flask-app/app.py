
# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 入力データの取得
        sex = request.form["sex"]
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        age = int(request.form["age"])
        goal = request.form["goal"]
        # 食事プランを計算
        schedule = generate_diet_plan(sex, height, weight, age, goal)
        return render_template("result.html", schedule=schedule)
    else:
        return render_template("form.html")

def generate_diet_plan(sex, height, weight, age, goal):
    # ここで食事プランを生成（後述）
    return {
        "calorie": 2500,
        "protein": 150,
        "fat": 50,
        "carb": 350,
        # おすすめメニューなど
        "meals": [
            {"name": "朝食", "menu":"鶏胸肉と玄米"},
            {"name": "昼食", "menu":"サラダチキンとさつまいも"},
            {"name": "夕食", "menu":"牛赤身ステーキとブロッコリー"}
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)
def generate_diet_plan(sex, height, weight, age, goal):
    # 基礎代謝計算
    if sex == "male":
        bmr = 13.397*weight + 4.799*height - 5.677*age + 88.362
    else:
        bmr = 9.247*weight + 3.098*height - 4.330*age + 447.593

    # 総消費カロリーは仮に1.5倍
    tdee = bmr * 1.5

    # 目標によるカロリーバランス
    if goal == "macho":
        calorie = tdee + 400
        protein = int(weight * 2.0)
    elif goal == "fitmacho":
        calorie = tdee + 100
        protein = int(weight * 1.5)
    elif goal == "fat":
        calorie = tdee + 700
        protein = int(weight * 1.2)
    else:
        calorie = tdee
        protein = int(weight)
    
    fat = int((calorie * 0.25) / 9)
    carb = int((calorie - (protein*4 + fat*9)) / 4)

    # サンプルメニューはご自由に
    meals = [
        {"name": "朝食", "menu":"○○○"},
        {"name": "昼食", "menu":"△△△"},
        {"name": "夕食", "menu":"□□□"}
    ]
    return {"calorie": int(calorie), "protein": protein, "fat": fat, "carb": carb, "meals": meals}
