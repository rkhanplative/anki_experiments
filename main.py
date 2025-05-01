import yaml
import genanki
import random

# Load the YAML file
with open('anki_deck.yaml', 'r') as file:
    deck_data = yaml.safe_load(file)

with open('note_models.yaml', 'r') as file:
    note_models = yaml.safe_load(file)['note_models']

# Create a unique deck ID
deck_id = random.randrange(1 << 30, 1 << 31)

# Create the deck
deck = genanki.Deck(deck_id, deck_data['deck_name'])

# Create note models
models = {}
for model_data in note_models:
    model = genanki.Model(
        random.randrange(1 << 30, 1 << 31),
        model_data['name'],
        fields=[{'name': field['name']} for field in model_data['fields']],
        templates=[{
            'name': template['name'],
            'qfmt': template['qfmt'],
            'afmt': template['afmt']
        } for template in model_data['templates']]
    )
    models[model_data['name']] = model

# Add cards to the deck
for card_data in deck_data['cards']:
    model = models[card_data['model']]
    
    # Check if all necessary fields exist
    try:
        note_fields = [card_data['fields'][field['name']] for field in model.fields]
    except KeyError as e:
        print(f"Error: Missing field {e} in card data. Please check your YAML file for completeness.")
        continue  # Skip this card if there are missing fields
    
    note = genanki.Note(
        model=model,
        fields=note_fields
    )
    deck.add_note(note)

# Create and save the Anki package
package = genanki.Package(deck)
package.write_to_file(f'{deck_data["deck_name"].replace(" ","_")}.apkg')
print(f"Anki package '{deck_data['deck_name']}' created successfully.")
