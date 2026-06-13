# User Flows

## Persona 1: The Rural Farmer (Hindi/Code-Mixed)
- **User**: "मुझे किसान योजना चाहिए, मेरा aadhaar card है" (I want farmer scheme, I have aadhaar card)
- **Bot**: Detects Hindi/Code-mix. Identifies keyword "किसान". Consults RAG for PM-KISAN.
- **Bot**: "नमस्ते! पीएम किसान योजना (PM-KISAN) के तहत किसानों को हर साल ₹6000 मिलते हैं। क्या आपकी उम्र 18 वर्ष से अधिक है और आपके नाम पर खेती की ज़मीन है?"
- **User**: "हाँ"
- **Bot**: "बहुत बढ़िया! आवेदन के लिए ये दस्तावेज़ चाहिए:
  - आधार कार्ड
  - बैंक खाता (Aadhaar linked)
  - ज़मीन के कागज़ात
  क्या आप जानना चाहते हैं कि आवेदन कहाँ करें?"

## Persona 2: The Gig Worker / Unorganized Sector Worker (Tamil)
- **User**: "நான் ஒரு தச்சுத் தொழிலாளி, எனக்கு எந்தத் திட்டம் உதவும்?" (I am a carpenter, what scheme will help me?)
- **Bot**: Detects Tamil. Searches RAG for unorganized sector schemes (e-Shram).
- **Bot**: "வணக்கம்! இ-ஷ்ரம் (e-Shram) திட்டம் அமைப்புசாரா தொழிலாளர்களுக்கு மிகவும் பயனுள்ளதாக இருக்கும். இதன் மூலம் ₹2 லட்சம் விபத்து காப்பீடு கிடைக்கும். உங்கள் வயது 16 முதல் 59க்குள் உள்ளதா?"
- **User**: "ஆம், 35 வயது."
- **Bot**: "நல்லது! பதிவு செய்ய தேவையான ஆவணங்கள்:
  - ஆதார் அட்டை
  - ஆதாருடன் இணைக்கப்பட்ட மொபைல் எண்
  - வங்கி கணக்கு விவரம்."

## Persona 3: Woman Head-of-Household
- **User**: "I need help with cooking gas."
- **Bot**: Detects English intent. Since strictly configured to prefer Hindi/Tamil, it may reply in the default language of the region (e.g., Hindi) or confirm preference.
- **Bot**: "नमस्ते! गैस सिलेंडर के लिए उज्ज्वला योजना (Ujjwala Yojana) है। क्या आप एक वयस्क महिला हैं?"
- **User**: "Yes, I am a 40 year old woman."
- **Bot**: "उज्ज्वला योजना के तहत आपको मुफ़्त गैस कनेक्शन मिलेगा। आवश्यक दस्तावेज़:
  - बीपीएल राशन कार्ड
  - आधार कार्ड
  - पासपोर्ट साइज़ फोटो."
