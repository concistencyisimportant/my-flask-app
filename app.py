from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "4c93f79a"

# 日本語→英語メニュー変換辞書（必要に応じて増やして！）
menu_jp_to_en = {
    "オートミールと卵": "oatmeal and egg",
    "トースト・ヨーグルト": "toast and yogurt",
    "果物・ゆで卵": "fruit and boiled egg",
    "パン・ハム・チーズ": "bread, ham and cheese",
    "牛丼": "beef bowl",
    "サラダチキン・玄米": "chicken salad and brown rice",
    "鶏胸肉弁当": "chicken breast bento",
    "魚定食": "grilled fish set meal",
    "焼き魚・野菜炒め": "grilled fish and stir fried vegetables",
    "ハンバーグ": "hamburger steak",
}

def get_calorie(menu_jp):
    menu_en = menu_jp_to_en.get(menu_jp, menu_jp)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": "4c93f79a",        # これを追加！
        "x-app-key": "50ba46ef84f89d4dcca50d21431bc29a",
        "Content-Type": "application/json"
    }
    data = {"query": menu_en}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"API send: {menu_en}, status: {r.status_code}, response: {r.text}")
        if r.status_code != 200:
            return None
        foods = r.json().get("foods", [])
        if foods and "nf_calories" in foods[0]:
            return int(foods[0]['nf_calories'])
    except Exception as e:
        print("API error:", e)
    return None

def generate_diet_plan(sex, height, weight, age, goal):
    days = ["月", "火", "水", "木", "金", "土", "日"]
    breakfasts = [
        "オートミールと卵", "トースト・ヨーグルト", "果物・ゆで卵",
        "パン・ハム・チーズ", "オートミールと卵", "トースト・ヨーグルト", "パン・ハム・チーズ"
    ]
    lunches = [
        "牛丼", "サラダチキン・玄米", "鶏胸肉弁当",
        "魚定食", "牛丼", "サラダチキン・玄米", "鶏胸肉弁当"
    ]
    dinners = [
        "ハンバーグ", "焼き魚・野菜炒め", "ハンバーグ",
        "焼き魚・野菜炒め", "ハンバーグ", "焼き魚・野菜炒め", "ハンバーグ"
    ]
    week_menu = []
    for i in range(7):
        b, l, d = breakfasts[i], lunches[i], dinners[i]
        b_kcal = get_calorie(b)
        l_kcal = get_calorie(l)
        d_kcal = get_calorie(d)
        day_total = sum(x for x in [b_kcal, l_kcal, d_kcal] if x is not None)
        week_menu.append({
            "day": days[i],
            "breakfast": b, "b_kcal": b_kcal,
            "lunch": l, "l_kcal": l_kcal,
            "dinner": d, "d_kcal": d_kcal,
            "total": day_total
        })
    return {"week_menu": week_menu}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sex = request.form.get("sex", "")
        height = float(request.form.get("height", 0))
        weight = float(request.form.get("weight", 0))
        age = int(request.form.get("age", 0))
        goal = request.form.get("goal", "") 
        schedule = generate_diet_plan(sex, height, weight, age, goal)
        return render_template("result.html", schedule=schedule)
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
