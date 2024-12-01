import streamlit as st

# Sidebar
st.set_page_config(
    page_title="ASME Sec VIII Div 1 Calculator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("This homepage of ASME Sec VIII Div 1 Calculator contains some figures referenced in the calculations on the left sidebar.")

# Display the image in Streamlit
st.image("nozzle_hillside.png", caption='Fig 1 - Hillside Nozzle')
st.image("flange_integral.png", caption='Fig 2 - Integral Flange')
st.image("flange_blind.png", caption='Fig 3 - Blind Flange')
