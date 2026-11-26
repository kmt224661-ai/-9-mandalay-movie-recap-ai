import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from openai import OpenAI

BASE = Path(__file__).parent
UPLOADS = BASE / 'uploads'
UPLOADS.mkdir(exist_ok=True)
app = FastAPI(title='9/Mandalay Movie Recap AI')
templates = Jinja2Templates(directory=str(BASE / 'templates'))

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/api/upload')
async def upload_movie(file: UploadFile = File(...)):
    allowed = {'.mp4', '.mov', '.mkv', '.webm'}
    suffix = Path(file.filename or '').suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, 'MP4, MOV, MKV, သို့မဟုတ် WEBM ဖိုင်ကိုသာ တင်ပါ။')
    # 2 GB safety limit for this starter build
    dest = UPLOADS / (str(abs(hash(file.filename or 'movie'))) + suffix)
    size = 0
    with dest.open('wb') as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > 2 * 1024 * 1024 * 1024:
                dest.unlink(missing_ok=True)
                raise HTTPException(413, 'ဖိုင်အရွယ်အစား 2GB ထက်မကျော်ရပါ။')
            out.write(chunk)
    return {'ok': True, 'filename': file.filename, 'saved_as': dest.name, 'size_bytes': size,
            'note': 'ဖိုင် Upload အောင်မြင်ပါသည်။ ဇာတ်လမ်းခွဲခြမ်းစိတ်ဖြာမှုအတွက် Video Analysis pipeline/API ကို ချိတ်ဆက်ရန် လိုအပ်ပါသည်။'}

@app.post('/api/recap')
async def create_recap(payload: dict):
    source = (payload.get('source') or '').strip()
    style = payload.get('style', 'သဘာဝကျတဲ့ မြန်မာ Movie Recap')
    length = payload.get('length', '1-2 မိနစ်')
    if not source:
        raise HTTPException(400, 'ဇာတ်လမ်းအကျဉ်း သို့မဟုတ် Video မှရရှိထားသော စာသားကို ထည့်ပါ။')
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return JSONResponse({'ok': True, 'demo': True,
            'script': f'ဒီနေရာမှာ AI က {length} စာစာသားကို ထုတ်ပေးမည်။\n\nထည့်သွင်းထားသော အကြောင်းအရာကို အခြေခံပြီး Hook၊ ဇာတ်လမ်းအကျဉ်း၊ အရေးကြီး Dialogue နှင့် စိတ်ဝင်စားဖွယ် အဆုံးသတ်တို့ ပါဝင်သော {style} Script ကို ထုတ်ပေးရန် OPENAI_API_KEY ထည့်သွင်းပါ။\n\nအကြောင်းအရာ:\n{source}',
            'message': 'Demo mode ဖြစ်နေပါသည်။ တကယ့် AI Script ထုတ်ရန် API Key လိုအပ်ပါသည်။'})
    client = OpenAI(api_key=api_key)
    prompt = f'''သင်သည် မြန်မာဘာသာ Movie Recap ဇာတ်ညွှန်းရေးသူဖြစ်သည်။ အောက်ပါအကြောင်းအရာကို အခြေခံ၍ {length} ခန့်စာ {style} ဖြင့်ရေးပါ။\nလိုအပ်ချက်များ - အစမှာ တိုတိုထိမိသော Hook၊ ဇာတ်လမ်းကို အစဉ်လိုက်နားလည်လွယ်စွာ ပြောပြရန်၊ ရရှိထားသော Dialogue များကို သဘာဝကျကျ ထည့်ရန်၊ မသိသောအချက်ကို မတီထွင်ရန်၊ အဆုံးမှာ စိတ်ဝင်စားစရာဖြစ်ရန်။ စာကြောင်းတိုတိုနှင့် အသံဖတ်ရန်အဆင်ပြေအောင်ရေးပါ။\n\nအကြောင်းအရာ:\n{source}'''
    result = client.chat.completions.create(model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        messages=[{'role':'system','content':'မြန်မာ Movie Recap Script ရေးသားရာတွင် ကျွမ်းကျင်သူ။'}, {'role':'user','content':prompt}], temperature=0.7)
    return {'ok': True, 'demo': False, 'script': result.choices[0].message.content}

@app.get('/health')
def health():
    return {'ok': True, 'service': '9/Mandalay Movie Recap AI'}
