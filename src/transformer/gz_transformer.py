import json
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"

INGREDIENTS_CATEGORY = """
      Altri ingredienti
      Bevande
      Burri, salse e olii
      Carni
      Dolcificanti
      Erbe, spezie, aromi
      Formaggi
      Frutta
      Pesci
      Uova
      Verdure
    """

EXAMPLES = """
      Example:
      Input user: Olio extra vergine d'oliva, fettine di tacchino
      Response: [{"name": "Olio extra vergine d'oliva", "category": "Burri, salse e olii"}, {"name": "fettine di tacchino", "category": "Carni"}
    """

PROMPT_CLASSIFIER = f"""
      You are an ingredients italian expert designed to output JSON. You must classify the provided ingredients in one of these category:
    {INGREDIENTS_CATEGORY}
    {EXAMPLES}
    """


def classify_ingredients(string_ingredients: str):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": PROMPT_CLASSIFIER},
            {"role": "user", "content": string_ingredients}
        ],
        response_format={"type": "json_object"}
    )

    prova = json.loads(completion.choices[0].message.content)
    for _ in prova['ingredients']:
        print(_)
