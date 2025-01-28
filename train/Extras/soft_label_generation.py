import json
import re

# def clean_and_decode_token(token):
#     """
#     Nettoie et décode les tokens pour éviter les problèmes d'encodage
#     (par exemple les caractères mal interprétés comme 'ĠMamÃ©').
#     """
#     # Enlever le caractère 'Ġ' au début du token
#     cleaned_token = token.replace("Ġ", "")

#     # Tenter de décoder les séquences Unicode mal encodées
#     try:
#         cleaned_token = bytes(cleaned_token, 'utf-8').decode('utf-8')
#     except UnicodeDecodeError:
#         # Si une erreur se produit, tenter de récupérer une version lisible
#         cleaned_token = cleaned_token.encode('utf-8', 'ignore').decode('utf-8', 'ignore')

#     return cleaned_token

def merge_token(token_list):
    merged_tokens = []
    current_token = ""

    for token in token_list:
        if token == "<|endoftext|>":  # Ignorer explicitement le token de fin de texte
            continue
        if token == "<\/s>":  # Ignorer explicitement le token de fin de texte
            continue
        if token == "</s>":  # Ignorer explicitement le token de fin de texte
            continue

        if token == ".":  # Ignorer le point isolé
            if current_token:  # Ajouter le token actuel sans le point
                merged_tokens.append(current_token)
            current_token = ""
            continue

        if not token.startswith("\u0120"):  # Pas d'espace au début du token => le fusionner
            current_token += token
        else:  # Le token commence par un espace => commencer un nouveau mot
            if current_token:  # Ajouter le token actuel déjà construit
                merged_tokens.append(current_token)
            current_token = token  # Démarrer un nouveau mot

    # Ajouter le dernier token traité s'il est valide
    if current_token and current_token != ".":  
        merged_tokens.append(current_token)

    return merged_tokens

# def compare_and_exclude_the_token_present_in_model_input(model_input, token_list):
#     filtered_tokens = [token for token in token_list if token.strip() not in model_input]
#     return filtered_tokens
def compare_and_exclude_the_token_present_in_model_input(model_input, token_list):
    filtered_tokens = []
    model_input_clean = model_input.lower()  # Convertir en minuscule pour comparaison insensible à la casse

    for token in token_list:
        cleaned_token = token.replace("Ġ", "").lower()  # Retirer le préfixe 'Ġ' et convertir en minuscule

        # Vérifier si le token nettoyé n'est pas dans la model_input
        if cleaned_token not in model_input_clean.split():
            filtered_tokens.append(token)  # Ajouter le token original s'il n'est pas présent

    return filtered_tokens



def create_span_from_token(token_list, model_output_text):
    spans = []
    current_position = 0  # Position actuelle dans la chaîne model_output_text

    for token in token_list:
        # Nettoyer le token pour supprimer les préfixes spéciaux comme Ġ ou Ċ
        cleaned_token = token.replace("Ġ", " ").replace("Ċ", "\n").strip()
        #cleaned_token = clean_and_decode_token(cleaned_token2)
        # Utiliser une regex pour localiser précisément le token dans model_output_text
        match = re.search(re.escape(cleaned_token), model_output_text[current_position:], re.IGNORECASE)
        if not match:
            raise ValueError(f"Token '{token}' introuvable dans le texte à partir de la position {current_position}.")

        # Calculer les positions exactes de début et de fin
        token_start = current_position + match.start()
        token_end = current_position + match.end()
        
        spans.append({"start": token_start, "prob": 0, "end": token_end})

        # Mettre à jour la position courante pour éviter les recherches répétées
        current_position = token_end

    return spans



def convert_to_utf8(input_string):
    # Convertir la chaîne en bytes en utilisant l'encodage UTF-8
    utf8_bytes = input_string.encode('utf-8')
    return utf8_bytes


def determinate_probability(soft_labels, token_list, reference_response):
    for i, token in enumerate(token_list):
        # clean_token = clean_and_decode_token(token)
        # print(token, clean_token)
        clean_token = token.replace("Ġ", " ").replace("Ċ", "\n").strip()
        if clean_token in reference_response:
            soft_labels[i]['prob'] = 0
        else:
            soft_labels[i]['prob'] = 1
    return soft_labels

import json

def main(input_file_path, reference_file_path):
    soft_labels_list = []

    # Ouvrir le fichier d'entrée JSONL et le fichier de référence JSON
    with open(input_file_path, 'r') as input_file, open(reference_file_path, 'r') as ref_file:
        # Lire toutes les lignes du fichier d'entrée JSONL
        input_lines = input_file.readlines()
        
        # Charger le fichier de référence JSON en une seule fois
        reference_data = json.load(ref_file)

        # Vérifier que les deux fichiers contiennent le même nombre d'éléments
        if len(input_lines) != len(reference_data):
            raise ValueError("Les fichiers d'entrée et de référence doivent avoir le même nombre d'éléments.")

        # Parcourir les lignes des deux fichiers simultanément
        for input_line, reference_item in zip(input_lines, reference_data):
            item = json.loads(input_line.strip())  # Ligne du fichier JSONL
            reference_response = reference_item['ref']  # Attribut 'ref' comme référence

            # Extraire les données nécessaires
            model_input = item['model_input']
            model_output_tokens = item['model_output_tokens']
            model_output_text = item["model_output_text"]

            # Étape 1: Fusionner les tokens
            merged_tokens = merge_token(model_output_tokens)
            print("========================= Merge token =============================")
            print(merged_tokens)
            print("===================================================================")

            # Étape 2: Filtrer les tokens présents dans model_input
            filtered_tokens = compare_and_exclude_the_token_present_in_model_input(model_input, merged_tokens)
            print("========================= filtered_tokens =============================")
            print(filtered_tokens)
            print("===================================================================")


            # Étape 3: Créer les spans
            soft_labels = create_span_from_token(filtered_tokens, model_output_text)
            print("========================= fsoft_labels =============================")
            print(soft_labels)
            print("===================================================================")


            # Étape 4: Déterminer les probabilités
            final_soft_labels = determinate_probability(soft_labels, filtered_tokens, reference_response)
            soft_labels_list.append(final_soft_labels)

            # Afficher le résultat
            print(f"ID: {item['id']}")
            print(f"Soft Labels: {final_soft_labels}\n")
        print(soft_labels_list)
        return soft_labels_list


reference_response_file_path = "/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/reference_response-en.json"
file_path = "/home/chinjoyce/Downloads/MUSHROOM-task3/test-unlabeled/v1/converted_test_en.jsonl"  # Remplacez avec votre fichier
soft_labels_list = main(file_path, reference_response_file_path)






# Exemple d'utilisation
if __name__ == "__main__":
    output_jsonl_file = "/home/chinjoyce/Downloads/MUSHROOM-task3/test-unlabeled/Results.jsonl"
    process_json_and_update_jsonl( output_jsonl_file, soft_labels_list)
    print("Submission ready!!!")
