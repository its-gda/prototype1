import streamlit as st
import database as db

st.set_page_config(page_title="AI Store Builder", page_icon="🛍️")

if 'user_id' not in st.session_state:
      st.session_state['user_id'] = None
if 'username' not in st.session_state:
      st.session_state['username'] = None

st.title("🚀 AI Dynamic Store Builder")
st.markdown("### Build your personalized shop link in minutes.")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
      with st.form("login_form"):
          u_login = st.text_input("Username")
          p_login = st.text_input("Password", type="password")
          if st.form_submit_button("Login"):
              user_id = db.verify_user(u_login, p_login)
              if user_id:
                  st.session_state['user_id'] = user_id
                  st.session_state['username'] = u_login
                  st.success("Logged in! Use the sidebar to go to Dashboard.")
                  st.rerun()
              else:
                  st.error("Invalid credentials")

with tab2:
      with st.form("signup_form"):
          u_sign = st.text_input("Choose Username")
          p_sign = st.text_input("Choose Password", type="password")
          if st.form_submit_button("Create Account"):
              if db.add_user(u_sign, p_sign):
                  st.success("Account created! Now login.")
              else:
                  st.error("Username already taken.")

if st.session_state['user_id']:
      if st.sidebar.button("Logout"):
          st.session_state['user_id'] = None
          st.session_state['username'] = None
          st.rerun()