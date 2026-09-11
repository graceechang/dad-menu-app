import streamlit as st
import random
import datetime

# 設定資料庫
data = [
    {"name": "蔬菜蛋餅", "type": "早餐", "protein": 8},
    {"name": "無糖豆漿 + 蒸南瓜", "type": "早餐", "protein": 10},
    {"name": "水煮蛋 + 低蛋白麵包", "type": "早餐", "protein": 9},
    {"name": "冬粉炒蛋絲", "type": "早餐", "protein": 8},
    {"name": "瘦肉粥", "type": "早餐", "protein": 10},
    {"name": "全麥饅頭夾蛋", "type": "早餐", "protein": 13},
    {"name": "清蒸薑絲魚片", "type": "主菜", "protein": 10},
    {"name": "蒜泥白肉 (瘦肉)", "type": "主菜", "protein": 10},
    {"name": "清蒸蝦仁 (5-6隻)", "type": "主菜", "protein": 12},
    {"name": "板豆腐炒木耳", "type": "主菜", "protein": 12},
    {"name": "香煎雞胸肉", "type": "主菜", "protein": 12},
    {"name": "蛤蜊絲瓜", "type": "主菜", "protein": 8},
    {"name": "洋蔥炒蛋", "type": "主菜", "protein": 10},
    {"name": "清炒高麗菜", "type": "配菜", "protein": 1.5},
    {"name": "蒜炒小黃瓜", "type": "配菜", "protein": 1},
    {"name": "螞蟻上樹 (純冬粉)", "type": "配菜", "protein": 0.5},
    {"name": "炒白蘿蔔絲", "type": "配菜", "protein": 1},
    {"name": "冬瓜清湯", "type": "配菜", "protein": 1},
    {"name": "玉米鬚水", "type": "配菜", "protein": 0.5},
    {"name": "薑絲蛤蜊湯", "type": "配菜", "protein": 2}
]

st.title("🛡️ 爸爸的菜單抽籤器")

# 判斷是否為週末
weekday = datetime.datetime.now().weekday()
is_weekend = weekday >= 5

# 使用 Session State 來儲存抽出的結果，這樣「重抽單項」時其他項才不會動
if 'menu' not in st.session_state:
    st.session_state.menu = {
        "早餐": random.choice([d for d in data if d["type"] == "早餐"]),
        "午餐": random.choice([d for d in data if d["type"] == "主菜"]) if is_weekend else {"name": "外食健康餐 (選白肉)", "protein": 15},
        "晚餐": random.choice([d for d in data if d["type"] == "主菜"]),
        "配菜": random.choice([d for d in data if d["type"] == "配菜"])
    }

# 顯示介面
cols = st.columns(2)

for i, (meal_time, item) in enumerate(st.session_state.menu.items()):
    with cols[i % 2]:
        st.subheader(meal_time)
        st.info(f"🍴 {item['name']}\n\n**蛋白質: {item['protein']}g**")
        if st.button(f"🔄 換個{meal_time}", key=meal_time):
            if meal_time == "午餐" and not is_weekend:
                st.warning("平日午餐建議外食喔！")
            else:
                # 重新抽籤邏輯
                pool = [d for d in data if d["type"] == ("早餐" if meal_time == "早餐" else "主菜" if "餐" in meal_time else "配菜")]
                st.session_state.menu[meal_time] = random.choice(pool)
                st.rerun()

# 計算總量
total_p = sum(item['protein'] for item in st.session_state.menu.values())
st.divider()
delta_value = total_p - 50
st.metric("今日預估蛋白質總含量", f"{total_p} g", delta= delta_value, delta_color="inverse")