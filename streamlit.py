import streamlit as st
import requests

# Placeholder for City, Area, and Road Data
# Create hierarchical dictionary for Streamlit dropdown
city_data = {
    "Bangalore": {
        "Indiranagar": ["100 Feet Road", "CMH Road"],
        "Whitefield": ["Marathahalli Bridge"],
        "Koramangala": ["Sony World Junction", "Sarjapur Road"],
        "M.G. Road": ["Trinity Circle", "Anil Kumble Circle"],
        "Jayanagar": ["Jayanagar 4th Block", "South End Circle"],
        "Hebbal": ["Hebbal Flyover", "Ballari Road"],
        "Yeshwanthpur": ["Yeshwanthpur Circle", "Tumkur Road"]
    },
    "Mumbai": {
        "Andheri": ["Sion Circle"],
        "Mira Road": ["Linking Road"],
        "Marine Lines": ["Mulund Check Naka", "Marine Drive"],
        "Kurla": ["CST Junction"],
        "Ghatkopar": ["SV Road"],
        "Dadar": ["Western Express Highway", "Eastern Express Highway"],
        "Goregaon": ["Dadar TT Circle"],
        "Chembur": ["JVLR", "Goregaon Flyover"],
        "Borivali": ["Peddar Road"],
        "Bandra": ["LBS Road", "Bandra-Worli Sea Link", "Andheri Metro Junction"]
    },
    "Delhi": {
        "Chanakyapuri": ["Dr. APJ Abdul Kalam Road"],
        "ITO": ["Bahadur Shah Zafar Marg"],
        "Connaught Place": ["Kasturba Gandhi Marg", "Indira Chowk", "Rajiv Chowk"],
        "Dhaula Kuan": ["Sardar Patel Marg"],
        "Mandi House": ["Tilak Marg"],
        "Lutyens' Delhi": ["Akbar Road"],
        "Lodhi Colony": ["Lodi Road"],
        "Vasant Kunj": ["Nelson Mandela Road"],
        "Ashram": ["Ring Road"],
        "Rohini": ["Outer Ring Road"],
        "Sundar Nagar": ["Mathura Road"],
        "Mahipalpur": ["NH-8 (Delhi-Jaipur Expressway)"],
        "Akshardham": ["NH-24 (Delhi-Meerut Expressway)"]
    },
    "Kolkata": {
        "Anandapur": ["EM Bypass"],
        "Baguiati": ["VIP Road"],
        "Park Circus": ["AJC Bose Road"],
        "Esplanade": ["Chowringhee Road", "Jawaharlal Nehru Road"],
        "Barabazar": ["Rabindra Sarani"],
        "Dum Dum": ["Jessore Road"],
        "Behala": ["Diamond Harbour Road", "James Long Sarani"],
        "Baranagar": ["BT Road"],
        "Howrah": ["Howrah Bridge Approach Road"],
        "Shyambazar": ["Bidhan Sarani"],
        "Theatre Road": ["Shakespeare Sarani"],
        "Park Street Area": ["Park Street"],
        "Bhowanipore": ["Sarat Bose Road"],
        "Gariahat": ["Gariahat Road"],
        "Central Avenue": ["Chittaranjan Avenue"],
        "Rashbehari": ["Rashbehari Avenue"],
        "Ballygunge": ["Syed Amir Ali Avenue"],
        "Beleghata": ["Beleghata Main Road"]
    },
    "Chennai": {
        "Nandanam": ["Anna Salai"],
        "Koyambedu": ["Poonamallee High Road", "Jawaharlal Nehru Road"],
        "Meenambakkam": ["GST Road"],
        "Thiruvanmiyur": ["OMR", "ECR"],
        "Vadapalani": ["Arcot Road"],
        "Gopalapuram": ["Cathedral Road"],
        "Kodambakkam": ["Kodambakkam High Road"],
        "T. Nagar": ["Usman Road", "G.N. Chetty Road"],
        "Velachery": ["Velachery Main Road"],
        "Kolathur": ["Kolathur Red Hills Road"],
        "West Tambaram": ["Tambaram Mudichur Road"],
        "Madhavaram": ["Madhavaram High Road"],
        "Nungambakkam": ["Nungambakkam High Road"],
        "Park Town": ["Periyar EVR High Road"],
        "Adyar": ["Sardar Patel Road"],
        "Vandalur": ["Vandalur-Kelambakkam Road"],
        "Medavakkam": ["Medavakkam Main Road"]
    },
    "Hyderabad": {
        "Outer Hyderabad": ["Nehru Outer Ring Road (ORR)"],
        "Central Hyderabad": ["Inner Ring Road (IRR)"],
        "Rajendranagar": ["PVNR Expressway"],
        "Secunderabad": ["Mahatma Gandhi Road (MG Road)"],
        "Hussain Sagar": ["Necklace Road"],
        "Shamshabad": ["NH-44"],
        "Panjagutta": ["NH-65"],
        "Uppal": ["NH-163"],
        "Mehdipatnam": ["NH-765"],
        "Somajiguda": ["Raj Bhavan Road"]
    },
    "Pune": {
        "Wakad": ["Pune-Mumbai Expressway"],
        "Shivajinagar": ["Jangli Maharaj Road (JM Road)"],
        "Deccan": ["Fergusson College Road (FC Road)"],
        "Kothrud": ["Karve Road"],
        "Bavdhan": ["Paud Road"],
        "Viman Nagar": ["Nagar Road"],
        "Narhe": ["Sinhagad Road"],
        "Swargate": ["Satara Road"],
        "Hadapsar": ["Pune-Solapur Road"],
        "Baner": ["Baner Road"],
        "Aundh": ["Aundh Road"],
        "Magarpatta": ["Magarpatta Road"],
        "Katraj": ["Katraj-Dehu Road Bypass"],
        "Ghorpadi": ["B.T. Kawade Road"],
        "Kondhwa": ["NIBM Road"],
        "Pashan": ["Sus Road"],
        "Lohegaon": ["Airport Road"],
        "Alandi": ["Alandi Road"],
        "Pimpri-Chinchwad": ["Pimpri-Chinchwad Spine Road"],
        "Bibwewadi": ["Bibwewadi Road"]
    },
    "Ahmedabad": {
        "Sarkhej": ["SG Highway (Sarkhej-Gandhinagar Highway)"],
        "Navrangpura": ["Ashram Road"],
        "Ellis Bridge": ["C.G. Road"],
        "Memnagar": ["Drive-In Road"],
        "Satellite": ["132 Feet Ring Road"],
        "Iscon": ["Iscon Road"],
        "Bopal": ["Bopal Road"],
        "Ognaj": ["S.P. Ring Road"],
        "Naroda": ["Naroda Road"],
        "Maninagar": ["Maninagar Main Road"],
        "Kalupur": ["Relief Road"],
        "Shahibaug": ["Shahibaug Road"],
        "Sabarmati": ["Sabarmati-Gandhinagar Highway"],
        "Hansol": ["Airport Road"],
        "Kankaria": ["Kankaria Road"],
        "Chandkheda": ["New C.G. Road"],
        "Paldi": ["Paldi Road"],
        "Vasna": ["Vasna Road"],
        "Prahlad Nagar": ["Prahlad Nagar Road"],
        "Ambawadi": ["Ambawadi Road"]
    },
    "Lucknow": {
        "Gomti Nagar": ["Shaheed Path", "Lohia Path"],
        "Indira Nagar": ["Faizabad Road"],
        "Alambagh": ["Kanpur Road (NH-27)"],
        "Rajajipuram": ["Hardoi Road"],
        "Arjunganj": ["Sultanpur Road"],
        "Mahanagar": ["Sitapur Road"],
        "Gomti Nagar Extension": ["Amar Shaheed Path"],
        "Jankipuram": ["Ring Road"],
        "Hazratganj": ["Vidhan Sabha Marg", "Ashok Marg"],
        "Charbagh": ["Charbagh Road"],
        "Telibagh": ["Rae Bareli Road"],
        "Jankipuram Extension": ["Kursi Road"],
        "Aliganj": ["Aliganj Main Road"],
        "Amausi": ["Lucknow-Kanpur Expressway"],
        "Chowk": ["Chowk Road"],
        "Aishbagh": ["Aishbagh Road"],
        "Husainabad": ["Husainabad Road"],
        "Vikas Nagar": ["Vikas Nagar Main Road"]
    },
    "Jaipur": {
        "Civil Lines": ["Ajmer Road"],
        "Malviya Nagar": ["Tonk Road"],
        "Vishwakarma Industrial Area": ["Sikar Road"],
        "Jawahar Nagar": ["JLN Marg"],
        "Pink City": ["MI Road"],
        "Amer": ["Amer Road"],
        "Gopalpura": ["Gopalpura Bypass"],
        "Mansarovar": ["B2 Bypass"],
        "Vaishali Nagar": ["Queens Road"],
        "Jhotwara": ["Kalwar Road"],
        "Kanakpura": ["Sirsi Road"],
        "Kukas": ["Delhi Road"],
        "Transport Nagar": ["Agra Road"],
        "Rambagh": ["Bhawani Singh Road"],
        "Johari Bazaar": ["Johari Bazaar Road"],
        "Chandpole": ["Chandpole Bazaar Road"],
        "Sindhi Camp": ["Station Road"],
        "Sodala": ["New Sanganer Road"],
        "Lalarpura": ["Gandhi Path"],
        "C-Scheme": ["Prithviraj Road"]
    },
    "Chandigarh": {
        "Sector 17": ["Madhya Marg"],
        "Sector 22": ["Dakshin Marg"],
        "Sector 1": ["Uttar Marg"],
        "Sector 16": ["Jan Marg"],
        "Sector 34": ["Himalaya Marg"],
        "Industrial Area Phase 1": ["Purv Marg"],
        "Sector 5": ["Shanti Path"],
        "Sector 40": ["Vikas Marg"],
        "Sector 42": ["Sarovar Path"],
        "Sector 26": ["Udyog Path"],
        "Sector 47": ["Himalaya Path"],
        "Near Sukhna Lake": ["Sukhna Path"],
        "Zirakpur": ["Airport Road"],
        "IT Park": ["IT Park Road"],
        "Rock Garden": ["Circular Road"],
        "PGI Hospital Area": ["PGI Road"],
        "Kishangarh": ["Kishangarh Road"],
        "Manimajra": ["Manimajra Road"],
        "Panchkula": ["Panchkula Road"],
        "Kaimbwala": ["Kaimbwala Road"]
    },
    "Bhopal": {
        "Koh-e-Fiza": ["VIP Road"],
        "Misrod": ["Hoshangabad Road"],
        "Kolar": ["Kolar Road"],
        "TT Nagar": ["New Market Road"],
        "MP Nagar Zone 1": ["MP Nagar Main Road"],
        "Ayodhya Nagar": ["Ayodhya Bypass Road"],
        "Arera Hills": ["Jail Road"],
        "Bairagarh": ["Indore Road (NH-46)"],
        "Karond": ["Berasiya Road", "Karond Bypass"],
        "Anand Nagar": ["Raisen Road"],
        "Lalghati": ["Lalghati Road"],
        "Gandhi Nagar": ["Airport Road"],
        "Shahpura": ["Shahpura Road"],
        "Budhwara": ["Hamidia Road"],
        "Katara Hills": ["Katara Hills Road"],
        "Old Bhopal": ["Chowk Bazaar Road"],
        "Van Vihar": ["Bhadbhada Road"],
        "Arera Colony": ["Link Road No.1"],
        "Habibganj": ["ISBT Road"]
    },
    "Indore": {
        "Vijay Nagar": ["AB Road"],
        "Rajwada": ["MG Road"],
        "Bengali Square": ["Ring Road"],
        "Regal Square": ["RNT Marg"],
        "Bhawar Kuan": ["Khandwa Road"],
        "Kalani Nagar": ["Airport Road"],
        "Malwa Mill": ["Bhawarkuan Road"],
        "Dewas Naka": ["MR-10 Road"],
        "Infosys Campus": ["Super Corridor"],
        "Mahalaxmi Nagar": ["Kanadia Road"],
        "Annapurna Nagar": ["Annapurna Road"],
        "Sapna Sangeeta": ["Sapna Sangeeta Road"],
        "Rau": ["Rau-Pithampur Road"],
        "Khajrana": ["Khajrana Main Road"],
        "Dewas Bypass": ["Dewas Naka Road"],
        "Malganj": ["Jawahar Marg"],
        "Chhavni": ["Chhavni Main Road"],
        "Sarwate Bus Stand": ["Malwa Mill Road"],
        "Tilak Nagar": ["Tilak Nagar Main Road"],
        "Ujjain Naka": ["Indore-Ujjain Road"]
    },
    "Patna": {
        "Patna Junction": ["Bailey Road"],
        "Gandhi Maidan": ["Ashok Rajpath"],
        "Dak Bungalow": ["Fraser Road"],
        "Sri Krishna Puri": ["Boring Road"],
        "Rajendra Nagar": ["Kankarbagh Main Road", "Rajendra Nagar Bridge Road"],
        "Income Tax Golambar": ["Gandhi Maidan Marg"],
        "Mithapur": ["Station Road"],
        "Patliputra Colony": ["Patliputra Kurji Road"],
        "Kotwali": ["Harding Road"],
        "Zero Mile": ["New Bypass Road (NH-30)"],
        "Digha": ["Digha Ashiana Road"],
        "Phulwari Sharif": ["Phulwari Sharif Road"],
        "Danapur": ["Gola Road"],
        "Jagdeo Path": ["Raja Bazar Bailey Road Flyover"],
        "Bihta": ["Danapur Khagaul Road"],
        "Anisabad": ["Anisabad Golambar Road"],
        "Kadamkuan": ["Bari Path Road"],
        "Punpun": ["Patna-Gaya Road (NH-83)"],
        "Jakkanpur": ["Mithapur Road"],
        "Transport Nagar": ["Didarganj Bypass Road"],
        "Saguna More": ["Saguna More Road"],
        "Bikram": ["Bikram Bypass"],
        "Kurji More": ["Kurji More Road"],
        "Hanuman Nagar": ["Hanuman Nagar Road"],
        "Ramkrishna Nagar": ["Ramkrishna Nagar Road"],
        "Rajapur Pul": ["Rajapur Pul Road"],
        "NIT More": ["NIT More Road"],
        "Kidwaipuri": ["Kidwaipuri Road"],
        "Lohia Path": ["Lohia Path"],
        "Chiriyatand Bridge": ["Chiriyatand Bridge Road"],
        "Chandmari": ["Chandmari Road"],
        "Mithila Colony": ["Mithila Colony Road"],
        "Pataliputra Golambar": ["Pataliputra Golambar Road"],
        "Gardanibagh": ["Gardanibagh Road"],
        "Chitkohra": ["Chitkohra Road"],
        "Fatuha": ["Fatuha Road"],
        "Sampatchak": ["Sampatchak Road"],
        "Patna Sahib": ["Patna Sahib Road"],
        "Gai Ghat": ["Gai Ghat Road"]
    },
    "Surat": {
        "Majura Gate": ["Ring Road", "Majura Gate Road"],
        "Varachha": ["Varachha Road"],
        "Udhna": ["Udhna Magdalla Road"],
        "Athwalines": ["Ghod Dod Road", "Athwalines Road"],
        "Piplod": ["Dumas Road", "Piplod Road"],
        "Vesu": ["VIP Road"],
        "Pal": ["Canal Road", "Pal Road"],
        "Kapodra": ["Kapodra Road"],
        "Katargam": ["Katargam Road"],
        "Adajan": ["Adajan Road"],
        "Sachin": ["Sachin Magdalla Road"],
        "Althan": ["Althan Road"],
        "Rander": ["Rander Road"],
        "Pandesara": ["Pandesara Road"],
        "Jahangirpura": ["Jahangirpura Road"],
        "Amroli": ["Amroli Road"],
        "Bhatar": ["Bhatar Road"],
        "City Light": ["New City Light Road"],
        "Nana Varachha": ["Nana Varachha Main Road"],
        "Puna Kumbharia": ["Puna Kumbharia Road"],
        "Yogi Chowk": ["Yogi Chowk Road"],
        "Sarthana": ["Sarthana Jakatnaka Road"],
        "Utran": ["Utran Road"],
        "Mora Bhagal": ["Mora Bhagal Road"],
        "Mota Varachha": ["Mota Varachha Road"],
        "Bamroli": ["Bamroli Road"],
        "Kharwar Nagar": ["Kharwar Nagar Road"],
        "Godadara": ["Godadara Road"],
        "Parvat Patiya": ["Parvat Patiya Road"],
        "Palanpur": ["Palanpur Road"],
        "Limbayat": ["Limbayat Road"],
        "Umarwada": ["Umarwada Road"],
        "Anjana Farm": ["Anjana Farm Road"],
        "Khajod": ["Khajod Road"],
        "Hazira": ["Hazira Road"],
        "Ichhapore": ["Ichhapore GIDC Road"]
    }
}

# Weather conditions data
weather_conditions = [
    "Clear", 
    "Rainy", 
    "Cloudy", 
    "Hazy", 
    "Foggy", 
    "Storm", 
    "Thunderstorms", 
    "Stormy", 
    "Dusty", 
    "Overcast", 
    "Fog", 
    "Rain", 
    "Windy"
]

# Placeholder for AWS Endpoint URL
endpoint_url = "<your_endpoint_url>"  # Replace with actual endpoint later

# Placeholder for Generative AI insights
def generative_ai_insights(input_data):
    return "This is a placeholder for generative AI insights."

# App Title
st.title("Road Congestion Prediction")

# Sidebar for dropdown selection
st.sidebar.title("Select Location")
selected_city = st.sidebar.selectbox("Select City", list(city_data.keys()))

selected_area = None
selected_road = None

if selected_city and selected_city in city_data:
    selected_area = st.sidebar.selectbox("Select Area", list(city_data[selected_city].keys()))
    if selected_area and selected_area in city_data[selected_city]:
        selected_road = st.sidebar.selectbox("Select Road", city_data[selected_city][selected_area])

# Other User Input Parameters
date = st.sidebar.date_input("Date")
traffic_volume = st.sidebar.number_input("Traffic Volume", min_value=0)
average_speed = st.sidebar.number_input("Average Speed (km/h)", min_value=0)
travel_time_index = st.sidebar.number_input("Travel Time Index", min_value=0)
incident_reports = st.sidebar.number_input("Incident Reports", min_value=0)

# Weather conditions dropdown (replacing the text input)
selected_weather = st.sidebar.selectbox("Weather Conditions", weather_conditions)

# Predict Congestion Level
if st.sidebar.button("Predict Congestion Level"):
    input_data = {
        "date": str(date),
        "city": selected_city,
        "area": selected_area,
        "road": selected_road,
        "traffic_volume": traffic_volume,
        "average_speed": average_speed,
        "travel_time_index": travel_time_index,
        "incident_reports": incident_reports,
        "weather_conditions": selected_weather,
    }
    
    # Placeholder prediction (Replace with actual AWS response later)
    predicted_level = 80  # Example congestion level (scale: 0–100)

    # Display congestion level
    st.write(f"Predicted Congestion Level: {predicted_level} out of 100")

    # Color-coded text feedback
    if predicted_level <= 40:
        st.success("Congestion Level: Low")
    elif predicted_level <= 70:
        st.warning("Congestion Level: Moderate")
    else:
        st.error("Congestion Level: High")

    # Progress bar visualization
    st.progress(predicted_level / 100)
    
    # Generative AI insights (Placeholder for now)
    st.info(generative_ai_insights(input_data))

# Display instructions
st.write(
    "Use the sidebar to select **City → Area → Road Name** and provide input parameters "
    "to predict congestion levels. AWS endpoint and generative AI functionalities are placeholders for now."
)