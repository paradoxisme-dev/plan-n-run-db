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
        ],
        "project_status": [
            {
                "name": "En cours",
                "description": "Le projet est en cours."
            },
            {
                "name": "Terminé",
                "description": "Le projet est terminé."
            },
            {
                "name": "En attente",
                "description": "Le projet est en attente."
            }
        ]
    },
    "youtube": {
        "project": [
            {
                "name": "Chaîne Youtube",
                "description": "Une chaîne Youtube."
            },
            {
                "name": "Vidéo Youtube",
                "description": "Un projet de vidéo Youtube."
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
            }
        ],
        "project_status": [
            {
                "name": "Planification",
                "description": "Le projet est en phase de planification."
            },
            {
                "name": "Écriture",
                "description": "Le projet est en phase d'écriture."
            },
            {
                "name": "Tournage",
                "description": "Le projet est en phase de tournage."
            },
            {
                "name": "Montage",
                "description": "Le projet est en phase de montage."
            },
            {
                "name": "En ligne",
                "description": "Le projet est en ligne."
            },
        ]
    }
}


if __name__ == "__main__":
    import json
    for key, value in default_types.items():
        print(f"Generating default types for: {key}")
        with open(f"default_types/{key}.json", "w") as f:
            json.dump(value, f, indent=4)
