from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# NutritionixのAPI情報
APP_ID  = ""                    # App IDは空欄でも動くことが多いですが、本来は取得推奨
API_KEY = "4c93f79a"

# 日本語→英語の対応表は増やしましょう
menu_jp_to_en = {
    "オートミールと卵": "oatmeal and egg",
    "トースト・ヨーグルト": "toast and yogurt",
    "牛丼": "beef bowl",
    "サラダチキン・玄米": "chicken salad and brown rice",
    "魚定食": "grilled fish set meal",
    "鶏胸肉弁当": "chicken breast bento",
    "パン・ハム・チーズ": "bread, ham and cheese",
    "焼き魚・野菜炒め": "grilled fish and stir fried vegetables",
    "ハンバーグ": "hamburger steak",
    "果物・ゆで卵": "fruit and boiled egg",
    # 必要に応じて追加
}

def get_calorie(menu_jp):
    menu_en = menu_jp_to_en.get(menu_jp, menu_jp)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-key": API_KEY,
        # "x-app-id": APP_ID,   # 必要な場合はここにも入れてください
        "Content-Type": "application/json"
    }
    data = {"query": menu_en}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=5)
        if not r.ok:
            return None
        result = r.json()
        foods = result.get("foods", [])
        if foods:
            return int(foods[0]["nf_calories"])
    except Exception as e:
        print("API ERROR:", e)
    return None

def generate_diet_plan(sex, height, weight, age, goal):
    days = ["月", "火", "水", "木", "金", "土", "日"]
    breakfasts = [
        "オートミールと卵",
        "トースト・ヨーグルト",
        "果物・ゆで卵",
        "パン・ハム・チーズ",
        "オートミールと卵",
        "トースト・ヨーグルト",
        "パン・ハム・チーズ"
    ]
    lunches = [
        "牛丼",
        "サラダチキン・玄米",
        "鶏胸肉弁当",
        "魚定食",
        "牛丼",
        "サラダチキン・玄米",
        "鶏胸肉弁当"
    ]
    dinners = [
        "ハンバーグ",
        "焼き魚・野菜炒め",
        "ハンバーグ",
        "焼き魚・野菜炒め",
        "ハンバーグ",
        "焼き魚・野菜炒め",
        "ハンバーグ"
    ]

    week_menu = []
    for i in range(7):
        b, l, d = breakfasts[i], lunches[i], dinners[i]
        b_kcal = get_calorie(b)
        l_kcal = get_calorie(l)
        d_kcal = get_calorie(d)
        total = sum(x for x in [b_kcal, l_kcal, d_kcal] if x)
        week_menu.append({
            "day": days[i],
            "breakfast": b, "b_kcal": b_kcal,
            "lunch": l, "l_kcal": l_kcal,
            "dinner": d, "d_kcal": d_kcal,
            "total": total
        })
    return {"week_menu": week_menu}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sex = request.form.get("sex","")
        height = float(request.form.get("height",0))
        weight = float(request.form.get("weight",0))
        age = int(request.form.get("age",0))
        goal = request.form.get("goal","")
        schedule = generate_diet_plan(sex, height, weight, age, goal)
        return render_template("result.html", schedule=schedule)
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
