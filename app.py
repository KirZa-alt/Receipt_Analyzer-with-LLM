import streamlit as st
from PIL import Image
import io
import base64
import json
import re
import pandas as pd
import matplotlib.pyplot as plt

import google.genai as genai

# ------------------ GEMINI AI SETUP ------------------
# Replace with your actual Gemini API key
client = genai.Client(api_key="AIzaSyCsp4OaaRCzBGv5-AvhMfaONkB9pPa-KvU")

# ------------------ STREAMLIT APP ------------------
st.title("AI Receipt Analyzer")
st.markdown("""
Upload your receipt image (JPG/PNG) and get:
- OCR text extraction (even for blurry images)
- Structured table of items & prices
- Automatic category assignment
- Totals by category and overall spending
- Spending chart visualization
- AI-powered financial insights
""")

# ------------------ FILE UPLOADER ------------------
uploaded_file = st.file_uploader("Upload receipt image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)

    # ------------------ IMAGE TO BASE64 ------------------
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # ------------------ PROMPT FOR OCR ------------------
    ocr_prompt = (
        "Here is a receipt image. Extract all items and prices. "
        "Return only valid JSON list like:\n"
        "[{\"item\":\"\",\"price\":0.0,\"category\":\"\"}]"
    )

    try:
        # ------------------ GEMINI AI OCR ------------------
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[ocr_prompt, img_b64]
        )

        raw = response.text
        st.subheader("AI OCR Output")
        st.text(raw)

        # ------------------ EXTRACT JSON ------------------
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if not match:
            st.error("AI did not return structured JSON.")
        else:
            data_json = match.group(0)
            data = json.loads(data_json)
            df = pd.DataFrame(data)

            # ------------------ DISPLAY STRUCTURED TABLE ------------------
            st.subheader("Structured Data")
            st.dataframe(df)

            # ------------------ CALCULATE TOTALS ------------------
            totals = df.groupby("category")["price"].sum()
            st.subheader("Totals by Category")
            st.dataframe(totals.reset_index().rename(columns={"price":"Total"}))
            st.write(f"**Overall Spending:** ${df['price'].sum():.2f}")

            # ------------------ SPENDING CHART ------------------
            st.subheader("Spending Chart")
            fig, ax = plt.subplots()
            totals.plot(kind="bar", color="skyblue", ax=ax)
            ax.set_ylabel("Amount ($)")
            ax.set_xlabel("Category")
            ax.set_title("Spending by Category")
            st.pyplot(fig)

            # ------------------ AI FINANCIAL INSIGHTS ------------------
            st.subheader("AI Financial Insights")
            insight_prompt = (
                "I have this receipt data in JSON format: "
                f"{data_json}\n"
                "Provide 3-4 actionable financial insights in plain English. "
                "Include categories where spending is high, suggestions for saving, "
                "and simple budgeting tips."
            )

            insight_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[insight_prompt]
            )

            insights = insight_response.text
            st.markdown(insights)

            # ------------------ PROFESSIONAL SUMMARY ------------------
            st.markdown("---")
            st.subheader("Summary")
            st.markdown(f"""
- **Total Spending:** ${df['price'].sum():.2f}  
- **Top Spending Category:** {totals.idxmax()} (${totals.max():.2f})  
- **Number of Items:** {len(df)}  

AI has analyzed your receipt and provided actionable advice to help optimize your spending. Use the chart and insights above to plan your budget better.
""")

    except Exception as e:
        st.error("AI processing failed: " + str(e))
