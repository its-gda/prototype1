import google.generativeai as genai
import streamlit as st
  # PUT YOUR KEY HERE
GENAI_API_KEY = st.secrets["GEMENI_API_KEY"]
genai.configure(api_key=GENAI_API_KEY)

def generate_description(product_name):
      try:
          model = genai.GenerativeModel('gemini-pro')
          prompt = f"Write a catchy, professional one-sentence e-commerce product description for: {product_name}. Be concise."
          response = model.generate_content(prompt)
          return response.text
      except Exception:
          return f"High-quality {product_name} designed for maximum performance and style. Get yours today!"