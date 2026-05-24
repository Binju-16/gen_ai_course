import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in .env")

model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
policy_path = os.path.join("data", "example_policies", "policy_1_grade_levels.txt")
if not os.path.exists(policy_path):
    raise FileNotFoundError(policy_path)

with open(policy_path, "r", encoding="utf-8") as f:
    policy = f.read()

client = OpenAI(api_key=api_key)

for label, prompt_file in [("V1", "docs/system_prompt_v1.md"), ("V2", "docs/system_prompt.md")]:
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(prompt_file)

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    print("=== ", label, prompt_file)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": policy},
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    content = response.choices[0].message.content
    output_text = content.strip()
    print(output_text)
    print()

    out_path = f"evaluation_output_{label.lower()}.txt"
    with open(out_path, "w", encoding="utf-8") as out_file:
        out_file.write(output_text)
    print(f"Saved {label} output to {out_path}")
    print()