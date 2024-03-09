
## Josée Martel 2024-02
## formation  HackQC24

import json, urllib, requests

####
# Retrouver les informations de votre jeton
# ** Ne jamais mettre votre jeton sur un espace partagé ou nuage comme un dépot GIT

from JETONSJOSEE_editeur import JETONSJOSEEEDITEUR
### JETONSJOSEEEDITEUR = {
###    "PROD":"xxxxxxx",
###    "BETA" : "xxxxyyyy",
###    "PAB" : "xxxxyyzzzz"}

jetonPAB = JETONSJOSEEEDITEUR['PAB'] # environnement PAB
postHeader = {
            "Authorization": jetonPAB,
            'Content-Type':'application/x-www-form-urlencoded',
            "Connection": "keep-alive" }


def postRequest(url, dictMaj, headers=postHeader):
    """   Fonction générique pour lancer des requêtes POST de MAJ ou création 
            des packages et ressources
    """
    try:
        dictMajFormat = urllib.parse.quote(json.dumps(dictMaj))
        # response = requests.post(url, data=dictMajFormat, headers=headers, verify=False)
        response = requests.post(url, data=dictMajFormat, headers=headers)

    except Exception as e:
        print('oh probleme dans la requete POST', e)
        raise e

    if response.status_code != 200:
        
        responseDict = json.loads(response.text) 
        try: 
            messErreurReponse = responseDict['error']['name']
        except:
            try:
                messErreurReponse = responseDict['error']['message']
            except:
                messErreurReponse = response.text

        if response.status_code == 403:
            messErreurRecu = "{0} - {1} : Problème accès! L'utilisateur à les accès en édition?. Le vpn est branché? \n{2}".format(response.reason, response.status_code, messErreurReponse)
            raise Exception("Erreurs de validation: \n {}".format(messErreurRecu))
        elif response.status_code == 404:
            messErreurRecu = "{0} - {1} : Introuvable, vérifier le ID \n{2}".format(response.reason, response.status_code, messErreurReponse)
            raise Exception("Erreurs de validation: \n {}".format(messErreurRecu))
        elif response.status_code == 409:
            messErreurRecu = '{0} - {1} \n {2}'.format(response.reason, response.status_code, messErreurReponse)
            raise Exception("Erreurs de validation: \n {}".format(messErreurRecu))
        
        print('** Probleme avec la requete, cette requete est inexacte:\n {}'.format(url))
        raise Exception('Probleme avec la requete, cette requete est incorrecte:\n {0} \n Erreur : {1} '.format(url, messErreurReponse))


def MAJ_deletePackage(idPackToDelete, purge=False):
    """ Fonction générique qui supprime un package
    *  purge = remove completement ** attention cannot by undone **

    """
    # pour delete un pack on fait un dict avec le id et on le passe à la requete de delete
    dictId = {'id': idPackToDelete} 
    urlDelete = "https://pab.donneesquebec.ca/recherche/api/3/action/package_delete"

    postRequest(url=urlDelete, dictMaj=dictId)
    
    if purge:
        urlPurge = "https://pab.donneesquebec.ca/recherche/api/3/action/dataset_purge"
        postRequest(url=urlPurge, dictMaj=dictId)

    print('package {} a été supprimé'.format(idPackToDelete))


if __name__ == '__main__':

# attention a l'environnement utilisé, production pour aller chercher des données
# et la PAB pour la création et l'édition de données bien indiquer si vous êtes en prod ou en édition dans PAB
    
    ########################
    # pour les tests comme on relancera la creation de la meme ressource 
    # on debute par la supprimer sinon nous aurons une erreur car on ne peut creer la meme ressource 2 fois
    try: 
        MAJ_deletePackage('josee-test-creation') #*** a enlever
        import time
        time.sleep(2) # laisser le temps a api de delete avant de recreer 
    except:
        pass
    #########################
    

    ################
    # Creer un package - jeu de données
    #########################
    
    urlActionPAB = "https://pab.donneesquebec.ca/api/3/action/" 
    # urlActionPAB = "https://pab.donneesquebec.ca/recherche/api/3/action/" 
    urlCreationPack = urlActionPAB+"package_create"
    
    dictPackageACreer = {
            # attributs obligatoires pour les packs
            'title': 'josee test creation', # identifier vos tests ou jeu a votre nom
            'notes': 'A long description of my dataset',
            'update_frequency': 'hourly',
            'ext_spatial': 'cm-montreal',
            'owner_org': 'a494684c-3adb-45d9-ae7d-ef6908c98c6a', # hackqc24, requete ...3/action/organization_show?id=hackqc24
            'extras_organisation_principale': "gouvernement-du-quebec",
            'language': 'FR',
            'update_frequency': 'asNeeded',
            'license_id': 'cc-by',
            'type': 'dataset',
            'private': False,
            'state': 'active',
            'name': 'josee-test-creation', # attention avec la nomenclature de cet attribut, ce sera id-url pour acces API donc respecter les obligations acces url 
                                    ## -> pas accent, carac spéciaux, pas espaces, on separe avec des tirets, doit réfléter le titre
        }

    postRequest(urlCreationPack, dictPackageACreer)

    #################
    # Creer une ressource à l'intérieur du package josee-test-creation
    #################

    dictResourceACreer = {

        'package_id': 'josee-test-creation',
        'name' : 'resssource_cree_api', 
        'description' : 'Fichier CSV contenant xyz',
        'taille_entier': 6, 
        'format':'CSV',
        'resource_type': 'donnees',  
        'relidi_condon_valinc':'oui', 
        'relidi_condon_nombre':'n/a',
        'relidi_condon_boolee':'oui',
        'relidi_condon_datheu':'oui',
        'relidi_confic_utf8':'oui', 
        'relidi_confic_separateur_virgule':'oui',
        'relidi_confic_pascom':'n/a',
        'relidi_confic_epsg':'n/a', 
        'url_type': 'upload',
        'mimetype': 'text/csv',
        'mimetype_inner': None,
        }

    urlCreationResource = urlActionPAB+"resource_create"

    response = requests.post(urlCreationResource, 
                            data=dictResourceACreer, 
                            headers=postHeader)
                            # files= fichier_a_envoyer)

    if response.status_code == 200:
        print('Ressource créée avec succès.')
    else:
        print('Erreur lors de la création de la ressource :', response.text)


    print('Terminé 🍾🍾🍾🍾🍾🍾')


