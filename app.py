import streamlit as st
from tracker import process_video
import tempfile
import os
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                    url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="AI Sports Coach", layout="wide")
set_bg("bg3.jpeg")

st.title("AI Sports Mechanics Coach 🏀⚽")
st.markdown("Upload your video to compare your kinematic form with a professional athlete.")
sport_choice = st.selectbox("Select Sport", ["Basketball", "Football"])
dominant_side = st.selectbox("Dominant Side (Shooting Hand / Kicking Leg)", ["Right-Side", "Left-Side"])
col1, col2 = st.columns(2)

with col1:
    st.header("Pro Form (Reference)")
    if sport_choice == "Basketball":
        pro_video_url = "Basketball.mp4" 
        st.video(pro_video_url)
        st.success("Target: Maintain a 90-degree shooting elbow prior to release.")
    else:
        pro_video_url = "Football.mp4" 
        st.video(pro_video_url)
        st.success("Target: Deep knee bend (< 100 deg) on the backswing for maximum striking power.")

with col2:
    st.header("Your Analysis")
    feedback = []
    accuracy = 0
    uploaded_file = st.file_uploader(f"Upload your .mp4 {sport_choice} video", type=["mp4"])

    if uploaded_file is not None:
        
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        tfile.close()
        input_video_path = tfile.name
        output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.webm').name
        st_frame = st.empty()
        
       
        with st.spinner(f"Running {sport_choice} Biomechanical Analysis..."):
            
            feedback, accuracy = process_video(
                input_video_path,
                output_video_path,
                sport=sport_choice,
                dominant_side=dominant_side,
                st_frame=st_frame
)
            
        st.success("Analysis Complete! Review the footage below.")
        st.video(output_video_path)
        st.subheader("📊 Final Performance Analysis")
        st.metric("Accuracy", f"{int(accuracy)}%")
        st.progress(int(accuracy))
        st.subheader("📌 Areas to Improve")

        if feedback and "areas" in feedback:
            for point in feedback["areas"]:
                st.markdown(f"- **{point}**")

        st.subheader("⚙️ Technical Feedback")

        if feedback and "technical" in feedback:
            for tip in feedback["technical"]:
                st.markdown(f"- {tip}")

      
      
    try:
            os.remove(input_video_path)
    except Exception:
            pass