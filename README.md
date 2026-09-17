# Transactions Fraud Detection API (MLOps Project)

Ce projet consiste en la mise en place d'une chaîne complète de **MLOps** pour la détection de transactions frauduleuses. Il couvre tout le cycle de vie, du développement d'une API de prédiction jusqu'au déploiement orchestré sur un cluster Kubernetes, avec une automatisation totale via un pipeline CI/CD.

## Fonctionnalités
- **API REST** : Développée avec FastAPI pour servir des prédictions en temps réel.
- **Modèle ML** : Pipeline de détection de fraude avec prétraitement personnalisé (Custom Encoders).
- **Conteneurisation** : Image Docker optimisée pour le déploiement.
- **Orchestration** : Déploiement sur Kubernetes (Minikube) avec gestion des réplicas et des services.
- **CI/CD** : Automatisation complète via GitHub Actions (Tests -> Build -> Push).

---
## Structure du Projet
```text
Transactions_Fraud_Detection/
├── app/
│   ├── app.py                # API FastAPI et logique de prédiction
│   ├── preprocessing.py       # Classes de prétraitement du modèle
│   ├── requirements.txt        # Dépendances Python pour l'image docker
│   └── model_ensemble.joblib  # Pipeline de modèle entraîné + preprocessing
├── tests/
│   └── test_main.py           # Tests unitaires et d'intégration (Pytest)
├── k8s/
│   ├── deployment.yaml        # Configuration des Pods et du Service
│   └── configmap.yaml         # Paramètres métier (seuil de fraude)
├── models/
│   └── model_ensemble.joblib       # Pipeline de modèle entraîné + preprocessing
├── src/                        #entrainement du modèle
├── .github/workflows/
│   └── ci.yml               # Pipeline CI (GitHub Actions)
├── Dockerfile                 # Conteneurisation de l'application
├── requirements.txt           # Dépendances Python pour tout le projet (ML, DataViz, MLops)
└── README.md
```  

## Installation et Utilisation

### 1. Lancer l'API localement :
Après avoir cloner le repo, pour tester l'API sur votre machine locale :

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'API
uvicorn app.app:app --reload
```
L'API est accessible sur http://127.0.0.1:8000 (L'accès au Swagger UI se fait via : http://127.0.0.1:8000/docs)

### 2. Tests Automatisés :
Les tests sont lancés localement ou automatiquement via le CI :
```bash
python -m pytest
```

## Exemple de Test (Requête API)
Pour tester l'endpoint /predict, envoyez un corps (JSON) de la forme suivante via Swagger :

```JSON
{
  "trans_date_trans_time": "2019-10-16 15:20:24",
  "cc_num": 373905417449658,
  "merchant": "fraud_Botsford and Sons",
  "category": "home",
  "amt": 9.65,
  "first": "Sarah",
  "last": "Bishop",
  "gender": "F",
  "street": "554 Mcdonald Valley Apt. 539",
  "city": "Meridian",
  "state": "TX",
  "zip": 76665,
  "lat": 31.929,
  "long": -97.6443,
  "city_pop": 2526,
  "job": "Phytotherapist",
  "dob": "1970-11-12",
  "trans_num": "fbbc30a7dae635613ae0122fb1215a0a",
  "unix_time": 1350400824,
  "merch_lat": 31.891614,
  "merch_long": -98.522877
}
````

## Docker & CI/CD
Le projet utilise GitHub Actions pour automatiser le cycle de mise à jour.

**Continuous Integration :** À chaque push ou pull_request, les tests unitaires sont lancés.

**Continuous Deployment :** Si les tests passent, une image Docker est buildée et poussée sur Docker Hub avec les tags latest et github.sha.

Image Docker Hub : soufianeeloulji/fraud_detection

## Déploiement Kubernetes (Minikube)

### 1. Démarrer le cluster :
```bash
minikube start
```

### 2. Déployer l'application :
```bash
kubectl apply -f k8s/
```

### 3. Accéder à l'API :

```bash
minikube service fraud-detection-api-service --url
```

### 4. Mise à jour (Rolling Update) : Grâce à la configuration imagePullPolicy: Always, pour déployer une nouvelle version après un push Docker Hub :
```bash
kubectl rollout restart deployment fraud-detection-api-deployment
```
### 5. Configuration via ConfigMap
Le seuil de détection (FRAUD_THRESHOLD) est géré de manière externe. Pour le modifier sans changer le code :

Modifier k8s/configmap.yaml.

Appliquer les changements :

```bash
kubectl apply -f k8s/configmap.yaml
kubectl rollout restart deployment fraud-detection-api-deployment
```


