import streamlit as st
from PIL import Image
import openai
import pandas as pd
import io

openai.api_key = "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"  # Replace with your key

st.set_page_config(page_title="GPT-4 Ledger Extractor")
st.title("📷 Extract Ledger Table Using GPT-4 Vision")
st.write("Upload a handwritten ledger image and get a downloadable Excel file extracted via GPT-4 Vision.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

def call_openai_vision(image_bytes):
    base64_img = image_bytes.getvalue()
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts handwritten ledger data from images into clean tabular format."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all the ledger data from this image and format it as a clean table. Return the data in CSV format."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img.decode('latin1')}", "detail": "high"}}
                ]
            }
        ],
        max_tokens=1500
    )
    return response.choices[0].message.content

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Ledger", use_column_width=True)

    if st.button("Extract with GPT-4 Vision"):
        with st.spinner("Analyzing image with GPT-4 Vision..."):
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            result_csv = call_openai_vision(image_bytes)

        st.subheader("📄 Extracted Table (CSV Format)")
        st.code(result_csv, language="csv")

        try:
            df = pd.read_csv(io.StringIO(result_csv))
            st.subheader("📊 Structured Table")
            st.dataframe(df)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)

            st.download_button(
                label="📥 Download Excel",
                data=output,
                file_name="ledger_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error("Could not parse result into Excel. Here's the raw output:")
            st.text_area("Output", result_csv)

else:
    st.info("Upload a handwritten ledger image to get started.")
