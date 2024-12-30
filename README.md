# WhereIsMyDad

L'application **WhereIsMyDad** va permettre à n'importe qui de retrouver ses deux parents, à condition qu'ils émettent leurs coordonnées gps. Suivez simplement ces étapes pour installer l'application sur votre machine:

## Installation

1. **Cloner le repository :**

   Exécutez la commande suivante dans le répertoire de votre choix sur les 3 VMs:

   ```bash
   git clone https://github.com/RaphaelDP/WhereIsMyDad.git
   ```

2. **Ajouter les fichiers .env pour chaque VM :**

   Pour spécifier l'adresse IP du broker, ajoutez un fichier .env à la racine de chacun des dossiers *vmx*. Dans le fichier .env initialisez la variable **IP_BROKER** comme suit:

   ```bash
   IP_BROKER = VOTRE_IPV4
   ```

3. **Lancer l'application :**
    
   * L'application web et le consumer sont accessibles dans le dossier *vm1*. Pour procéder à l'installation sur la VM1, exécutez la commande suivante : 

   ```bash
   cd vm1/ && docker compose up --build
   ```

   * Le producer1 est accessible dans le dossier *vm2*. Pour procéder à l'installation sur la VM2, exécutez la commande suivante : 

   ```bash
   cd vm2/ && docker build -t producer1 . && docker run producer1
   ```

   * Le producer2 est accessible dans le dossier *vm3*. Pour procéder à l'installation sur la VM3, exécutez la commande suivante : 

   ```bash
   cd vm3/ && docker build -t producer2 . && docker run producer2
   ```

    **Remarque :** Si vous souhaitez relancer l'application après l'avoir build, stoppez et supprimez bien tous les dockers liés à l'application. Vous pourrez ensuite relancer les dockers sans avoir à build à nouveau.

## Utilisation

1. **Accéder à l'application :** 

    Ouvrez votre navigateur et allez sur l'adresse [`http://localhost:8080`](http://localhost:8080) pour retrouver vos parents.

2. **Fonctionnalités de l'application :**

   Pour lancer la recherche, cliquez sur le bouton *Commencer la traque* une fois qu'il est apparu. Si tout se passe bien, vous verrez vos deux papas se déplacer. Des boutons vous permettront d'afficher/cacher leur déplacement ou de faire un focus sur eux. 

3. **Accéder aux données générées par les papas :**

   Ouvrez un terminal à partir de la VM1, et exécutez cette commande :

   ```bash
   docker exec -it postgres psql -U postgres -d daddy_db
   ```

   Vous êtes à présent dans la console postgres, et connecté à la base de données. Vous pouvez maintenant exécutez la commande suivante pour afficher les 10 premières données :

   ```bash
   select * from gps_messages limit 10;
   ```

**Remarque :** Pour des questions de logistique, vos deux papas se trouveront toujours en plein centre de Pau au lancement de l'application, et bougeront aléatoirement ensuite.

Nous vous souhaitons une bonne traque ! 