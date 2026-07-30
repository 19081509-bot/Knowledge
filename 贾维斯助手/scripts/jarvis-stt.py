#!/usr/bin/env python3
"""达摩院 SenseVoiceSmall STT — 通过 SiliconFlow API 实现中文语音识别"""
import subprocess, sys, json, os, tempfile, requests

API_KEY = "sk-iybgixsjrstotytjuwwlmwuannkgjaexqrnlijrhvkfnogqy"
API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
MODEL = "FunAudioLLM/SenseVoiceSmall"

def record(duration=5):
    """录音 → WAV 16kHz 单声道"""
    f = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    output = f.name; f.close()
    subprocess.run(['ffmpeg', '-y', '-f', 'avfoundation', '-i', ':0',
                    '-t', str(duration), '-ac', '1', '-ar', '16000',
                    '-acodec', 'pcm_s16le', output],
                   capture_output=True, timeout=duration+5)
    return output

def transcribe(wav_path):
    """调用 SiliconFlow SenseVoiceSmall API 进行转录"""
    with open(wav_path, 'rb') as f:
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": ("audio.wav", f, "audio/wav")},
            data={"model": MODEL, "language": "zh"},
            timeout=30
        )
    if resp.status_code != 200:
        return {"error": f"API错误 {resp.status_code}: {resp.text}"}
    result = resp.json()
    text = result.get("text", "").strip()
    return {"text": text}

if __name__ == '__main__':
    dur = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    wav = record(dur)
    print(json.dumps({"event": "recorded", "file": wav, "size": os.path.getsize(wav)}), flush=True)
    result = transcribe(wav)
    os.unlink(wav)
    print(json.dumps(result, ensure_ascii=False))
