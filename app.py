from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Nutritionix API 認証情報
API_ID = "4c93f79a"  # ←ご自身のApp IDを入力！
API_KEY = "50ba46ef8f489d4dcca50d21431bc29a"  # ←Appkeyを入力！

# メニュー（日⇔英）対応辞書　（必要に応じて追加！）
menu_jp_to_en = {
    "オートミールと卵": "oatmeal and egg",
    "トースト・ヨーグルト": "toast and yogurt",
    "果物・ゆで卵": "fruit and boiled egg",
    "パン・ハム・チーズ": "bread, ham, and cheese",
    "納豆ご飯": "rice with natto",
    "シリアルとミルク": "cereal and milk",
    "牛丼": "beef bowl",
    "サラダチキン・玄米": "salad chicken and brown rice",
    "鶏胸肉弁当": "chicken breast bento",
    "魚定食": "grilled fish set meal",
    "パスタ": "pasta",
    "野菜炒め定食": "stir-fried vegetables set meal",
    "ハンバーグ": "hamburger steak",
    "焼き魚・野菜炒め": "grilled fish and stir-fried vegetables",
    "麻婆豆腐": "mapo tofu",
    "豚肉生姜焼き": "ginger pork",
    "サバの味噌煮": "miso simmered mackerel",
    "鶏もも照り焼き": "chicken thigh teriyaki",
}

# 朝昼夕の候補
breakfast_candidates = [
    "オートミールと卵", "トースト・ヨーグルト", "果物・ゆで卵",
    "パン・ハム・チーズ", "納豆ご飯", "シリアルとミルク"
]
lunch_candidates = [
    "牛丼", "サラダチキン・玄米", "鶏胸肉弁当",
    "魚定食", "パスタ", "野菜炒め定食"
]
dinner_candidates = [
    "ハンバーグ", "焼き魚・野菜炒め", "麻婆豆腐", "豚肉生姜焼き",
    "サバの味噌煮", "鶏もも照り焼き"
]

# 必要カロリー(TDEE)計算
def calculate_target_calories(sex, height, weight, age, goal):
    # BMR: Harris-Benedict
    if sex == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    tdee = bmr * 1.55  # (普通の活動レベルで固定)
    if goal == "維持":
        return int(tdee)
    elif goal == "減量":
        return int(tdee - 300)
    elif goal == "増量":
        return int(tdee + 300)
    return int(tdee)

# カロリー自動取得（API）
def get_calorie(menu_jp):
    menu_en = menu_jp_to_en.get(menu_jp, menu_jp)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": API_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"query": menu_en}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=10)
        if r.status_code != 200:
            print(f"API error: {r.status_code} {r.text}")
            return None
        foods = r.json().get("foods", [])
        if foods and "nf_calories" in foods[0]:
            return int(foods[0]["nf_calories"])
    except Exception as e:
        print("API error:", e)
    return None

# ランダム献立生成（必要カロリー考慮）
def generate_random_schedule(target_cal):
    days = ["月", "火", "水", "木", "金", "土", "日"]
    # 割合: 朝2.5割、昼3.5割、夜4割
    breakfast_ratio = 0.25
    lunch_ratio = 0.35
    dinner_ratio = 0.40
    week_menu = []
    used_breakfast = []
    used_lunch = []
    used_dinner = []
    for i in range(7):
        # 毎週重複を防ぐ（足りなければシャッフルして再度使う）
        if len(used_breakfast) == len(breakfast_candidates):
            used_breakfast = []
        if len(used_lunch) == len(lunch_candidates):
            used_lunch = []
        if len(used_dinner) == len(dinner_candidates):
            used_dinner = []
        b_choices = [x for x in breakfast_candidates if x not in used_breakfast]
        l_choices = [x for x in lunch_candidates if x not in used_lunch]
        d_choices = [x for x in dinner_candidates if x not in used_dinner]
        breakfast = random.choice(b_choices)
        lunch = random.choice(l_choices)
        dinner = random.choice(d_choices)
        used_breakfast.append(breakfast)
        used_lunch.append(lunch)
        used_dinner.append(dinner)
        # カロリー取得
        b_kcal = get_calorie(breakfast)
        l_kcal = get_calorie(lunch)
        d_kcal = get_calorie(dinner)
        total = sum(x for x in [b_kcal, l_kcal, d_kcal] if x)
        week_menu.append({
            "day": days[i],
            "breakfast": breakfast, "b_kcal": b_kcal, "b_target": int(target_cal * breakfast_ratio),
            "lunch": lunch, "l_kcal": l_kcal, "l_target": int(target_cal * lunch_ratio),
            "dinner": dinner, "d_kcal": d_kcal, "d_target": int(target_cal * dinner_ratio),
            "total": total,
            "target": target_cal
        })
    return week_menu

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sex = request.form.get("sex", "")
        height = float(request.form.get("height", 0))
        weight = float(request.form.get("weight", 0))
        age = int(request.form.get("age", 0))
        goal = request.form.get("goal", "")  # 維持/減量/増量
        target_cal = calculate_target_calories(sex, height, weight, age, goal)
        week_menu = generate_random_schedule(target_cal)
        return render_template("result.html", week_menu=week_menu, target_cal=target_cal)
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
