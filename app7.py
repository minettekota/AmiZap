import streamlit as st
import requests

# 楽天APIの設定
RAKUTEN_APP_ID = "1083501311495962220"
RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"

# アプリのタイトル
st.title("20代女性のライフスタイル・美容・健康サポートアプリ")

# 1. ライフスタイルに関するアンケート
st.header("1. ライフスタイル")
schedule = st.radio("日常のスケジュールはどのようなものですか？", 
                    ["忙しい（仕事や勉強で時間がない）", "余裕がある（時間に余裕があり、自由時間が多い）"])

weekend = st.radio("週末の過ごし方は？", 
                   ["アウトドア派（旅行、スポーツなど）", "インドア派（家でリラックスする、本や映画を楽しむ）"])

# 2. 美容・健康に対する関心度
st.header("2. 美容・健康に対する関心度")
beauty_time = st.radio("美容にどのくらい時間をかけていますか？", 
                       ["1日30分未満", "1日1時間程度", "1日1時間以上"])

health_conscious = st.radio("健康に気を使っていますか？", 
                            ["栄養バランスの取れた食事、運動などを意識している", "あまり気にしていない"])

# 3. ストレスの感じ方と解消方法
st.header("3. ストレスの感じ方と解消方法")
stress_level = st.radio("普段、どのくらいストレスを感じていますか？", 
                        ["高い（常にストレスを感じている）", "中程度（時々ストレスを感じる）", "低い（あまりストレスを感じない）"])

stress_relief = st.radio("ストレス解消方法は？", 
                         ["ショッピングや美容サービスの利用", "友人と過ごす", "一人で過ごす", "運動やアウトドア活動"])

# 4. ファッション・トレンドへの関心度
st.header("4. ファッション・トレンドへの関心度")
fashion_sensitivity = st.radio("ファッションやトレンドに敏感ですか？", 
                               ["非常に敏感", "まあまあ敏感", "あまり気にしない"])

fashion_purchase_frequency = st.radio("どのくらいの頻度でファッションアイテムを購入しますか？", 
                                      ["毎月", "3か月に一度", "年に数回"])

# 5. 予算
st.header("5. 予算")
budget = st.radio("美容やリラクゼーションにどれくらいの予算をかけていますか？", 
                  ["1万円未満", "1万円〜3万円", "3万円以上"])

# アンケート結果に基づく楽天APIリクエスト
if st.button("結果を表示"):
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
            
            st.image(item_image, caption=item_name, use_column_width=True)
            st.write(f"価格: ¥{item_price}")
            st.write(f"[楽天で見る]({item_url})")
            st.write("---")
    else:
        st.write("おすすめの商品が見つかりませんでした。")
