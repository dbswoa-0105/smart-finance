import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="재민의 스마트 가계부", layout="wide")

class FinanceManager:
    def __init__(self, db_name="finance_final.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finance_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                item TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT
            )
        ''')
        self.conn.commit()

    def add_record(self, date, type, item, amount, category):
        self.cursor.execute('INSERT INTO finance_data (date, type, item, amount, category) VALUES (?, ?, ?, ?, ?)',
                           (date, type, item, amount, category))
        self.conn.commit()

    def update_record(self, r_id, date, r_type, item, amount, category):
        self.cursor.execute('''
            UPDATE finance_data SET date=?, type=?, item=?, amount=?, category=? WHERE id=?
        ''', (date, r_type, item, amount, category, r_id))
        self.conn.commit()

    def delete_record(self, r_id):
        self.cursor.execute('DELETE FROM finance_data WHERE id=?', (r_id,))
        self.conn.commit()

    def get_df(self):
        return pd.read_sql_query("SELECT * FROM finance_data ORDER BY date DESC", self.conn)

ICON_MAP = {
    "식비": "🍱 식비", "교통비": "🚌 교통비", "쇼핑": "🛍️ 쇼핑", 
    "의료": "🏥 의료", "주거": "🏠 주거", "월급": "💰 월급", 
    "알바비": "🍯 알바비", "용돈": "💸 용돈", "기타": "🎸 기타"
}

db = FinanceManager()

st.title("💰 재민의 스마트 가계부")

with st.sidebar:
    st.header("➕ 새 내역 추가")
    s_date = st.date_input("날짜", datetime.now())
    s_type = st.radio("구분", ["지출", "수입"], horizontal=True)
    s_item = st.text_input("항목명")
    s_amount = st.number_input("금액", min_value=0, step=1000)
    cat_list = list(ICON_MAP.keys())
    s_cat_name = st.selectbox("카테고리", cat_list, key="add_cat")
    s_cat = ICON_MAP.get(s_cat_name)

    if st.button("저장하기", use_container_width=True):
        if s_item and s_amount > 0:
            db.add_record(s_date.strftime("%Y-%m-%d"), s_type, s_item, s_amount, s_cat)
            st.rerun()

df = db.get_df()

if not df.empty:
    income = df[df['type'] == '수입']['amount'].sum()
    expense = df[df['type'] == '지출']['amount'].sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("총 수입", f"{income:,}원")
    c2.metric("총 지출", f"{expense:,}원")
    c3.metric("현재 잔액", f"{income - expense:,}원")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("📊 카테고리별 지출 비중")
        exp_df = df[df['type'] == '지출']
        if not exp_df.empty:
            st.bar_chart(exp_df.groupby('category')['amount'].sum())
        else:
            st.write("지출 내역이 없습니다.")
            
    with col_chart2:
        st.subheader("📈 일자별 자금 흐름")
        st.line_chart(df.groupby('date')['amount'].sum())

    st.divider()
    with st.expander("🛠️ 내역 수정 및 삭제하기"):
        col_id, col_edit = st.columns([1, 3])
        with col_id:
            edit_id = st.selectbox("수정/삭제할 ID", df['id'].tolist())
            target = df[df['id'] == edit_id].iloc[0]
        
        with col_edit:
            e_date = st.date_input("수정 날짜", datetime.strptime(target['date'], "%Y-%m-%d"))
            e_type = st.selectbox("수정 구분", ["지출", "수입"], index=0 if target['type']=="지출" else 1)
            e_item = st.text_input("수정 항목명", value=target['item'])
            e_amount = st.number_input("수정 금액", value=int(target['amount']))
            
            # 카테고리 수정 기능 추가
            current_cat_name = target['category'].split(" ")[1] if " " in target['category'] else target['category']
            e_cat_name = st.selectbox("수정 카테고리", cat_list, index=cat_list.index(current_cat_name) if current_cat_name in cat_list else 0)
            e_cat = ICON_MAP.get(e_cat_name)
            
            b1, b2 = st.columns(2)
            if b1.button("📝 수정 완료", use_container_width=True):
                db.update_record(edit_id, e_date.strftime("%Y-%m-%d"), e_type, e_item, e_amount, e_cat)
                st.rerun()
            if b2.button("🗑️ 삭제하기", use_container_width=True):
                db.delete_record(edit_id)
                st.rerun()

    st.subheader("📝 상세 내역")
    st.dataframe(df, use_container_width=True)
else:
    st.info("데이터가 없습니다.")