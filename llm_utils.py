import requests

def call_ollama(prompt, timeout=180):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2:7b",
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )
        # 先判断HTTP状态码是否正常
        if response.status_code != 200:
            print(f"⚠️ Ollama返回错误状态码：{response.status_code}")
            return ""
        
        data = response.json()
        # 检查response字段是否存在
        if "response" not in data:
            print("⚠️ Ollama返回格式错误，缺少response字段")
            return ""
        
        return data["response"].strip()
    except requests.exceptions.ConnectionError:
        print("⚠️ 无法连接Ollama，请检查Ollama是否启动")
        return ""
    except requests.exceptions.Timeout:
        print("⚠️ Ollama响应超时，建议换更小的模型")
        return ""
    except Exception as e:
        print(f"⚠️ Ollama调用失败：{str(e)}")
        return ""