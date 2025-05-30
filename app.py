import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import io

st.set_page_config(page_title="Ledger OCR to Excel", layout="centered")

st.title("🧾 Handwritten Ledger to Excel Converter")

st.write("Upload an image of a handwritten ledger (in Hindi/English), and get an Excel table as output.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Extract Text and Convert to Excel"):
        with st.spinner("Running OCR..."):
            # Run OCR (Hindi + English)
            raw_text = pytesseract.image_to_string(image, lang='hin+eng')

        st.subheader("📄 Extracted Text")
        st.text_area("OCR Output", raw_text, height=300)

        # Parse into rows
        lines = raw_text.split("\n")
        rows = []
        for line in lines:
            # Split by common delimiters
            parts = [part.strip() for part in line.split() if part.strip()]
            if parts:
                rows.append(parts)

        if rows:
            df = pd.DataFrame(rows)

            st.subheader("🧾 Structured Table")
            st.dataframe(df)

            # Convert to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)

            st.download_button(
                label="📥 Download as Excel",
                data=output,
                file_name="ledger_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Could not structure the data into a table. Try a clearer image or adjust formatting.")

else:
    st.info("Please upload an image to begin.")
