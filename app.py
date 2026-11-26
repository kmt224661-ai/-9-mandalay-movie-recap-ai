import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="9/Mandalay Movie Recap AI",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 9/Mandalay Movie Recap AI")
st.write("မြန်မာ Movie Recap ဖန်တီးရေး AI")

movie = st.file_uploader(
    "🎥 Movie ဖိုင်တင်ပါ",
    type=["mp4", "mov", "mkv", "webm"]
)

source = st.text_area(
    "📝 Movie အကြောင်းအရာထည့်ပါ",
    height=180
)

style = st.selectbox(
    "Recap ပုံစံ",
    ["စိတ်ဝင်စားဖွယ်", "ဟာသဆန်ဆန်", "ကြောက်စရာ", "ရုပ်ရှင်ဝေဖန်ပုံစံ"]
)

length = st.selectbox(
    "Video ကြာချိန်",
    ["1 မိနစ်", "2 မိနစ်", "3 မိနစ်", "5 မိနစ်"]
)

if st.button("✨ AI Recap ထုတ်မယ်"):
    if not source.strip():
        st.warning("Movie အကြောင်းအရာ အရင်ထည့်ပါ။")
    else:
        try:
            client = OpenAI()
            with st.spinner("AI ရေးပေးနေပါတယ်..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "သင်သည် မြန်မာ Movie Recap ကျွမ်းကျင်သူဖြစ်သည်။"
                        },
                        {
                            "role": "user",
                            "content": f"""
{length} ကြာမြင့်မည့် မြန်မာ Movie Recap ရေးပါ။
ပုံစံ - {style}
အစမှာ Hook ထည့်ပါ။
ဇာတ်လမ်းကို နားလည်လွယ်အောင် ရေးပါ။
မသိသောအချက် မတီထွင်ပါနှင့်။
အကြောင်းအရာ:
{source}
"""
                        }
                    ]
                )

            st.session_state["recap"] = response.choices[0].message.content

        except Exception as e:
            st.error(f"Error: {e}")

if "recap" in st.session_state:
    st.subheader("✍️ Recap စာသား ပြင်ဆင်ရန်")

    st.session_state["recap"] = st.text_area(
        "ကိုယ်ကြိုက်သလို ပြင်ရေးနိုင်ပါတယ်",
        value=st.session_state["recap"],
        height=350
    )

    st.download_button(
        "📥 Recap စာသား Download",
        data=st.session_state["recap"],
        file_name="movie_recap.txt",
        mime="text/plain"
    )

if movie:
    st.success(f"Movie ဖိုင်ရွေးပြီးပါပြီ: {movie.name}")

st.caption("9/Mandalay Movie Recap AI")
