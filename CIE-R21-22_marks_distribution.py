import streamlit as st
import pandas as pd
import random
import io

# Function to generate random distribution of marks
def generate_marks_distribution():
    # Part A: 12 questions with marks 0 or 1, total 12 marks
    part_a = [random.choice([0, 1]) for _ in range(12)]
    while sum(part_a) != 12:
        part_a = [random.choice([0, 1]) for _ in range(12)]
    
    # Part B: 3 random questions selected out of 5, total 18 marks
    part_b = [random.randint(0, 6) for _ in range(3)]
    while sum(part_b) != 18:
        part_b = [random.randint(0, 6) for _ in range(3)]

    return part_a, part_b

# Streamlit App Interface
st.title("Marks Distribution Generator for Pharmacy Questions")

st.write("""
Upload an Excel file where the first column contains question names, 
and the second column is reserved for marks (to be filled by the app).
The app will randomly generate a marks distribution for each part.
""")

# Upload Excel File
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Display uploaded file
    st.write("Uploaded Excel file preview:")
    st.write(df.head())
    
    # Generate marks distribution
    part_a, part_b = generate_marks_distribution()
    
    # Assign the Part A marks to the first 12 rows (if there are at least 12 questions)
    if len(df) >= 12:
        df['Part A Marks'] = part_a + [None] * (len(df) - 12)
    else:
        st.warning("Excel file does not contain at least 12 questions for Part A")
    
    # Assign Part B marks to 3 random questions from the remaining ones
    remaining_questions = df.iloc[12:].reset_index(drop=True)
    selected_part_b_indices = random.sample(range(len(remaining_questions)), 3)
    for idx, selected_idx in enumerate(selected_part_b_indices):
        df.loc[selected_idx + 12, 'Part B Marks'] = part_b[idx]
    
    # Generate the output Excel file with the distribution
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Marks Distribution")
    output.seek(0)

    # Provide download link for the generated Excel file with updated filename
    st.download_button(
        label="Download Excel with Marks Distribution",
        data=output,
        file_name="CIE-R21-22-marks distribution.xlsx",  # Updated filename
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# GitHub Integration
st.write("""
### Want to see the code?
Check out the [GitHub Repository](https://github.com/yourusername/Marks-Distribution-Streamlit) to view the source code for this app and contribute!
""")
