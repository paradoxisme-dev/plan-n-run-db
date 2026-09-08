default_types = {
    "all": {
        "project": [
            {
                "name": "Chaîne Youtube",
                "description": "Une chaîne Youtube."
            },
            {
                "name": "Vlog",
                "description": "Un vlog personnel."
            },
            {
                "name": "Podcast",
                "description": "Un projet de podcast."
            },
            {
                "name": "Court-métrage",
                "description": "Un projet de court-métrage."
            },
            {
                "name": "Série",
                "description": "Un projet de série."
            },
            {
                "name": "Live",
                "description": "Un projet de live."
            },
            {
                "name": "Format de vidéo",
                "description": "Un format de vidéo."
            },  
            {
                "name": "Série de vidéos",
                "description": "Un projet de série de vidéos divers."
            },
            {
                "name": "Vidéo",
                "description": "Un projet de vidéo divers."
            }
        ],
        "ressource": [
            {
                "name": "URL",
                "description": "Une ressource de type URL."
            },
            {
                "name": "Fichier",
                "description": "Une ressource de type fichier."
            },
            {
                "name": "Script",
                "description": "Une ressource de type script."
            },
            {
                "name": "Autre",
                "description": "Une ressource de type autre."
            }
        ]
    }
}


if __name__ == "__main__":
    import json
    for key, value in default_types.items():
        print(f"Generating default types for: {key}")
        with open(f"default_types/{key}.json", "w") as f:
            json.dump(value, f, indent=4)
