import json
import math

def calculate(recipe, output_per_minute):
    """
    Рассчитывает производственную цепочку.
    Возвращает список всех зданий с их связями.
    """
    with open('recipes.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)
    
    if recipe not in recipes:
        return None
    
    # Список всех зданий (каждое здание - отдельный элемент)
    buildings = []
    # Связи между зданиями (от какого к какому, сколько ресурсов)
    connections = []
    
    # Счетчик для уникальных ID
    building_id = [0]
    
    def process_recipe(recipe_name, required_output, level):
        """Рекурсивно обрабатывает рецепт и создает здания"""
        if recipe_name not in recipes:
            # Базовый ресурс (руда) - создаем один "источник"
            b_id = building_id[0]
            building_id[0] += 1
            buildings.append({
                'id': b_id,
                'name': recipe_name,
                'building': 'Источник',
                'level': level,
                'output': required_output,
                'is_source': True
            })
            return [b_id]  # Возвращаем список ID зданий
        
        recipe_data = recipes[recipe_name]
        recipe_output = recipe_data['output']
        building_type = recipe_data['building']
        
        # Сколько циклов нужно в минуту
        cycles_needed = required_output / recipe_output
        # Сколько зданий нужно (округляем вверх)
        num_buildings = math.ceil(cycles_needed)
        
        # Создаем здания для этого рецепта
        current_building_ids = []
        for i in range(num_buildings):
            b_id = building_id[0]
            building_id[0] += 1
            buildings.append({
                'id': b_id,
                'name': recipe_name,
                'building': building_type,
                'level': level,
                'output': required_output / num_buildings,
                'building_num': i + 1,
                'total_buildings': num_buildings,
                'is_source': False
            })
            current_building_ids.append(b_id)
        
        # Обрабатываем ингредиенты
        for ingredient_name, amount_per_cycle in recipe_data['ingredients'].items():
            # Сколько ингредиента нужно в минуту
            ingredient_needed = cycles_needed * amount_per_cycle
            
            # Рекурсивно создаем здания для ингредиента
            child_ids = process_recipe(ingredient_name, ingredient_needed, level + 1)
            
            # Создаем связи от зданий ингредиента к текущим зданиям
            # Распределяем связи равномерно
            for i, parent_id in enumerate(current_building_ids):
                # Выбираем соответствующее здание-источник
                child_idx = int((i / len(current_building_ids)) * len(child_ids))
                child_id = child_ids[child_idx]
                
                connections.append({
                    'from': child_id,
                    'to': parent_id,
                    'resource': ingredient_name,
                    'amount': ingredient_needed / len(current_building_ids)
                })
        
        return current_building_ids
    
    # Запускаем обработку с корневого рецепта
    process_recipe(recipe, output_per_minute, 0)
    
    return {
        'target_recipe': recipe,
        'target_output': output_per_minute,
        'buildings': buildings,
        'connections': connections
    }
