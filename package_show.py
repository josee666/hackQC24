## Josée Martel 2024-02
## formation  HackQC24
import urllib3, json

if __name__ == '__main__':
    http = urllib3.PoolManager()
    # on construit la requête que nous avons préalablement testée dans le navigateur Web, 
    # vérifier toujours vos requêtes via un navigateur internet pour vous assurez qu'elles fonctionnent
    url = "https://www.donneesquebec.ca/recherche/api/3/action/package_show?id=77338401-0d96-43fc-9f75-2f5807918cb9"
    response = http.request('GET', url)
    reponseLoad = json.loads(response.data) # transforme la reponse en dictionnaire Python (json) 
    if response.status != 200:
        print('** Probleme avec la requete, cette requete est inexacte:\n {}'.format(url))
        raise Exception('Probleme avec la requete, cette requete est incorrecte:\n {}'.format(url))

    resultDictPythonPackage = reponseLoad['result']
    listRessourcesContenuDansLePackage = resultDictPythonPackage['resources']
    urlTelechargementFichierRes1 = listRessourcesContenuDansLePackage[0]['url']
    print('Terminé 😎')


