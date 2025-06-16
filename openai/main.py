

from openai import OpenAI


def main():
    req_deepseek()


def req_deepseek():
    api_key = "xxx"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        timeout=30,
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "想要拥有”睡后收入“的核心是什么"},
        ],
        stream=False
    )

    # for chunk in response.response.iter_bytes():
        # print(chunk)
    # print(response.response.json())
    print(response.choices[0].message.content)


if __name__ == '__main__':
    main()



