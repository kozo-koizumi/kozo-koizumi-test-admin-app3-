# admin.py
import streamlit as st
from supabase import create_client, Client

# ===============================
# --- Supabase 設定 ---
# ===============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# ===============================
# --- 固定管理者ログイン ---
# ===============================
ADMIN_ID = st.secrets["ADMIN_ID"]
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- ログイン画面 ---
if not st.session_state.logged_in:
    st.title("管理者ログイン")
    user_input = st.text_input("ユーザーID")
    pass_input = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if user_input == ADMIN_ID and pass_input == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("ログイン成功")
            st.rerun()
        else:
            st.error("ログイン失敗")
    st.stop()

# ===============================
# --- 注文一覧画面 ---
# ===============================

import streamlit as st
from supabase import create_client, Client

# Supabase 設定
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("パンツ採寸入力（ウエスト・丈）")

# 受付番号入力
order_id_input = st.number_input(
    "受付番号を入力してください",
    min_value=1,
    step=1
)

if st.button("検索"):
    res = supabase.table("orders").select("*").eq("id", order_id_input).single().execute()
    st.session_state.order = res.data if res.data else None

order = st.session_state.get("order")

if order:
    st.success("注文が見つかりました")
    st.write(f"名前: {order.get('name')}")
    st.write(f"住所: {order.get('address')}")

    # パンツ情報フォーム
    with st.form("pants_form"):
        waist = st.number_input("パンツ ウエスト(cm)", value=order.get("pants_waist") or 0)
        length = st.number_input("パンツ 丈(cm)", value=int(order.get("pants_length") or 0))
        memo = st.text_input("備考", value=order.get("pants_memo") or "")

        submitted = st.form_submit_button("保存")

        if submitted:
            # 更新
            supabase.table("orders").update({
                "pants_waist": waist,
                "pants_length": length,
                "pants_memo": memo
            }).eq("id", order["id"]).execute()

            st.success("パンツ採寸を更新しました")

"""
st.title("注文一覧（管理画面）")

# Supabase から注文を取得
res = supabase.table("orders").select("*").order("id", desc=True).execute()
orders = res.data or []

if not orders:
    st.info("まだ注文はありません。")
else:
    for order in orders:
        # --- 基本情報 ---
        order_id = order.get("id", "不明")
        name = order.get("name") or "不明"
        total_raw = order.get("total_price", 0)

        try:
            total_int = int(total_raw)
        except (ValueError, TypeError):
            total_int = 0

        with st.expander(f"受付ID: {order_id} - {name} - {total_int:,}円"):
            st.write(f"名前: {name}")
            st.write(f"郵便番号: {order.get('zipcode') or '未入力'}")
            st.write(f"住所: {order.get('address') or '未入力'}")
            st.write(f"電話: {order.get('phone') or '未入力'}")
            st.write(f"メール: {order.get('email') or '未入力'}")

            st.write("【注文商品】")

            has_item = False
            for item in ["shirt", "pants", "socks"]:
                try:
                    qty = int(order.get(item, 0))
                except (ValueError, TypeError):
                    qty = 0

                if qty > 0:
                    has_item = True
                    size = order.get(f"{item}_size") or "未指定"
                    memo = order.get(f"{item}_memo") or ""
                    memo_text = f" / 備考: {memo}" if memo else ""

                    st.write(
                        f"{item.capitalize()}: {qty}点 ({size}){memo_text}"
                    )

            if not has_item:
                st.write("商品なし")

            st.write(f"合計: {total_int:,}円")
"""
