import streamlit as st
import pandas as pd
from models.plan_generator import generate_meal_plan
from utils.filters import filter_recipes_by_restrictions
from utils.nutrition import calculate_total_nutrition

st.title("Meal-o — Персонализированный план питания")

# --- Ввод данных пользователя ---
age = st.slider("Возраст", 10, 90, 25)
weight = st.number_input("Вес (кг)", 30, 200, 70)
height = st.number_input("Рост (см)", 130, 210, 175)
activity = st.selectbox("Физическая активность", ["Низкая", "Средняя", "Высокая"])
goal = st.selectbox("Цель", ["Похудение", "Поддержание", "Набор массы"])
restrictions = st.text_input("Пищевые ограничения (через запятую)", "лактоза, глютен")

# --- Загрузка рецептов ---
recipes = pd.read_csv("data/recipes.csv")

# --- Расчёт целевой калорийности ---
def estimate_calories(weight, height, age, activity, goal):
    base = 10 * weight + 6.25 * height - 5 * age + 5
    factor = {"Низкая": 1.2, "Средняя": 1.55, "Высокая": 1.75}[activity]
    goal_adj = {"Похудение": 0.85, "Поддержание": 1.0, "Набор массы": 1.15}[goal]
    return int(base * factor * goal_adj)

calorie_target = estimate_calories(weight, height, age, activity, goal)

# --- Обработка и генерация ---
if st.button("Сгенерировать рацион"):
    user_profile = {
        "age": age,
        "weight": weight,
        "height": height,
        "activity": activity,
        "goal": goal,
        "restrictions": restrictions.split(",")
    }

    filtered_recipes = filter_recipes_by_restrictions(recipes, user_profile["restrictions"])

    if len(filtered_recipes) < 5:
        st.warning("Слишком мало рецептов после фильтрации. Попробуйте убрать некоторые ограничения.")
    else:
        plan = generate_meal_plan(user_profile, filtered_recipes, calorie_target)
        st.markdown("### Ваш план питания:")
        st.markdown(plan)
