from elasticsearch import Elasticsearch


class MealSearcher:
    def __init__(self):
        self.es = Elasticsearch(["http://localhost:9200"])

    def search_recipe(self, category):
        print(category)
        query_body = {
            "query": {
                "term": {
                    "category": {
                        "value": category.lower()
                    }
                }
            }
        }
        # Assuming the Elasticsearch index is called 'recipes'
        response = self.es.search(index='recipes', body=query_body)
        if response['hits']['hits']:
            # Assuming the recipe name is stored in a field named 'recipe_name'
            recipe_name = response['hits']['hits'][0]['_source']['recipe']
            return recipe_name
        else:
            return "Recipe Not Found"

    def get_meal_plan(self, template):
        meal_plan = []
        for record in template:
            recipe_name = self.search_recipe(record['category'])
            meal_plan.append({
                'day': record['day'],
                'moment_of_day': record['moment_of_day'],
                'recipe_name': recipe_name
            })
        return meal_plan
