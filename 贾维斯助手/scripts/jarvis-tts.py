#!/usr/bin/env python3
"""贾维斯语音合成 — Edge TTS (微软自然中文) + Tingting 降级"""
import subprocess, sys, json, os, asyncio, tempfile

# 首选：Edge TTS — 微软自然中文语音
async def edge_speak(text, voice="zh-CN-XiaoxiaoNeural"):
    try:
        import edge_tts
        f = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        out = f.name; f.close()
        communicate = edge_tts.Communicate(text[:1000], voice)
        await communicate.save(out)
        subprocess.run(['afplay', out], capture_output=True, timeout=60)
        os.unlink(out)
        return {"spoken": True, "engine": "edge-tts", "voice": voice}
    except Exception as e:
        return {"spoken": False, "error": str(e), "engine": "edge-tts"}

# 降级：macOS say (婷婷 - 最自然的中文系统语音)
def say_speak(text, voice="Tingting"):
    try:
        subprocess.run(["say", "-v", voice, text[:500]], check=True, timeout=60)
        return {"spoken": True, "engine": "say", "voice": voice}
    except Exception as e:
        return {"spoken": False, "error": str(e), "engine": "say"}

def speak(text):
    if not text:
        return {"spoken": False, "error": "empty text"}
    
    # 尝试 Edge TTS (微软自然中文)
    try:
        result = asyncio.run(edge_speak(text))
        if result["spoken"]:
            return result
    except:
        pass
    
    # 降级到 macOS say
    return say_speak(text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list-voices":
        # 列出 Edge TTS 中文语音
        try:
            import edge_tts
            voices = asyncio.run(edge_tts.list_voices())
            zh_voices = [v for v in voices if v["Locale"].startswith("zh")]
            for v in zh_voices:
                print(f'{v["ShortName"]} ({v["Locale"]}) — {v["FriendlyName"]}')
        except:
            print("Edge TTS 不可用")
    else:
        text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
        result = speak(text)
        print(json.dumps(result, ensure_ascii=False))
