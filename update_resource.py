
import requests, json

####
# Retrouver les informations de votre jeton
# ** Ne jamais mettre votre jeton sur un espace partagé ou nuage comme un dépot GIT

# à adapter selon la facon que vous stockez votre jeton
from JETONSJOSEE_editeur import JETONSJOSEEEDITEUR
### JETONSJOSEEEDITEUR = {
###    "PAB" : "xxxxyyzzzz"}

jetonPAB = JETONSJOSEEEDITEUR['PAB'] # environnement PAB
postHeader = {
            "Authorization": jetonPAB,
            # 'Content-Type':'application/x-www-form-urlencoded',
            "Connection": "keep-alive" }

if __name__ == '__main__':

    urlActionPAB = "https://pab.donneesquebec.ca/recherche/api/3/action/" 
    urlresourcePatch = urlActionPAB+'resource_patch'

    # charger le CSV a ajouter et/ou modifier 
    fileRessource = "C:/Users/marjo31/local_job/test.csv"
    fichier_a_envoyer = {
        'upload': open(fileRessource, 'rb'),
        }

    resourceIdToUpdate = '6ca279eb-3147-4a35-8a9e-e9f6fa4ac937' # retrouver votre id de ressource a modif
    # mettre les attributs a modifier
    resourceDictToModif = {
        'id' : resourceIdToUpdate,
        'description': 'description modifiée test',
    }
    
    response = requests.post(urlresourcePatch, data=resourceDictToModif,
                              files= fichier_a_envoyer,
                              headers=postHeader)
    
    if response.status_code == 200:
        print('Ressource MAJ avec succès.')
    else:
        print('Erreur lors de la modification de la ressource :', response.text)
        raise Exception(response.text)
    

    # Consulter la donnée du fichier CSV que nous venons de charger
    urlRequeteDatastoreSearch = urlActionPAB+"datastore_search?resource_id={}".format(resourceIdToUpdate)
    response = requests.get(urlRequeteDatastoreSearch,
                              headers=postHeader)
    json_data = json.loads(response.text)
    if response.status_code != 200:
        print('Erreur  :', response.text)
        raise Exception(response.text)

    reccords = json_data['result']['records']
    for unRec in reccords:
        print (unRec)
    print('fin')