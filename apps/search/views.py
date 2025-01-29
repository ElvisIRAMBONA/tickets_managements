from django.shortcuts import render
from apps.events.documents import EventDocument
from elasticsearch_dsl import Q

def search_event(request):
    """
    View to render the search page with results from Elasticsearch.
    This function handles both full search results and autocompletion when the query is short.
    """
    query = request.GET.get("q", "")  # Récupérer la requête, ou une chaîne vide par défaut
    print("Query:", query)  # Afficher la requête pour débogage
    query = Q("match", name={"query": query, "fuzziness": "AUTO"})
    events = []
    suggestions = []
    error_message = None

    if query:
        try:
            if len(query) >= 2:  # Si la longueur de la requête est >= 2, utiliser l'autocomplétion
                # Requête wildcard pour trouver des titres contenant la requête
                search = EventDocument.search().query(Q("wildcard", title={"value": f"*{query}*"}))
                results = search[:10].execute()  # Limiter à 10 résultats pour de meilleures performances
                print("Results from wildcard search:", results)  # Afficher les résultats pour débogage

                suggestions = [
                    {
                        "id": hit.id,
                        "title": hit.title,
                        "description": hit.description,
                    }
                    for hit in results
                ]
            else:  # Si la requête est trop courte, utiliser une recherche complète
                search = EventDocument.search().query(Q("match", title=query))
                results = search[:10].execute()  # Limiter à 10 résultats
                print("Results from match search:", results)  # Afficher les résultats pour débogage

                events = [hit.to_dict() for hit in results]

        except Exception as e:
            error_message = f"Error during search: {e}"
            print(f"Error during search: {e}")

    return render(request, "search.html", {
        "events": events,
        "error_message": error_message,
        "suggestions": suggestions
    })
