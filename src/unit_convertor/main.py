# import streamlit as st
# from litellm import completion  # type: ignore
# # from decouple import config
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # SECRET_KEY = config('GEMINI_API_KEY')
# SECRET_KEY = os.getenv("GEMINI_API_KEY" , "") 

# # print(SECRET_KEY)

# os.environ["GEMINI_API_KEY"] = SECRET_KEY


# def ask_gemini(query):
#     response = completion(
#         model="gemini/gemini-1.5-flash",
#         messages=[{"role": "user", "content": query}]
#     )
#     return response["choices"][0]["message"]["content"]


# st.set_page_config(page_title="AI Unit Converter", layout="wide")
# st.title("🔄 AI-Powered Google Unit Converter")

# mode = st.radio("Choose Mode:", ["Simple Mode", "AI Mode"])

# if mode == "Simple Mode":
#     category = st.selectbox("Category", ["Length", "Weight", "Temperature", "Currency"])
#     from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles"])
#     to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles"])
#     value = st.number_input("Enter Value", min_value=0.0, step=0.01)

#     if st.button("Convert"):
#         result = value * 1000  
#         st.success(f"Converted Value: {result} {to_unit}")

# elif mode == "AI Mode":
#     st.subheader("🤖 Ask AI for Conversions!")
#     user_query = st.text_area("Describe your conversion (e.g., 'Convert 5 feet to cm')")

#     if st.button("Ask AI"):
#         st.info("🔄 AI is thinking...")
#         ai_response = ask_gemini(user_query)
#         st.success(ai_response)



import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import os
import re

load_dotenv()
SECRET_KEY = os.getenv("GEMINI_API_KEY", "")
os.environ["GEMINI_API_KEY"] = SECRET_KEY


def is_unit_conversion_query(query):
    pattern = r"(convert|how many|what is|equals|in)\s+(\d+(\.\d+)?)?\s*\w+\s+(to|in|into|equals|is)?\s*\w*"
    return bool(re.search(pattern, query.lower()))

# ai suggestion static list 
ai_suggestions = [
    "✅ Convert 5 meters to feet",
    "✅ How many meters in a km?",
    "✅ Convert 100 Fahrenheit to Celsius",
    "✅ What is 10 kg in grams?"
]

# main function that ask question to gemini llm
def ask_gemini(query):
    if not is_unit_conversion_query(query):
        return f"⚠️ Please ask a valid unit conversion question. Example: '{ai_suggestions[0]}'"

    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": query}],
        api_key=SECRET_KEY
    )
    return response["choices"][0]["message"]["content"]

# Conversion formulas
def convert_units(category, from_unit, to_unit, value):
    if category == "Length":
        conversion_factors = {
            ("Meters", "Kilometers"): value / 1000,
            ("Kilometers", "Meters"): value * 1000,
            ("Miles", "Kilometers"): value * 1.60934,
            ("Kilometers", "Miles"): value / 1.60934
        }
    
    elif category == "Weight":
        conversion_factors = {
            ("Grams", "Kilograms"): value / 1000,
            ("Kilograms", "Grams"): value * 1000,
            ("Milligrams", "Grams"): value / 1000,
            ("Grams", "Milligrams"): value * 1000
        }
    
    elif category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value  # If same unit, return the same value

    # Get the conversion factor, return the converted value
    return conversion_factors.get((from_unit, to_unit), "Invalid conversion")


st.set_page_config(page_title="AI Unit Converter", page_icon="🔁")
st.title("🔄 AI-Powered Google Unit Converter 📐")
st.write("🪄Switch between  **Simple Mode 🧮** (Standard conversions) & **AI Mode 👑** (Smart conversions🤖)")

mode = st.radio("Choose Mode:", ["Simple Mode 🤓", "AI Mode 😎"])

if mode == "Simple Mode 🤓":
    category = st.selectbox("Category", ["Length", "Weight", "Temperature"])

    # Dynamically update units based on selected category
    unit_options = {
        "Length": ["Meters", "Kilometers", "Miles"],
        "Weight": ["Grams", "Kilograms", "Milligrams"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }

    from_unit = st.selectbox("From", unit_options[category])
    to_unit = st.selectbox("To", unit_options[category])
    value = st.number_input("Enter Value", min_value=0.0, step=0.01)

    if st.button("Convert"):
        result = convert_units(category, from_unit, to_unit, value)
        if isinstance(result, str):
            st.error("Invalid conversion")
        else:
            st.success(f"Converted Value: {result:.2f} {to_unit}")

elif mode == "AI Mode 😎":
    st.subheader("🤖 Ask AI for Conversions!")
    user_query = st.text_area("Describe your conversion (e.g., 'Convert 5 feet to cm')")

    if st.button("Ask AI 👑"):
        st.info("🔄 AI is thinking...")
        ai_response = ask_gemini(user_query)
        st.success(ai_response)

    # Show AI suggestions
    st.write("💡 **Examples of valid queries:**")
    for suggestion in ai_suggestions:
        st.write(f"- {suggestion}")

def ballons():
    st.balloons()

st.text("©️made by maneeshanif ✒️")
st.button("Its time to celebrate 🎉" , on_click=ballons)
    
