import csv
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_model(X, y):
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X, y)
    return model

def generate_pseudo_labels(model, X_unlabeled, threshold=0.80):
    probabilities = model.predict_proba(X_unlabeled)
    labels = probabilities.argmax(axis=1)
    confidence = probabilities.max(axis=1)
    selected = [(i, int(label), float(conf))
                for i, (label, conf) in enumerate(zip(labels, confidence))
                if conf >= threshold]
    return selected

def save_pseudo_labels(selected, filename="pseudo_labels.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["unlabeled_index", "pseudo_label", "confidence"])
        writer.writerows([[i, label, f"{conf:.4f}"] for i, label, conf in selected])

def main():
    X, y = make_classification(n_samples=500, n_features=4,
                               n_informative=3, n_redundant=0,
                               n_classes=2, class_sep=1.8,
                               random_state=42)
    X_pool, X_test, y_pool, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)

    X_labeled, X_unlabeled = X_pool[:25], X_pool[25:]
    y_labeled = y_pool[:25]

    initial_model = train_model(X_labeled, y_labeled)
    initial_accuracy = accuracy_score(y_test, initial_model.predict(X_test))

    selected = generate_pseudo_labels(initial_model, X_unlabeled, 0.80)
    save_pseudo_labels(selected)

    indices = [x[0] for x in selected]
    pseudo_y = [x[1] for x in selected]
    X_pseudo = X_unlabeled[indices]

    import numpy as np
    X_combined = np.vstack([X_labeled, X_pseudo])
    y_combined = np.concatenate([y_labeled, pseudo_y])

    final_model = train_model(X_combined, y_combined)
    final_accuracy = accuracy_score(y_test, final_model.predict(X_test))

    print("Semi-Supervised Learning Results")
    print("---------------------------------")
    print(f"Labeled training samples: {len(X_labeled)}")
    print(f"Unlabeled samples: {len(X_unlabeled)}")
    print(f"Pseudo-labels generated: {len(selected)}")
    print("Confidence threshold: 0.80")
    print(f"Initial model accuracy: {initial_accuracy:.2%}")
    print(f"Final model accuracy:   {final_accuracy:.2%}")
    print(f"Accuracy improvement:   {(final_accuracy-initial_accuracy):.2%}")

if __name__ == "__main__":
    main()
