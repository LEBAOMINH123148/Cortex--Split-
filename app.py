import streamlit as st
import requests

api_url = "API"

# Config
st.set_page_config(page_title="Cortex Search", page_icon="🧠", layout="centered")

# Title centered
st.markdown("<h1 style='text-align: center;'>Welcome to <span style='color: red;'>Cortex</span></h1>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload your file here (Video or audio):", type=["mp4", "mov", "avi", "mkv", "mp3", "wav", "m4a"])

if uploaded_file:
    st.success("File Uploaded")
    
    # Check if video or audio
    is_video = uploaded_file.name.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
    
    # Show player
    if is_video:
        st.video(uploaded_file)
    else:
        st.audio(uploaded_file)

    # Search Form
    with st.form(key="search_form"):
        if is_video:
            Vquery = st.text_input("What do you want to find?(visual): ")
            Aquery = st.text_input("What do you want to find?(audio): ")
        else:
            Vquery = "" 
            Aquery = st.text_input("What do you want to find?: ")
            
        submit_button = st.form_submit_button("Search")
        
        if submit_button:
            if Vquery or Aquery:
                # Check API URL
                if not api_url:
                    st.error("API error")
                else:
                    with st.spinner("Searching: "):
                        try:
                            unique_key = f"{uploaded_file.name}_{uploaded_file.size}"
                            filename = uploaded_file.name
                            
                            files = {"file": (filename, uploaded_file.getvalue(), uploaded_file.type)}
                            
                            data = {
                                "v_query": Vquery,
                                "a_query": Aquery,
                                "unique_key": unique_key,
                                "filename": filename
                            }
                            
                            # Call API to kaggle
                            response = requests.post(api_url, files=files, data=data)
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.success("Search completed!")
                                
                                # Đọc dữ liệu từ key "results" cho khớp với Backend
                                matches = result.get("results", [])
                                
                                if matches:
                                    st.subheader("RESULT:")
                                    for match in matches:
                                        start_time = match.get('start', 0)
                                        end_time = match.get('end', 0)
                                        text_content = match.get('text', '')
                                        score = match.get('score', 0)
                                        
                                        st.markdown(f"**⏱ {start_time:.2f}s - {end_time:.2f}s**")
                                        st.write(f"📝 {text_content} *(Score: {score:.2f})*")
                                        st.markdown("---")
                                else:
                                    st.info("No results found in this file.")
                            else:
                                st.error(f"Error from server (Status Code: {response.status_code})")
                                st.write(response.text)
                                
                        except Exception as e:
                            st.error("Can't connect to backend")
                            st.error(f"Detail: {str(e)}")
            else:
                st.warning("Please tell us what you want to find first")