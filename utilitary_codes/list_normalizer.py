import pickle
import os

# Dicionários de equivalência
genre_equivalents = {
    "Acción": "Action",
    "Acesso Antecipado": "Early Access",
    "Aventura": "Adventure",
    "Ação": "Action",
    "Corrida": "Racing",
    "Estrategia": "Strategy",
    "Rol": "RPG",
    "Simuladores": "Simulation",
    "Strategie": "Strategy",
    "Stratégie": "Strategy",
    "Symulacje": "Simulation",
    "Анимация и моделирование": "Animation & Modeling",
    "Бесплатные": "Free To Play",
    "Дизайн и иллюстрация": "Design & Illustration",
    "Инди": "Indie",
    "Казуальные игры": "Casual",
    "Обработка фото": "Photo Editing",
    "Приключенческие игры": "Adventure",
    "Симуляторы": "Simulation",
    "Спорт": "Sports",
    "Утилиты": "Utilities",
    "Экшены": "Action",
    "冒險": "Adventure",
    "角色扮演": "RPG"
}

category_equivalents = {
    "Cartes à échanger Steam": "Steam Trading Cards",
    "Classificações Steam": "Steam Ratings",
    "Compartilhamento em família": "Family Sharing",
    "Compat. contrôleurs complète": "Full Controller Support",
    "Compat. contrôleurs partielle": "Partial Controller Support",
    "Compat. parcial com controle": "Partial Controller Support",
    "Compat. parcial con control": "Partial Controller Support",
    "Compat. parcial con mando": "Partial Controller Support",
    "Compat. total com controle": "Full Controller Support",
    "Compatíveis com RV": "VR Supported",
    "Compras dentro de la aplicación": "In-App Purchases",
    "Conquistas Steam": "Steam Achievements",
    "Cooperativo": "Co-op",
    "Cooperativo on-line": "Online Co-op",
    "Cromos de Steam": "Steam Trading Cards",
    "Estadísticas": "Stats",
    "Estatísticas": "Stats",
    "HDR disponible": "HDR available",
    "JcJ en ligne": "Online PvP",
    "Jednoosobowa": "Single-player",
    "JxJ": "PvP",
    "JxJ on-line": "Online PvP",
    "JxJ tela dividida/compart.": "Shared/Split Screen PvP",
    "Karty kolekcjonerskie Steam": "Steam Trading Cards",
    "Logros de Steam": "Steam Achievements",
    "Multijogador": "Multi-player",
    "Multijoueur": "Multi-player",
    "Multijoueur multiplateforme": "Cross-Platform Multiplayer",
    "Nuvem Steam": "Steam Cloud",
    "Osiągnięcia Steam": "Steam Achievements",
    "Partage familial": "Family Sharing",
    "Partilha de Biblioteca": "Family Sharing",
    "Préstamo familiar": "Family Sharing",
    "PvP online": "Online PvP",
    "Remote Play para tabletas": "Remote Play on Tablet",
    "Remote Play sur tablette": "Remote Play on Tablet",
    "Remote Play sur téléphone": "Remote Play on Phone",
    "Remote Play sur télévision": "Remote Play on TV",
    "Remote Play на планшете": "Remote Play on Tablet",
    "Remote Play на телевизоре": "Remote Play on TV",
    "Remote Play на телефоне": "Remote Play on Phone",
    "Solo": "Single-player",
    "Steam 成就": "Steam Achievements",
    "Steam 雲端": "Steam Cloud",
    "Subtítulos disponibles": "Captions available",
    "Succès Steam": "Steam Achievements",
    "Tablas de clasificación de Steam": "Steam Leaderboards",
    "Tarjetas de Steam": "Steam Trading Cards",
    "Udostępnianie gier": "Family Sharing",
    "Um jogador": "Single-player",
    "Un jugador": "Single-player",
    "Warsztat Steam": "Steam Workshop",
    "Wieloosobowa": "Multi-player",
    "Wieloplatformowa wieloosobowa": "Cross-Platform Multiplayer",
    "Workshop Steam": "Steam Workshop",
    "Внутриигровые покупки": "In-App Purchases",
    "Для нескольких игроков": "Multi-player",
    "Для одного игрока": "Single-player",
    "Достижения Steam": "Steam Achievements",
    "Игрок против игрока": "PvP",
    "Игрок против игрока (общий/разделённый экран)": "Shared/Split Screen PvP",
    "Игрок против игрока (по сети)": "Online PvP",
    "Коллекционные карточки Steam": "Steam Trading Cards",
    "Кооператив": "Co-op",
    "Кооператив (общий/разделённый экран)": "Shared/Split Screen Co-op",
    "Кооператив (по сети)": "Online Co-op",
    "Мастерская Steam": "Steam Workshop",
    "Общий/разделённый экран": "Shared/Split Screen",
    "Полная поддержка контроллеров": "Full Controller Support",
    "С редактором уровней": "Includes level editor",
    "Семейный доступ": "Family Sharing",
    "Скрытые субтитры": "Captions available",
    "Таблицы лидеров Steam": "Steam Leaderboards",
    "Частичная поддержка контроллеров": "Partial Controller Support",
    "單人": "Single-player",
    "完全支援控制器": "Full Controller Support",
    "親友同享": "Family Sharing"
}

# Funções auxiliares
def normalize_str(s):
    return s.strip() if isinstance(s, str) else ""

def apply_equivalents(lst, eq_map):
    descriptions = []
    for dict in lst:
        desc = dict['description']
        mapped_desc = eq_map.get(desc, desc)
        temp_dict = {
            'description' : mapped_desc,
            'id' : dict['id']
        }
        descriptions.append(temp_dict)
    
    return descriptions

# Lista de arquivos para processar
file_pairs = [
    ("filtered_games/mixed.p", "normalized_filtered_games/mixed_normalized.p"),
    ("filtered_games/mostly_positive.p", "normalized_filtered_games/mostly_positive_normalized.p"),
    ("filtered_games/positive.p", "normalized_filtered_games/positive_normalized.p"),
    ("filtered_games/overwhelmingly_positive.p", "normalized_filtered_games/overwhelmingly_positive_normalized.p"),
    ("filtered_games/very_positive.p", "normalized_filtered_games/very_positive_normalized.p")
]

# Processar cada arquivo
for input_path, output_path in file_pairs:
    # Verificar se o arquivo de entrada existe
    if not os.path.exists(input_path):
        print(f"Arquivo de entrada não encontrado: {input_path}")
        continue
    
    # Carregar dados
    with open(input_path, "rb") as f:
        games = pickle.load(f)
    
    # Aplicar normalização
    for game in games.values():
        game["genres"] = apply_equivalents(game.get("genres", []), genre_equivalents)
        game["categories"] = apply_equivalents(game.get("categories", []), category_equivalents)
        game["developers"] = [normalize_str(d) for d in game.get("developers", []) if isinstance(d, str)]
        game["publishers"] = [normalize_str(p) for p in game.get("publishers", []) if isinstance(p, str)]
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salvar arquivo atualizado
    with open(output_path, "wb") as f:
        pickle.dump(games, f)
    
    print(f"Arquivo processado e salvo em: {output_path}")