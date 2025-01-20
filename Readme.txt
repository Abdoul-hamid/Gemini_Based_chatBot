Ce réalisation s'inscrit dans le cadre d'un mini-projet TAL connu sur l'appélation NLP.

Suivez ces Instructions pour créer un environnement virtuel et installer les dépendances necéssaires.

1-Instructions pour créer et activer un environnement virtuel Python

    a-Créer l'environnement virtuel : Exécutez la commande suivante pour créer un nouvel environnement virtuel.
    Remplacez mon_environnement par le nom que vous souhaitez donner à votre environnement :

        Sur Windows :
        python -m venv chatbot_env



    b-Activer l'environnement virtuel :

        Sur Windows :
        chatbot_env\Scripts\activate



    c-désactiver l'environnement virtuel.
       
        Sur Windows:
        deactivate



2-Instructions pour utiliser ce fichier requirements.txt :
Après avoir activé l'environnement virtuel(mon_environnement), installez les dépendances avec la commande suivante :

    Sur Windows :
    pip install -r requirements.txt


3-Instructions pour lancer l'application streamlit

    streamlit run app.py