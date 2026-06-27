import streamlit as st
import time
from src.app.authentication import register_user, verify_login

if st.session_state.get("logged_in", False):
    st.switch_page("views/00_Executive_Home.py")

# Custom CSS removed to allow global Streamlit config.toml theme to propagate.

st.markdown("<h1 style='text-align: center; color: #3B82F6; font-size: 3rem; margin-bottom: 0;'>ReadyNest Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: 0;'>Secure Enterprise Data Platform</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Using a container to center and style the auth box
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Secure Login", "📝 Create Account"])
    
    with tab1:
        st.markdown("### Welcome Back")
        login_email = st.text_input("Email Address", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if login_email and login_password:
                progress_text = "Authenticating with secure server..."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                user = verify_login(login_email, login_password)
                my_bar.empty()
                
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user['name']
                    st.session_state.user_email = user['email']
                    st.session_state.user_role = user['role']
                    st.success(f"Welcome back, {user['name']}! Unlocking dashboard...")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")
            else:
                st.warning("⚠️ Please fill in both email and password.")

    with tab2:
        st.markdown("### Register New Account")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email Address", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Sign Up", type="secondary", use_container_width=True):
            if not all([reg_name, reg_email, reg_password, reg_confirm]):
                st.warning("⚠️ Please fill in all fields.")
            elif reg_password != reg_confirm:
                st.error("❌ Passwords do not match.")
            elif len(reg_password) < 6:
                st.error("❌ Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating account..."):
                    success, message = register_user(reg_name, reg_email, reg_password)
                    if success:
                        st.success("✅ Account created successfully! You can now log in via the Login tab.")
                    else:
                        st.error(f"❌ {message}")
                        
    st.markdown("</div>", unsafe_allow_html=True)
