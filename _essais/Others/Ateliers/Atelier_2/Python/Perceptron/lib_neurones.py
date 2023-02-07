import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score
# barre de progression
from tqdm import tqdm

# fonctions du modele
# initialisation des paramètres W et b
def initialisation(X):
    W = np.random.randn(X.shape[1], 1)
    # W = vecteur de même taille de X (ici 2 - coordonnées x,y des points)
    b = np.random.randn(1)
    return (W, b)

# modele - fonction sigmoide
def model(X, W, b):
    # modele matriciel
    Z = X.dot(W) + b
    # activation
    A = 1 / (1 + np.exp(-Z))
    return A

# fonction de cout / Log Loss
# quantifier les erreurs commises par le modèle
def log_loss(A, y):
    # Attention probleme d'overflow de la fonction exp du modèle qui entraine des A valant 0 ou 1.
    # Or dans la fonction log_loss, log(0) est non défini !!
    # on insère un epsilon faible volontairement
    epsilon = 1e-15
    return 1 / len(y) * np.sum(-y * np.log(A + epsilon) - (1 - y) * np.log(1 - A + epsilon))

# gradient
def gradients(A, X, y):
    dW = 1 / len(y) * np.dot(X.T, A - y)
    db = 1 / len(y) * np.sum(A - y)
    return (dW, db)

def update(dW, db, W, b, learning_rate):
    W = W - learning_rate * dW
    b = b - learning_rate * db
    return (W, b)

# Prediction d'un ensemble de données vis-à-vis du modèle - Fonction sigmoide
def predict(X, W, b):
    A = model(X, W, b)
    # print(A)    # probabilite d'etre dans la classe
    return A >= 0.5


# Definition du neuronne artificiel
def artificial_neuron(X, y, learning_rate = 0.1, n_iter = 100, pas_iter = 10):
    # initialisation W, b
    W, b = initialisation(X)
    # Evolution du cout / taux d'erreur de l'apprentissage
    Loss = []
    # Evolution du taux d'erreur
    acc = []
    # Evolution W
    Wfinal = []

    # boucle d'apprentissage
    for i in tqdm(range(n_iter)):
        # activations
        A = model(X, W, b)
        if i % pas_iter == 0:
            # Calcul cout
            Loss.append(log_loss(A, y))
            # Calcul taux d'erreur
            y_pred = predict(X, W, b)
            acc.append(accuracy_score(y, y_pred))
        # Calcul des gradients
        dW, db = gradients(A, X, y)
        # Mise à jour
        W, b = update(dW, db, W, b, learning_rate)
        Wfinal.append(W[0])

    y_pred = predict(X, W, b)
    # Comparaison donnees réelles y et données prédites par le modèle
    print(accuracy_score(y, y_pred))

    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(Loss)
    plt.subplot(1,2,2)
    plt.plot(acc)
    plt.show()

    return (W, b, Wfinal)   # retourne les paramètres du modèle

# Definition du neuronne artificiel
def artificial_neuron_test(X_train, y_train, X_test, y_test, learning_rate = 0.1, n_iter = 100, pas_iter = 10):
    # initialisation W, b
    W, b = initialisation(X_train)
    # Evolution du cout / taux d'erreur de l'apprentissage
    Loss_train = []
    Loss_test = []
    # Evolution du taux d'erreur
    acc_train = []
    acc_test = []
    # Evolution W
    Wfinal = []

    # boucle d'apprentissage
    for i in tqdm(range(n_iter)):
        # activations
        A = model(X_train, W, b)
        if i % pas_iter == 0:
            # Train data
            # Calcul cout
            Loss_train.append(log_loss(A, y_train))
            # Calcul taux d'erreur
            y_pred = predict(X_train, W, b)
            acc_train.append(accuracy_score(y_train, y_pred))

            # Test data - pour vérifier l'efficacité du modèle
            A_test = model(X_test, W, b)
            # Calcul cout
            Loss_test.append(log_loss(A_test, y_test))
            # Calcul taux d'erreur
            y_pred = predict(X_test, W, b)
            acc_test.append(accuracy_score(y_test, y_pred))

        # Calcul des gradients
        dW, db = gradients(A, X_train, y_train)
        # Mise à jour
        W, b = update(dW, db, W, b, learning_rate)
        Wfinal.append(W[0])

    y_pred = predict(X_train, W, b)
    # Comparaison donnees réelles y et données prédites par le modèle
    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(Loss_train, label='train loss')
    plt.plot(Loss_test, label='test loss')
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(acc_train, label='train acc')
    plt.plot(acc_test, label='test acc')
    plt.legend()
    plt.show()

    return (W, b, Wfinal)   # retourne les paramètres du modèle