from openai import OpenAI
import sys


def stream_chat(api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1"
    )

    messages = [
        {
            "role": "system",
            "content": "你是Kimi，由Moonshot AI提供的人工智能助手。"
        }
    ]

    print("Kimi聊天机器人（流式模式）")
    print("=" * 50)

    while True:
        user_input = input("\n你: ")
        if user_input.lower() == 'exit':
            break

        messages.append({"role": "user", "content": user_input})

        # 流式调用
        stream = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=messages,
            temperature=0.6,
            stream=True,  # 启用流式输出
        )

        print("\nKimi: ", end="", flush=True)
        assistant_message = ""

        for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta.content:
                    print(delta.content, end="", flush=True)
                    assistant_message += delta.content

        print()  # 换行
        # 将完整回复添加到历史
        messages.append({"role": "assistant", "content": assistant_message})

        # 控制历史长度
        if len(messages) > 20:
            messages = [messages[0]] + messages[-19:]


if __name__ == "__main__":
    # 建议将API Key存入环境变量
    import os

    API_KEY = os.getenv("MOONSHOT_API_KEY", "YOUR_API_KEY")
    stream_chat(API_KEY)