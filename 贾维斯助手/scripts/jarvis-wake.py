#!/usr/bin/env python3
"""贾维斯唤醒助手 — 本地 VAD 过滤 + SenseVoiceSmall API + Edge TTS"""
import subprocess, sys, json, os, tempfile, time, re, signal, requests, struct

HOME = os.path.expanduser('~')
TTS_SH = os.path.join(HOME, 'scripts/jarvis-tts.py')
AK = "sk-iybgixsjrstotytjuwwlmwuannkgjaexqrnlijrhvkfnogqy"
STT_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
STT_MODEL = "FunAudioLLM/SenseVoiceSmall"

WAKE = ['贾维斯','佳维斯','嘉维斯','家维斯','加维斯','甲维斯',
        'jarvis','jiaweisi','jia维斯']

# 防抖/限流
MIN_API_INTERVAL = 3.0     # 两次API调用最小间隔(秒)
API_BACKOFF_BASE = 2.0     # 错误后退避基数(秒)
last_api_time = 0
api_error_count = 0

def plog(d):
    print(json.dumps(d, ensure_ascii=False), flush=True)

def record(dur=5):
    f = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    out = f.name; f.close()
    subprocess.run(['ffmpeg','-y','-f','avfoundation','-i',':0',
        '-t',str(dur),'-ac','1','-ar','16000','-acodec','pcm_s16le',out],
        capture_output=True, timeout=dur+5)
    return out

def has_speech(path):
    """本地 VAD：检测音频是否有真实人声"""
    with open(path,'rb') as f: data = f.read()
    if len(data) <= 44: return False
    samples = struct.unpack(f'<{(len(data)-44)//2}h', data[44:])
    n = len(samples)
    # 统计不同振幅段帧数
    moderate = sum(1 for s in samples if abs(s) > 5000)   # 中等音量
    strong = sum(1 for s in samples if abs(s) > 10000)    # 大音量
    spike = sum(1 for s in samples if abs(s) > 20000)     # 峰值
    # 人声判断：有足够多的中等+强信号，且分散分布
    return (moderate > n * 0.01) and (strong > 5 or spike > 2)

def transcribe(path):
    global last_api_time, api_error_count
    now = time.time()
    # 限流：最小间隔
    elapsed = now - last_api_time
    if elapsed < MIN_API_INTERVAL:
        time.sleep(MIN_API_INTERVAL - elapsed)
    # 错误后退避
    if api_error_count > 0:
        backoff = min(API_BACKOFF_BASE ** api_error_count, 60)
        plog({'e':'backoff','wait':f'{backoff:.0f}s','errors':api_error_count})
        time.sleep(backoff)
    try:
        with open(path,'rb') as f:
            r = requests.post(STT_URL,
                headers={'Authorization':f'Bearer {AK}'},
                files={'file':('audio.wav',f,'audio/wav')},
                data={'model':STT_MODEL,'language':'zh'},
                timeout=30)
        last_api_time = time.time()
        if r.status_code == 200:
            api_error_count = 0
            return r.json().get('text','').strip()
        elif r.status_code == 429:
            api_error_count += 1
            plog({'e':'rate_limit','errors':api_error_count})
        elif r.status_code >= 500:
            api_error_count += 1
            plog({'e':'server_error','status':r.status_code,'errors':api_error_count})
        else:
            api_error_count += 1
            plog({'e':'api_error','status':r.status_code,'body':r.text[:100]})
        return ''
    except requests.exceptions.Timeout:
        api_error_count += 1
        plog({'e':'timeout','errors':api_error_count})
        return ''
    except Exception as e:
        api_error_count += 1
        plog({'e':'exception','err':str(e)[:80],'errors':api_error_count})
        return ''

def norm(t):
    return t.lower().replace(' ','').replace('，','').replace('。','').replace('？','').replace('！','')

def has_wake(text):
    if not text: return False
    t = norm(text)
    for w in WAKE:
        if w.lower() in t: return True
    if 'jia' in t and ('si' in t or 'wei' in t): return True
    return False

def extract_cmd(text):
    t = norm(text)
    for w in sorted(WAKE, key=len, reverse=True):
        if w.lower() in t:
            idx = t.index(w.lower()) + len(w)
            return text[idx:].strip().lstrip('，。？！?,.:；、').strip()
    return text

def speak(text):
    if not text: return
    plog({'e':'speak','t':text[:80]})
    try: subprocess.run(['python3',TTS_SH,text[:500]], capture_output=True, timeout=60)
    except: pass

def ask_claw(cmd):
    if not cmd: return ''
    plog({'e':'thinking'})
    try:
        r = subprocess.run(['openclaw','agent','--agent','main','--message',cmd,
            '--json','--timeout','60'], capture_output=True, text=True, timeout=70)
        out = r.stdout
        try:
            d = json.loads(out)
            for p in d.get('result',{}).get('payloads',[]):
                if p.get('text'): return p['text']
        except: pass
        return out[:800] if out.strip() else ''
    except subprocess.TimeoutExpired:
        plog({'e':'claw_timeout'})
        return '还没想好，请再说一遍'
    except Exception as e:
        plog({'e':'claw_error','err':str(e)[:80]})
        return '我遇到了点问题，请再说一遍'

def clean(text):
    if not text or len(text) < 2: return '没听清楚，请再说一遍'
    text = re.sub(r'```[\s\S]*?```','',text)
    text = re.sub(r'[*_~>`#|\[\]()]','',text)
    text = re.sub(r'\n+','，',text).strip()[:500]
    return text or '没听清楚，请再说一遍'

def main():
    plog({'e':'status','m':'🔔 说「贾维斯」+ 指令唤醒我'})
    while True:
        wav = record(5)
        if not has_speech(wav):
            try: os.unlink(wav)
            except: pass
            continue
        text = transcribe(wav)
        try: os.unlink(wav)
        except: pass
        if not text: continue
        plog({'e':'heard','t':text})
        if not has_wake(text): continue
        cmd = extract_cmd(text)
        plog({'e':'wake','cmd':cmd})
        speak('好的')
        reply = ask_claw(cmd or text)
        speak(clean(reply))
        time.sleep(1)

signal.signal(signal.SIGINT, lambda s,f: (plog({'e':'stopped'}), sys.exit(0)))

if __name__ == '__main__': main()
