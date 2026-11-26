9/Mandalay Movie Recap AI — Starter Website

ပါဝင်သည်
- ဖုန်း/ကွန်ပျူတာ Responsive Website UI
- MP4/MOV/MKV/WEBM Upload endpoint (2GB limit)
- AI Burmese Recap Script endpoint (OpenAI API Key ထည့်လျှင် အလုပ်လုပ်မည်)
- Movie URL ထည့်ရန် UI (URL မှ video download/analysis မပါသေး)
- Voice, subtitle, scene edit, music, final MP4 export အတွက် UI အစိတ်အပိုင်းများ

ကွန်ပျူတာတွင် စမ်းသပ်ရန်
1. Python 3.10+ install လုပ်ပါ။
2. ဒီ folder ထဲတွင် terminal ဖွင့်ပါ။
3. python -m venv .venv
4. Windows: .venv\\Scripts\\activate
   Mac/Linux: source .venv/bin/activate
5. pip install -r requirements.txt
6. (ရွေးချယ်နိုင်) .env.example ကို .env အဖြစ်ကူးပြီး OPENAI_API_KEY ထည့်ပါ။
   ထို့နောက် environment variable ကို OS မှ load လုပ်ပါ (သို့) app.py မတိုင်မီ export လုပ်ပါ။
7. uvicorn app:app --host 0.0.0.0 --port 8000
8. Browser တွင် http://127.0.0.1:8000 ကိုဖွင့်ပါ။

မှတ်ချက်
ဒီဟာက စတင်အသုံးပြုနိုင်တဲ့ MVP starter ဖြစ်ပါတယ်။ Production အတွက် HTTPS, login/password, private cloud storage,
background job queue, video scene analysis, speech-to-text, Burmese TTS, FFmpeg render pipeline,
backup နှင့် API usage limits တို့ကို ထပ်မံတည်ဆောက်ရပါမည်။ API key ကို Website frontend ထဲ မထည့်ပါနှင့်။
ကိုယ်ပိုင် သို့မဟုတ် အသုံးပြုခွင့်ရှိသော Video များကိုသာ တင်ပါ။
