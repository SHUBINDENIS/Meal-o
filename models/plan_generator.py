import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_meal_plan(user_profile, available_recipes, calorie_target):
    prompt = f"""Составь подробный рацион питания на день из доступных рецептов, чтобы удовлетворить следующие параметры:
- Цель: {user_profile['goal']}
- Ограничения: {user_profile['restrictions']}
- Суточная калорийность: {calorie_target} ккал
- Доступные блюда: {', '.join(available_recipes['name'].tolist())}
Формат ответа: завтрак, обед, ужин, перекус (название блюда).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Используем доступную тебе модель
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )

    return response.choices[0].message.content
