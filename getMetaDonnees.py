

## Josée Martel 2024-02
## formation  HackQC24

import urllib3, json

http = urllib3.PoolManager()

def getJsonResponseResult(url, methode='GET'):
    # fonction générique pour des get à l'API CKAN-Données Québec
    response = ""
    try:
        methode == 'GET'
        response = http.request('GET', url)
        reponseLoad = json.loads(response.data) # transforme la reponse en dictionnaire Python (json) 
        if response.status != 200:
            print('** Probleme avec la requete, cette requete est inexacte:\n {}'.format(url))
            raise Exception('Probleme avec la requete, cette requete est incorrecte:\n {}'.format(url))
        
        # Pour les retours des requetes au datastore, la structure est différente
        if reponseLoad['result'] and 'results' in reponseLoad['result']:
            return reponseLoad['result']['results']

        return reponseLoad['result']

    except Exception as e:
        print('oh probleme', e)
        raise


if __name__ == '__main__':

    # attention à l'environnement utilisé, Production pour aller chercher des données
    # et la PAB pour la création et l'édition de données bien indiquer si vous êtes en prod ou en édition dans PAB

    urlActionProd = "https://www.donneesquebec.ca/recherche/api/3/action/" 
    urlActionPAB = "https://pab.donneesquebec.ca/recherche/api/3/action/" 

    # on construit notre requete que nous avons préalablement testée dans le navigateur Web, 
    # vérifier toujours vos requêtes via un navigateur internet pour vous assurez qu'elles fonctionnent
    # on combine la requête action environnement et la requête souhaitée
    
    # PACKAGE_SHOW
    urlRequetePackageShow = urlActionProd+"package_show?id=77338401-0d96-43fc-9f75-2f5807918cb9"
    # on lance la requete à l'aide de notre fonction d'apel
    resultResponsePackageShow  = getJsonResponseResult(url=urlRequetePackageShow)
    
    # RESOURCE_SHOW
    urlRequeteResourceShow = urlActionProd+"resource_show?id=afdbda31-0ada-448e-82fd-d27567c63e93"
    resultResponseResourceShow = getJsonResponseResult(url=urlRequeteResourceShow)

    # PACKAGE_SEARCH
    urlRequetePackageSearch = urlActionProd+"package_search?q=parc&rows=5"
    resultResponsePackageSearch = getJsonResponseResult(url=urlRequetePackageSearch)

    # DATASTORE_SEARCH - enregistrements
    urlRequeteDatastoreSearch = urlActionProd+"datastore_search?resource_id=6fe7c470-2427-4c46-9252-3e39f320eeec"
    resultResponseDatastoreSearch = getJsonResponseResult(url=urlRequeteDatastoreSearch)
   
    # DATASTORE_SEARCH_SQL - enregistrements
    urlRequeteDatastoreSearchSql = urlActionProd+'datastore_search_sql?sql=SELECT "categorie", "titre", "dateDebut" from "6fe7c470-2427-4c46-9252-3e39f320eeec"'
    resultResponseDatastoreSearchSql = getJsonResponseResult(url=urlRequeteDatastoreSearchSql)
  
    # DATASTORE_SEARCH_SQL - enregistrements clause where
    sqlALancer = """SELECT "categorie", "titre", "dateDebut" from "6fe7c470-2427-4c46-9252-3e39f320eeec" where "categorie" = 'Rencontre' and "dateDebut" >'2020-05-17'"""
    
    urlRequeteDatastoreSearchSqlCustom = urlActionProd+'datastore_search_sql?sql={}'.format(sqlALancer)
    resultResponseDatastoreSearchSqlCustom = getJsonResponseResult(url=urlRequeteDatastoreSearchSqlCustom)

    print('Terminé 😎')





