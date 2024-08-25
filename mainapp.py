import streamlit as  st 
import  streamlit_option_menu as  sm
from model import Load_Model
from streamlit.components.v1  import html
from PIL import Image
from streamlit_push_notifications import send_alert
st.set_page_config(page_title="CropCare: Rice Disease Insight", layout="wide")
header_htm = f"""
        <div style="background-color:#4CAF50;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;font-family:'Montserrat', sans-serif;font-size:48px;">
            CropCare: Rice Disease Insight
        </h1>
        </div>
        """
st.markdown(header_htm, unsafe_allow_html=True)
st.divider()
col1,col2 = st.columns([60, 40], gap="small")

if  "uploaded"  not  in st.session_state:
    st.session_state["uploaded"] = False
if  "label_disease" not in st.session_state:
    st.session_state["label_disease"]  = None
#swith st.sidebar:
    #sm.option_menu("main menu", ["home", "predict", "about"])
@st.experimental_fragment
def  predict_image(img_file_name):
    obj = Load_Model(model_path="/home/wambugu/Downloads/mobilenet_model_rice_disease_classification.keras", img_path=img_file_name)
    return obj.predict_image_class()
with col2:
    upload_img_container = st.empty()
    with upload_img_container.container(border=False):
        st.write("upload  image please!")
        img_file  = st.file_uploader("Upload image to continue", type=["jpg","png","jepg"],accept_multiple_files=False)
        if img_file != None:
            with open(f"{img_file.name}", "wb") as f:
                f.write(img_file.read())
                
            st.session_state["uploaded"] = True
    if  st.session_state["uploaded"] == True:
        upload_img_container.empty()
        st.toast("Image  file  uploaded  succesfully")
        with st.container(height=500, border=False):
            st.image(image=Image.open(img_file).resize((150,150)), use_column_width=True, output_format="JPEG",channels="RGB")
        with st.spinner(text="checking..."):
            label = predict_image(img_file_name=img_file)
            st.session_state["label_disease"]  = label[0]
        header_html = f"""
        <div style="background-color:#4CAF50;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;font-family:'Montserrat', sans-serif;font-size:48px;">
            {label[0]}
        </h1>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        send_alert(message=f"{label[0]}")

with col1:
    if  st.session_state["label_disease"] != None:
        if  st.session_state["label_disease"] =="bacterial leaf blight":
            with st.container(height=500, border=False):
                st.html(open("bacterial.html").read())
        elif  st.session_state["label_disease"] == "leaf blast":
            with st.container(height=500, border=False):
                st.html(open("blast.html").read())
        elif  st.session_state["label_disease"] == "brown spot":
            with st.container(height=500, border=False):
                st.html(open("spot.html").read())
    else:
        st.error("Upload  a  photo to detect.")
            
            
    #st.write("Rice  disease  notify  is  a  web  application  that")