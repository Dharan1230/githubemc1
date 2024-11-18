import streamlit as st
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
from PIL import Image

st.set_page_config(layout= "wide")

def load_lottieurl(url):
   r = requests.get(url)
   if r.status_code != 200:
      return None
   return r.json()   

def local_css(file_name):
   with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)
local_css("C:/Users/Dharan M/OneDrive/Desktop/Project Portfolio/Style/style.css")      

lottie_coder = load_lottieurl("https://lottie.host/091db978-e971-4933-b951-a558a5724627/sHHBt5vjy8.json")
lottie_contact = load_lottieurl("https://lottie.host/908f97ff-8ff7-484d-82bd-5e04322bfc6c/onmPuWVEiM.json")
image = Image.open("C:/Users/Dharan M/OneDrive/Desktop/Project Portfolio/360.jpg")


st.write("##")
st.subheader("Hey Guys :wave:")
st.write("Welcome")
st.title("My Portfolio Website")
st.write("""
I am gonna explain briefly about how Streamlit can be used to build
interactive and responsive websites to deploy any machine learning model """)
st.write("[Read More] (https://streamlit.io/)")
st.write("---")

with st.container():
 selected = option_menu(
      menu_title = None,
      options = ['About', 'Projects', 'Contact'],
      icons = ['person', 'code-slash', 'chat-left-text-fill'],
      orientation = 'horizontal'
)
 
if selected == "About":
 
   with st.container():
      col1, col2 = st.columns(2)
      with col1:
         st.write("##")
         st.subheader("I am Manoj")
         st.title("Undergrad at BIMS")
      with col2:
         st_lottie(lottie_coder)   
   
   st.write("---")        

   with st.container():
      col3,col4 = st.columns(2)
      with col3:
         st.subheader("""
         Education
         - BIT
            - Bachelor of Engineering - Computer Science
            - Grade: xyz
         - Vidya Mandir Ind. PU college
            - PCMB
            - Grade: abc
         - Sri Vidya Mandir
            - Xth
            - Grade: def
         """)   
      with col4:
         st.subheader("""
         Experience
         - Ellucian -Internship
         - Duration
         - Bangalore
         """)

if selected =="Projects":
   with st.container():
      st.header("My Projects")
      st.write("##")
      col5, col6 = st.columns((1,2))
      with col5:
         st.image(image)      
      with col6:
         st.subheader("PERFUME")
         st.write("""Created a small web page using HTML and CSS.To visit click the below link""")
         st.markdown("[Visit Here](https://dharan1230.neocities.org/Perfume/)") 

if selected == "Contact":
   st.header("Get In Touch!")    
   st.write("##")
   st.write("##")

   contact_form="""
   <form action="https://formsubmit.co/dharanm1506@gmail.com" method="POST">
    <input type = "hidden" name ="_captcha" value = "false">
    <input type="text" name="name" placeholder = "Your name" required>
    <input type="email" name="email" placeholder = "Your email"  required>
    <textarea name = "message" placeholder = "Your message" required></textarea>
    <button type="submit">Send</button>
   </form>

   """
   left_col, right_col = st.columns((2,1))
   with left_col:
      st.markdown (contact_form, unsafe_allow_html= True)
   with right_col:   
      st_lottie(lottie_contact,height=200)
