import os
import pickle
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm

# --- Etapa 1: Carregar os dados de todos os arquivos ---

def load_all_games(folder):
    all_games = {}
    for filename in os.listdir(folder):
        if filename.endswith('.p'):
            with open(os.path.join(folder, filename), 'rb') as f:
                games = pickle.load(f)
                all_games.update(games)
    return all_games

games = load_all_games('filtered_games')
games_list = list(games.values())

# --- Etapa 2: Codificar os atributos estruturados ---

def encode_features(games):
    mlb_genres = MultiLabelBinarizer()
    mlb_categories = MultiLabelBinarizer()
    mlb_platforms = MultiLabelBinarizer()

    genres = [g.get("genres", []) for g in games]
    categories = [g.get("categories", []) for g in games]
    platforms = [[k for k, v in g.get("platforms", {}).items() if v] for g in games]

    X_genres = mlb_genres.fit_transform(genres)
    X_categories = mlb_categories.fit_transform(categories)
    X_platforms = mlb_platforms.fit_transform(platforms)

    prices = torch.tensor([
        g.get("price_overview", {}).get("final", 0) / 100.0 for g in games
    ]).unsqueeze(1)

    years = torch.tensor([
        int(g.get("release_date", {}).get("date", "2000")[-4:]) if g.get("release_date") else 2000 for g in games
    ]).unsqueeze(1)

    X_numerical = torch.cat([prices, years], dim=1)
    X_numerical = (X_numerical - X_numerical.mean(dim=0)) / X_numerical.std(dim=0)

    X = torch.tensor(
        torch.cat([torch.tensor(X_genres).float(),
                   torch.tensor(X_categories).float(),
                   torch.tensor(X_platforms).float(),
                   X_numerical], dim=1)
    )
    return X, mlb_genres, mlb_categories, mlb_platforms

node_features, _, _, _ = encode_features(games_list)

# --- Etapa 3: Construir as conexões do grafo (edge_index) ---

def build_edges(games):
    index_map = {g["appid"]: i for i, g in enumerate(games)}
    edges = set()
    for i, g1 in enumerate(games):
        for j, g2 in enumerate(games):
            if i >= j:
                continue
            if set(g1.get("genres", [])) & set(g2.get("genres", [])) \
               or set(g1.get("categories", [])) & set(g2.get("categories", [])) \
               or g1.get("developers", [None])[0] == g2.get("developers", [None])[0]:
                edges.add((i, j))
                edges.add((j, i))  # grafo não-direcionado
    edge_index = torch.tensor(list(edges)).t().contiguous()
    return edge_index

edge_index = build_edges(games_list)

# --- Etapa 4: Construir o Data object do PyG ---

data = Data(x=node_features, edge_index=edge_index)

# --- Etapa 5: Definir o modelo GNN (Item Tower) ---

class GNNItemTower(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=128, out_dim=64):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, out_dim)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

# --- Exemplo de uso ---

model = GNNItemTower(input_dim=data.x.size(1))
item_embeddings = model(data.x, data.edge_index)  # [n_jogos, embedding_dim]

print("Embeddings gerados para", item_embeddings.shape[0], "jogos.")
