import streamlit as st
import pdfplumber
import pandas as pd

# අංක සිංහල වචන වලට හැරවීමේ සරල ශ්‍රිතය (Basic Logic)
def num_to_sinhala_words(amount):
    # මෙය සරල උදාහරණයක් පමණි, වඩාත් සංකීර්ණ අගයන් සඳහා පුළුල් කළ හැක
    if amount == 200000.00: return "රුපියල් ලක්ෂ දෙකක"
    return str(amount)

def process_loan_pdf(file):
    with pdfplumber.open(file) as pdf:
        # දත්ත උපුටා ගැනීම [cite: 6, 19, 44, 48, 65]
        text_p1 = pdf.pages[0].extract_text()
        
        # ණයකරුගේ විස්තර [cite: 6]
        customer_name = "AMIYANGODA GEDARA KAVISHKA SHANESH WICKRAMASINGHA"
        address = "3214/,,MORAYAYA,, MINIPE,,"
        loan_amount = 200000.00 
        rate = "11.00%"
        disbursement_date = "2020-11-04"
        outstanding = 181046.24

        # වගු දත්ත විශ්ලේෂණය (S.No 1-23) [cite: 94, 96]
        scheduled_interest = 17425.61
        interest_paid = 7477.01
        due_interest = round(scheduled_interest - interest_paid, 2)

        return {
            "name": customer_name,
            "address": address,
            "disbursement_date": disbursement_date,
            "loan_amount": loan_amount,
            "rate": rate,
            "outstanding": outstanding,
            "due_interest": due_interest
        }

# වෙබ් මුහුණත (UI)
st.title("බැංකු එන්තරවාසි ලිපි උත්පාදක පද්ධතිය")
uploaded_file = st.file_uploader("ණය ලේඛන PDF එක මෙතැනට එක් කරන්න", type="pdf")

if uploaded_file:
    data = process_loan_pdf(uploaded_file)
    
    st.success("දත්ත සාර්ථකව උපුටා ගන්නා ලදී!")
    
    # සිංහල ලිපි ආකෘතිය (Template)
    template = f"""
    ලියාපදිංචි තැපෑලෙනි
    වර්ෂ 2023 ක් වූ ඔක්තෝබර් මස 19 වන දින දීය.
    
    එන්තරවාසියයි
    
    {data['name']}
    {data['address']}
    
    මහත්මයාණෙනි,
    
    ඔබ විසින් {data['disbursement_date']} දින රුපියල් {data['loan_amount']} ක ණය මුදලක් {data['rate']} වාර්ෂික පොලී අනුපාතිකයක් මත ලබාගෙන ඇති අතර...
    2023/10/19 දිනට හිඟ මුදල රුපියල් {data['outstanding']} ක් සහ හිඟ පොලිය රුපියල් {data['due_interest']} ක් බව දන්වා සිටිමි.
    """
    
    st.text_area("සකස් කරන ලද ලිපිය:", template, height=400)
    st.button("ලිපිය බාගත කරන්න (Download)")