import streamlit as st
import database as db

st.set_page_config(page_title="Public Store Preview")

if st.session_state.get('user_id') is None:
    st.error("Please login first!")
    st.stop()

user_id = st.session_state['user_id']
store = db.get_store_details(user_id)

if not store:
    st.warning("Your store is not set up yet. Go to the Dashboard!")
    st.stop()

# Extract store info
# store = (user_id, store_name, logo_path, brand_color, layout)
name, logo, color, layout = store[1], store[2], store[3], store[4]

# Apply custom brand color using HTML/CSS injection
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {color};
    }}
    .store-title {{
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: black;
    }}
    </style>
    """, unsafe_allow_html=True)

# Center alignment
st.markdown(f'<div class="store-title">{name}</div>', unsafe_allow_html=True)

if logo:
    st.image(logo, width=150)

products = db.get_products(user_id)

if layout == "Grid":
    cols = st.columns(2)
    for i, p in enumerate(products):
        with cols[i % 2]:
            # p = (id, user_id, name, desc, price, link, img)
            if p[6]: st.image(p[6])
            st.subheader(p[2])
            st.write(p[3])
            st.write(f"**Price: ${p[4]}**")
            st.link_button("Buy Now", p[5])
else:
    for p in products:
        st.subheader(p[2])
        st.write(p[3])
        st.write(f"**Price: ${p[4]}**")
        st.link_button("Buy Now", p[5])