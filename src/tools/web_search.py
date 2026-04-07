import urllib.request
import urllib.parse
import json

def search_documentation(query: str, limit: int = 2) -> str:
    """
    Permet à l'IA de faire des recherches basiques pour s'informer sur un concept technique.
    Utilise l'API Wikipedia en Open Source pour contourner les quotas des moteurs de recherche privés.
    """
    try:
        # Formatage de l'URL pour l'API Wikipedia
        encoded_query = urllib.parse.quote(query)
        url = f"https://fr.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&utf8=&format=json&srlimit={limit}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'WorkAI-Agent/1.0'})
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        search_results = data.get('query', {}).get('search', [])
        
        if not search_results:
            return f"Aucune documentation trouvée pour : {query}"
            
        formatted_results = []
        for item in search_results:
            title = item.get('title', '')
            # Nettoyage basique des balises HTML renvoyées par l'API
            snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
            formatted_results.append(f"Titre: {title}\nExtrait: {snippet}")
            
        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Erreur lors de la recherche web : {str(e)}"