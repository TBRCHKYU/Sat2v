import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.widgets import Button
import matplotlib.patheffects as path_effects
import math


# Цвета для разных типов зданий
BUILDING_COLORS = {
    'Assembler': '#3498DB',      # Синий
    'Constructor': '#27AE60',    # Зеленый
    'Smelter': '#E67E22',        # Оранжевый
    'Источник': '#95A5A6',       # Серый
    'Miner': '#95A5A6',          # Серый
    'default': '#9B59B6'         # Фиолетовый
}

# Темная тема (более контрастная)
COLORS = {
    'bg': '#0f0f1a',
    'text': '#ffffff',           # Чистый белый для лучшей читаемости
    'text_dark': '#1a1a2e',      # Темный текст для обводки
    'grid': '#16213e',
    'accent': '#ff6b6b'          # Более яркий акцент
}

# Эффект обводки для текста
TEXT_OUTLINE = [path_effects.withStroke(linewidth=3, foreground='black')]


def draw(production_data, save_path=None, show=True):
    """
    Визуализирует производственную цепочку.
    Каждое здание - отдельный блок.
    Поддерживает перемещение и масштабирование (колесико мыши, перетаскивание).
    """
    if not production_data:
        print("Нет данных для визуализации")
        return None
    
    buildings = production_data['buildings']
    connections = production_data['connections']
    
    if not buildings:
        print("Нет зданий для отображения")
        return None
    
    # Вычисляем позиции зданий
    positions = calculate_positions(buildings)
    
    # Создаем фигуру
    fig, ax = plt.subplots(figsize=(16, 10), facecolor=COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])
    
    # Заголовок (крупный и заметный)
    title = f"Производство: {production_data['target_recipe']} ({production_data['target_output']}/мин)"
    fig.suptitle(title, fontsize=18, color=COLORS['text'], fontweight='bold')
    
    # Рисуем связи (сначала, чтобы были под блоками)
    draw_connections(ax, connections, buildings, positions)
    
    # Рисуем здания
    draw_buildings(ax, buildings, positions)
    
    # Настраиваем оси
    setup_axes(ax, positions)
    
    # Добавляем легенду
    add_legend(ax)
    
    # Добавляем подсказку
    fig.text(0.5, 0.02, 
             'Колесико мыши - масштаб | Зажать колесико/ПКМ - перемещение | Двойной клик - сброс',
             ha='center', fontsize=11, color=COLORS['text'], alpha=0.9, fontweight='bold')
    
    # Включаем интерактивность
    enable_interactivity(fig, ax, positions)
    
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    
    if save_path:
        plt.savefig(save_path, facecolor=COLORS['bg'], dpi=150, bbox_inches='tight')
        print(f"Сохранено: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def calculate_positions(buildings):
    """Вычисляет позиции для каждого здания"""
    positions = {}
    
    # Группируем здания по уровням
    levels = {}
    for b in buildings:
        level = b['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(b)
    
    # Размеры блока (увеличены для размещения текста)
    block_width = 130
    block_height = 100
    h_spacing = 50  # Горизонтальный отступ
    v_spacing = 180  # Вертикальный отступ между уровнями
    
    # Размещаем здания по уровням (снизу вверх)
    max_level = max(levels.keys()) if levels else 0
    
    for level, level_buildings in levels.items():
        # Y позиция (уровень 0 сверху, максимальный снизу)
        y = (max_level - level) * v_spacing
        
        # Ширина всех зданий на этом уровне
        total_width = len(level_buildings) * block_width + (len(level_buildings) - 1) * h_spacing
        start_x = -total_width / 2
        
        for i, building in enumerate(level_buildings):
            x = start_x + i * (block_width + h_spacing) + block_width / 2
            positions[building['id']] = {
                'x': x,
                'y': y,
                'width': block_width,
                'height': block_height
            }
    
    return positions


def truncate_text(text, max_chars):
    """Сокращает текст до максимальной длины"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars-2] + '..'


def wrap_text(text, max_chars_per_line):
    """Разбивает текст на строки"""
    if len(text) <= max_chars_per_line:
        return text
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (" " + word) if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # Максимум 2 строки
    if len(lines) > 2:
        lines = [lines[0], truncate_text(' '.join(lines[1:]), max_chars_per_line)]
    
    return '\n'.join(lines)


def draw_buildings(ax, buildings, positions):
    """Рисует все здания"""
    for building in buildings:
        pos = positions[building['id']]
        x, y = pos['x'], pos['y']
        w, h = pos['width'], pos['height']
        
        # Цвет здания
        building_type = building.get('building', 'default')
        color = BUILDING_COLORS.get(building_type, BUILDING_COLORS['default'])
        
        # Тень
        shadow = Rectangle(
            (x - w/2 + 3, y - h/2 - 3), w, h,
            facecolor='black', alpha=0.3, zorder=1
        )
        ax.add_patch(shadow)
        
        # Основной блок
        rect = Rectangle(
            (x - w/2, y - h/2), w, h,
            facecolor=color, edgecolor=COLORS['text'],
            linewidth=2, zorder=2
        )
        ax.add_patch(rect)
        
        # Максимум символов в строке (зависит от ширины блока)
        max_chars = int(w / 9)
        
        # Название (с переносом строки если нужно)
        name = building['name']
        display_name = wrap_text(name, max_chars)
        
        # Считаем количество строк в названии для смещения
        name_lines = display_name.count('\n') + 1
        name_offset = 30 if name_lines == 1 else 35
        
        ax.text(x, y + name_offset, display_name, ha='center', va='center',
                fontsize=12, color=COLORS['text'], fontweight='bold', zorder=3,
                linespacing=0.9, path_effects=TEXT_OUTLINE)
        
        # Тип здания (сокращаем если нужно)
        building_text = truncate_text(building_type, max_chars)
        ax.text(x, y, building_text, ha='center', va='center',
                fontsize=10, color=COLORS['text'], fontweight='bold', zorder=3,
                path_effects=TEXT_OUTLINE)
        
        # Номер здания (если несколько)
        if building.get('total_buildings', 1) > 1:
            num_text = f"#{building.get('building_num', 1)}/{building.get('total_buildings', 1)}"
            ax.text(x, y - 28, num_text, ha='center', va='center',
                    fontsize=11, color=COLORS['text'], fontweight='bold', zorder=3,
                    path_effects=TEXT_OUTLINE)
        
        # Выход (под блоком)
        output = building.get('output', 0)
        if output > 0:
            ax.text(x, y - h/2 - 15, f"{output:.1f}/мин", ha='center', va='top',
                    fontsize=11, color=COLORS['accent'], fontweight='bold', zorder=3,
                    path_effects=TEXT_OUTLINE)


def draw_connections(ax, connections, buildings, positions):
    """Рисует связи между зданиями"""
    # Создаем словарь зданий по ID
    buildings_dict = {b['id']: b for b in buildings}
    
    for conn in connections:
        from_id = conn['from']
        to_id = conn['to']
        
        if from_id not in positions or to_id not in positions:
            continue
        
        from_pos = positions[from_id]
        to_pos = positions[to_id]
        
        # Координаты начала и конца стрелки (с отступом от блоков)
        x1 = from_pos['x']
        y1 = from_pos['y'] + from_pos['height'] / 2 + 5  # Верх блока + отступ
        x2 = to_pos['x']
        y2 = to_pos['y'] - to_pos['height'] / 2 - 20  # Низ блока - отступ для текста
        
        # Рисуем стрелку
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle='-|>',
            mutation_scale=20,
            color=COLORS['text'],
            linewidth=2,
            alpha=0.8,
            zorder=0
        )
        ax.add_patch(arrow)
        
        # Метка с количеством ресурса
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        amount = conn.get('amount', 0)
        if amount > 0:
            ax.text(mid_x + 8, mid_y, f"{amount:.1f}", ha='left', va='center',
                    fontsize=10, color=COLORS['text'], fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['bg'], 
                             edgecolor=COLORS['text'], alpha=0.95, linewidth=1.5),
                    zorder=1)


def setup_axes(ax, positions):
    """Настраивает оси графика"""
    if not positions:
        ax.set_xlim(-500, 500)
        ax.set_ylim(-500, 500)
        return
    
    # Находим границы (с учетом размеров блоков и текста)
    all_x = [p['x'] for p in positions.values()]
    all_y = [p['y'] for p in positions.values()]
    
    min_x = min(all_x) - 200
    max_x = max(all_x) + 200
    min_y = min(all_y) - 200  # Больше места снизу для текста под блоками
    max_y = max(all_y) + 180
    
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    
    # Убираем оси
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Сетка
    ax.grid(True, linestyle='--', alpha=0.2, color=COLORS['text'])


def add_legend(ax):
    """Добавляет легенду с типами зданий"""
    legend_items = []
    for name, color in BUILDING_COLORS.items():
        if name != 'default':
            patch = Rectangle((0, 0), 1, 1, facecolor=color, edgecolor=COLORS['text'], linewidth=2)
            legend_items.append((patch, name))
    
    if legend_items:
        patches, labels = zip(*legend_items)
        legend = ax.legend(patches, labels, loc='upper right', 
                          facecolor=COLORS['bg'], edgecolor=COLORS['text'],
                          labelcolor=COLORS['text'], fontsize=12,
                          framealpha=0.95)
        # Делаем рамку легенды толще
        legend.get_frame().set_linewidth(2)


def enable_interactivity(fig, ax, positions):
    """Включает интерактивность: масштабирование и перемещение"""
    
    # Сохраняем начальные границы для сброса
    initial_xlim = ax.get_xlim()
    initial_ylim = ax.get_ylim()
    
    # Состояние для перетаскивания
    state = {
        'dragging': False,
        'last_x': None,
        'last_y': None
    }
    
    def on_scroll(event):
        """Масштабирование колесиком мыши"""
        if event.inaxes != ax:
            return
        
        # Фактор масштабирования
        scale_factor = 1.2
        
        if event.button == 'up':
            scale = 1 / scale_factor
        elif event.button == 'down':
            scale = scale_factor
        else:
            return
        
        # Текущие границы
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Центр масштабирования - позиция мыши
        x_center = event.xdata
        y_center = event.ydata
        
        # Новые границы
        new_width = (xlim[1] - xlim[0]) * scale
        new_height = (ylim[1] - ylim[0]) * scale
        
        # Масштабируем относительно позиции мыши
        rel_x = (x_center - xlim[0]) / (xlim[1] - xlim[0])
        rel_y = (y_center - ylim[0]) / (ylim[1] - ylim[0])
        
        ax.set_xlim(x_center - new_width * rel_x, x_center + new_width * (1 - rel_x))
        ax.set_ylim(y_center - new_height * rel_y, y_center + new_height * (1 - rel_y))
        
        fig.canvas.draw_idle()
    
    def on_press(event):
        """Начало перетаскивания"""
        if event.inaxes != ax:
            return
        
        # Средняя кнопка (колесико) или правая кнопка
        if event.button in [2, 3]:
            state['dragging'] = True
            state['last_x'] = event.xdata
            state['last_y'] = event.ydata
    
    def on_release(event):
        """Конец перетаскивания"""
        state['dragging'] = False
        state['last_x'] = None
        state['last_y'] = None
    
    def on_motion(event):
        """Перетаскивание"""
        if not state['dragging'] or event.inaxes != ax:
            return
        
        if state['last_x'] is None or event.xdata is None:
            return
        
        # Смещение
        dx = state['last_x'] - event.xdata
        dy = state['last_y'] - event.ydata
        
        # Текущие границы
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Новые границы
        ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
        ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
        
        fig.canvas.draw_idle()
    
    def on_double_click(event):
        """Сброс масштаба при двойном клике"""
        if event.dblclick and event.inaxes == ax:
            ax.set_xlim(initial_xlim)
            ax.set_ylim(initial_ylim)
            fig.canvas.draw_idle()
    
    # Подключаем обработчики событий
    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_press_event', on_double_click)
