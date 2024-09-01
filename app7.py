import streamlit as st
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import datetime

# 楽天APIの設定
RAKUTEN_APP_ID = st.secrets["rakuten"]["app_id"]
RAKUTEN_API_URL = st.secrets["rakuten"]["api_url"]


# アプリのタイトル
st.title("20代女性のライフスタイル・美容・健康サポートアプリ")

#サイドバーにイメージを表示(UI変更で追加)
image_path = "amizaplogo.png" # ローカルファイルのパスを指定
caption_text = "いつも頑張っているあなたへ<br>日常生活の隙間に<br>ちょこっと素敵なサービスをお届け"
st.sidebar.image(image_path, use_column_width=True)
st.sidebar.markdown("**いつも頑張っているあなたへ**\n\n**日常生活の隙間に**\n\n**ちょこっと素敵なサービスをお届け**\n\n")

# ※１：以下、アンケートをサイドバーに表示（UI変更で追加）
# セッションステートを利用してアンケートの解答を保持
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# サイドバーにリセットボタンを追加
if st.sidebar.button("アンケートをリセット"):
    # アンケートの回答をリセット
    st.session_state.submitted = False
    st.session_state.schedule = None
    st.session_state.weekend = None
    st.session_state.beauty_time = None
    st.session_state.health_conscious = None
    st.session_state.stress_level = None
    st.session_state.stress_relief = None
    st.session_state.fashion_sensitivity = None
    st.session_state.fashion_purchase_frequency = None
    st.session_state.budget = None
    st.session_state.show_results = None # ← 右側の結果もリセットするために加えました
    st.sidebar.write("アンケートがリセットされました")

# サイドバーに名前を入力
name = st.sidebar.text_input("お名前を教えてください")
# ※１：以上、アンケートをサイドバーに表示（UI変更で追加）

# ※２：以下、アンケートをサイドバーに表示＆回答変更後結果表示ボタンを明示的に押す仕様に変更（UI変更で修正）
# 名前が入力され、まだアンケートが提出されていない場合のみ質問を表示
if name and not st.session_state.submitted:
    st.sidebar.write(f"{name}さん、アンケートにお答えください。")

    # 1. ライフスタイルに関するアンケート
    with st.sidebar.expander("1. ライフスタイルに関するアンケート"):
        schedule = st.radio("日常のスケジュールはどのようなものですか？", 
                            ["忙しい（仕事や勉強で時間がない）", "余裕がある（時間に余裕があり、自由時間が多い）"],
                            on_change=lambda: st.session_state.update(show_results=False))

        weekend = st.radio("週末の過ごし方は？", 
                        ["アウトドア派（旅行、スポーツなど）", "インドア派（家でリラックスする、本や映画を楽しむ）"],
                        on_change=lambda: st.session_state.update(show_results=False))

    # 2. 美容・健康に対する関心度
    with st.sidebar.expander("2. 美容・健康に対する関心度"):
        beauty_time = st.radio("美容にどのくらい時間をかけていますか？", 
                            ["1日30分未満", "1日1時間程度", "1日1時間以上"],
                            on_change=lambda: st.session_state.update(show_results=False))

        health_conscious = st.radio("健康に気を使っていますか？", 
                                    ["栄養バランスの取れた食事、運動などを意識している", "あまり気にしていない"],
                                    on_change=lambda: st.session_state.update(show_results=False))

    # 3. ストレスの感じ方と解消方法
    with st.sidebar.expander("3. ストレスの感じ方と解消方法"):
        stress_level = st.radio("普段、どのくらいストレスを感じていますか？", 
                                ["高い（常にストレスを感じている）", "中程度（時々ストレスを感じる）", "低い（あまりストレスを感じない）"],
                                on_change=lambda: st.session_state.update(show_results=False))

        stress_relief = st.radio("ストレス解消方法は？", 
                                ["ショッピングや美容サービスの利用", "友人と過ごす", "一人で過ごす", "運動やアウトドア活動"],
                                on_change=lambda: st.session_state.update(show_results=False))

    # 4. ファッション・トレンドへの関心度
    with st.sidebar.expander("4. ファッション・トレンドへの関心度"):
        fashion_sensitivity = st.radio("ファッションやトレンドに敏感ですか？", 
                                    ["非常に敏感", "まあまあ敏感", "あまり気にしない"],
                                    on_change=lambda: st.session_state.update(show_results=False))

        fashion_purchase_frequency = st.radio("どのくらいの頻度でファッションアイテムを購入しますか？", 
                                            ["毎月", "3か月に一度", "年に数回"],
                                            on_change=lambda: st.session_state.update(show_results=False))

    # 5. 予算
    with st.sidebar.expander("5. 予算"):
        budget = st.radio("美容やリラクゼーションにどれくらいの予算をかけていますか？", 
                        ["1万円未満", "1万円〜3万円", "3万円以上"],
                        on_change=lambda: st.session_state.update(show_results=False))

    # アンケート保存ボタン
    if st.sidebar.button("アンケートを保存"):
        # セッションに回答を保存
        st.session_state.submitted = True
        st.session_state.schedule = schedule
        st.session_state.weekend = weekend
        st.session_state.beauty_time = beauty_time
        st.session_state.health_conscious = health_conscious
        st.session_state.stress_level = stress_level
        st.session_state.stress_relief = stress_relief
        st.session_state.fashion_sensitivity = fashion_sensitivity
        st.session_state.fashion_purchase_frequency = fashion_purchase_frequency
        st.session_state.budget = budget
        st.sidebar.write("アンケートを保存しました")
else:
    if st.session_state.submitted:
        st.sidebar.write("アンケートは既に解答済みです。")
    else:
        st.sidebar.write("お名前を入力してください。")
# ※２：以上、アンケートをサイドバーに表示＆回答変更後結果表示ボタンを明示的に押す仕様に変更（UI変更で修正）

# （新たに追加）セッション状態の初期化
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# （修正done）アンケート結果に基づく楽天APIリクエスト
if st.button("結果を表示"):
    st.session_state.show_results = True

if st.session_state.show_results:
    #  セッションから回答を取得（UI変更で追加）
    if st.session_state.submitted:
        schedule = st.session_state.get('schedule', None)
        weekend = st.session_state.get('weekend', None)
        health_conscious = st.session_state.get('health_conscious', None)

    # リクエストパラメータを設定
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "keyword": "美容",
        "genreId": "100939",  # 美容ジャンル
        "minPrice": 1000,  # 価格フィルタ
        "maxPrice": 3000,
        "hits": 5,  # 表示件数
    }
    
    if "忙しい" in schedule:
        params["keyword"] = "時短美容"
    elif "アウトドア" in weekend:
        params["keyword"] = "アウトドアスキンケア"
    elif "健康" in health_conscious:
        params["keyword"] = "健康食品"
    
    # 楽天APIへのリクエスト
    response = requests.get(RAKUTEN_API_URL, params=params)
    items = response.json().get("Items", [])
    
    if items:
        st.header("あなたにおすすめの商品")
        for item in items:
            item_name = item["Item"]["itemName"]
            item_price = item["Item"]["itemPrice"]
            item_url = item["Item"]["itemUrl"]
            item_image = item["Item"]["mediumImageUrls"][0]["imageUrl"]  # 商品画像
            
            st.image(item_image, caption=item_name, use_column_width=False, width=500)
            st.write(f"価格: ¥{item_price}")
            st.write(f"[楽天で見る]({item_url})")
            st.write("---")

        # のむりんパート（最寄り店舗表示と予約）
        # PCの現在位置を取得
        def get_current_location():
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            return data['lat'], data['lon']

        # AmiZAP店舗リストの取得（仮定としてリストを用意）
        AmiZAP_locations = [
            {"name": "AmiZAP 渋谷", "lat": 35.658638663313766, "lon": 139.70382998499045},
            {"name": "AmiZAP 新宿", "lat": 35.6917090657765, "lon": 139.7057630257946},
            {"name": "AmiZAP 池袋", "lat": 35.73640163107946, "lon": 139.7200809914018335},
            {"name": "AmiZAP 銀座", "lat": 35.67248911726671, "lon": 139.76208100992432},
            {"name": "AmiZAP 神田", "lat": 35.69299106458599, "lon": 139.7711483902126},
            {"name": "AmiZAP 大井町", "lat": 35.60401857110624, "lon": 139.73588310317834},
            {"name": "AmiZAP 新高島平", "lat": 35.79191129625125, "lon": 139.6559264947171},
            {"name": "AmiZAP 日暮里", "lat": 35.72895751461521, "lon": 139.78276413624502},
            {"name": "AmiZAP 亀有", "lat": 35.76835745222231, "lon": 139.84745676454548},
            {"name": "AmiZAP 荻窪", "lat": 35.704733409781014, "lon": 139.61784132275315},
            # 他の店舗の情報を追加...
        ]

        # 最寄りのAmiZAPを検索
        def find_nearest_amizap(current_location, locations):
            nearest_location = None
            min_distance = float('inf')

            for location in locations:
                distance = geodesic(current_location, (location["lat"], location["lon"])).km
                if distance < min_distance:
                    nearest_location = location
                    min_distance = distance

            return nearest_location, min_distance

        # メイン処理
        if __name__ == "__main__":
            current_location = get_current_location()
            nearest_amizap, distance = find_nearest_amizap(current_location, AmiZAP_locations)

            if nearest_amizap:
                st.write(f"最寄りのAmiZAP は {nearest_amizap['name']}店で、距離は {distance:.2f} km です。")
    

        # 現在位置と最寄りの店舗の情報をデータフレームにまとめる
                map_data = pd.DataFrame(
                    [
                
                        {"lat": nearest_amizap["lat"], "lon": nearest_amizap["lon"], "name": nearest_amizap["name"]}
                    ]
                )
        
                # 地図を表示
                st.map(map_data, size=100, zoom=13)
            else:
                st.write("AmiZAPの店舗が見つかりませんでした。")

        # 時間の予約
        t = st.time_input("ご予約をお取りしますか？", datetime.time(10, 00))
        result = st.button("予約する")

        if result:
            st.write(t, f"で {nearest_amizap['name']}店のご予約を承りました！")

    else:
        st.write("おすすめの商品が見つかりませんでした。")

