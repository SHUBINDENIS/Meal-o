def calculate_total_nutrition(recipes, selected_names):
    selected = recipes[recipes["name"].isin(selected_names)]
    return {
        "calories": selected["calories"].sum(),
        "protein": selected["protein"].sum(),
        "fat": selected["fat"].sum(),
        "carbs": selected["carbs"].sum()
    }
