

import json, requests

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
            # 'Content-Type':'application/x-www-form-urlencoded',
            "Connection": "keep-alive" }


if __name__ == '__main__':

    urlActionPAB = "https://pab.donneesquebec.ca/recherche/api/3/action/" 

    packIdToUpdate = '11bdaa6e-33ce-447b-8e6c-1a804048f03b'
    urlPackPatch = urlActionPAB+'package_patch'

    packDict = {
        'id' : packIdToUpdate,
        'notes': 'description modif'  # josee-test-update
    }
    response = requests.post(urlPackPatch, data=packDict,
                              headers=postHeader)
    
    reponseLoad = json.loads(response.content)
    dictPackAUpdate = reponseLoad['result']
    
    if response.status_code == 200:
        print('Ressource créée avec succès.')
    else:
        print('Erreur  :', response.text)
    
    print('fin')
