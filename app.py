from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sex = request.form["sex"]
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        age = int(request.form["age"])
        goal = request.form["goal"]
        schedule = generate_diet_plan(sex, height, weight, age, goal)
        return render_template("result.html", schedule=schedule)
    else:
        return render_template("form.html")

def generate_diet_plan(sex, height, weight, age, goal):
    # 基礎代謝計算
    if sex == "male":
        bmr = 13.397*weight + 4.799*height - 5.677*age + 88.362
    else:
        bmr = 9.247*weight + 3.098*height - 4.330*age + 447.593

    tdee = bmr * 1.5

    if goal == "macho":
        calorie = tdee + 400
        protein = int(weight * 2.0)
        meals = [
            {"name": "朝食", "menu": "オートミール・スクランブルエッグ・プロテインドリンク"},
            {"name": "昼食", "menu": "鶏胸肉・ブロッコリー・さつまいも・サラダ"},
            {"name": "夕食", "menu": "牛赤身ステーキ・玄米・温野菜"}
        ]
    elif goal == "fitmacho":
        calorie = tdee + 100
        protein = int(weight * 1.5)
        meals = [
            {"name": "朝食", "menu": "ヨーグルト・バナナ・ゆで卵"},
            {"name": "昼食", "menu": "サラダチキン・オートミール・ミニトマト"},
            {"name": "夕食", "menu": "アジの塩焼き・玄米・味噌汁"}
        ]
    elif goal == "fat":
        calorie = tdee + 700
        protein = int(weight * 1.2)
        meals = [
            {"name": "朝食", "menu": "トースト・ハムエッグ・牛乳"},
            {"name": "昼食", "menu": "豚カツ定食"},
            {"name": "夕食", "menu": "ハンバーグ・ライス・サラダ"}
        ]
    else:
        calorie = tdee
        protein = int(weight)
        meals = [
            {"name": "朝食", "menu": "おにぎり・味噌汁・納豆"},
            {"name": "昼食", "menu": "焼き魚定食"},
            {"name": "夕食", "menu": "鶏の照り焼き・ごはん・野菜炒め"}
        ]
    
    fat = int((calorie * 0.25) / 9)
    carb = int((calorie - (protein*4 + fat*9)) / 4)

    return {"calorie": int(calorie), "protein": protein, "fat": fat, "carb": carb, "meals": meals}

if __name__ == "__main__":
    app.run(debug=True)
