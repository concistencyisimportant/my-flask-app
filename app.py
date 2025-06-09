def generate_diet_plan(sex, height, weight, age, goal):
    # ...（カロリー計算部分は省略、あなたのロジックを使ってOK）
    days = ["月", "火", "水", "木", "金", "土", "日"]
    breakfasts = [
        "オートミールと卵",
        "トースト・ヨーグルト",
        "ごはん・納豆・味噌汁",
        "バナナ・プロテインシェイク",
        "パン・ハム・チーズ",
        "シリアル・牛乳",
        "果物・ゆで卵"
    ]
    lunches = [
        "鶏胸肉弁当",
        "サラダチキン・玄米",
        "魚定食",
        "牛丼・サラダ",
        "豚しょうが焼き",
        "鯖の味噌煮定食",
        "野菜カレー"
    ]
    dinners = [
        "牛赤身ステーキ・ブロッコリー",
        "鶏の照り焼き・ごはん",
        "焼き魚・野菜炒め",
        "豚しゃぶサラダ",
        "ミートボール・パスタ",
        "ハンバーグ・温野菜",
        "タラのムニエル"
    ]

    week_menu = []
    for i in range(7):
        week_menu.append({
            "day": days[i],
            "breakfast": breakfasts[i],
            "lunch": lunches[i],
            "dinner": dinners[i]
        })
    return {
        "calorie": 2500, # 計算に差し替えて
        "protein": 150,
        "fat": 50,
        "carb": 350,
        "week_menu": week_menu
    }
