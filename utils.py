import torch


def euclidean_distance(a, b):
    return torch.norm(a - b, p=2)


def predict_font(embedding, average_embeddings):
    min_distance = float('inf')
    best_label = None

    embedding = torch.tensor(embedding) if type(embedding) is not torch.Tensor else embedding

    for label, avg_emb in average_embeddings.items():
        avg_emb = torch.tensor(avg_emb) if type(avg_emb) is not torch.Tensor else avg_emb
        distance = euclidean_distance(embedding, avg_emb)

        if distance.item() < min_distance:
            min_distance = distance.item()
            best_label = label

    return best_label


def predict_top_fonts(embedding, average_embeddings, top_n=3):
    distances = []

    embedding = torch.tensor(embedding) if type(embedding) is not torch.Tensor else embedding

    for label, avg_emb in average_embeddings.items():
        avg_emb = torch.tensor(avg_emb) if type(avg_emb) is not torch.Tensor else avg_emb
        distance = euclidean_distance(embedding, avg_emb)
        distances.append((label, distance.item()))

    distances.sort(key=lambda x: x[1])

    top_labels = [label for label, _ in distances[:top_n]]

    return top_labels
