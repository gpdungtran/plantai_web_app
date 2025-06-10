# main.py - điểm vào chính của ứng dụng
import streamlit as st
from modules.auth import login_user, create_user
from modules.db import init_db
from modules.home import show_home
from modules.feedback import save_feedback
from modules.history import show_user_history, show_area_statistics

st.set_page_config(page_title="Leaf Disease Detection App", layout="centered")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "menu" not in st.session_state:
    st.session_state.menu = "Trang chủ"

menu_options = ["Trang chủ", "Đăng nhập", "Đăng ký", "Lịch sử"]
selected = st.sidebar.selectbox("Chức năng", menu_options, index=menu_options.index(st.session_state.menu))
st.session_state.menu = selected
menu = st.session_state.menu

if menu == "Đăng ký":
    st.title("Đăng ký tài khoản")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    confirm = st.text_input("Xác nhận mật khẩu", type="password")
    if st.button("Đăng ký"):
        if not username or not password:
            st.warning("Vui lòng nhập đầy đủ thông tin")
        elif password != confirm:
            st.error("Mật khẩu không khớp")
        else:
            success, msg = create_user(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

elif menu == "Đăng nhập":
    st.title("Đăng nhập")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    if st.button("Đăng nhập"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Đăng nhập thành công! Xin chào {username}.")
            st.rerun()
        else:
            st.error("Sai tên đăng nhập hoặc mật khẩu")

elif menu == "Trang chủ":
    st.title("🌿 Kiểm tra bệnh cây trồng🌳")
    st.header("Chỉ với 1 bức ảnh, chúng tôi có thể nhận biết bệnh trên cây trồng của bạn! 🤩")
    if not st.session_state.logged_in:
        st.warning("Vui lòng đăng nhập để sử dụng ứng dụng")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👉 Đăng nhập ngay"):
                st.session_state.menu = "Đăng nhập"
                st.rerun()
        with col2:
            if st.button("📝 Tạo tài khoản mới"):
                st.session_state.menu = "Đăng ký"
                st.rerun()
    else:
        show_home(st.session_state.username)

elif menu == "Lịch sử":
    show_user_history(st.session_state.username)
    show_area_statistics()
