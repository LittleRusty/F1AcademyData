# Utility file containing info about drivers and colors to be used for data display
TEAMS = {
    "Campos Racing": {"color": "#EBC110"},
    "Rodin Motorsport": {"color": "#000000"},
    "Prema Racing": {"color": "#E80309"},
    "MP Motorsport": {"color": "#F7401A"},
    "ART Grand Prix": {"color": "#B4B3B4"},
    "Hitech TGR": {"color": "#2240FD"},
}


DRIVERS = {
    "CHA": {
        "full_name": "Chloe Chambers",
        "team": "Campos Racing",
        "color": "#1D19AC",
        "sponsor": "Red Bull Ford",
        "number": "14",
    },
    "HAV": {
        "full_name": "Nicole Havrda",
        "team": "Hitech TGR",
        "color": "#002663",
        "sponsor": "American Express",
        "number": "2",
    },
    "GAD": {
        "full_name": "Nina Gademan",
        "team": "Prema Racing",
        "color": "#FF87BC",
        "sponsor": "Alpine",
        "number": "3",
    },
    "FEL": {
        "full_name": "Emma Felbermayr",
        "team": "Rodin Motorsport",
        "color": "#52E252",
        "sponsor": "Kick Sauber",
        "number": "5",
    },
    "CRO": {
        "full_name": "Courtney Crone",
        "team": "ART Grand Prix",
        "color": "#B6BABD",
        "sponsor": "HAAS",
        "number": "7",
    },
    "PAA": {
        "full_name": "Mathilda PAATZ (WCD)",
        "team": "Hitech TGR",
        "color": "#F8A350",
        "sponsor": "Gatorade",
        "number": "8",
    },
    "ANA": {
        "full_name": "Aiva Anagnostiadis",
        "team": "Hitech TGR",
        "color": "#FFFFFF",
        "sponsor": "Tag Heuer",
        "number": "11",
    },
    "LAR": {
        "full_name": "Alba Larsen",
        "team": "MP Motorsport",
        "color": "#cd2028",
        "sponsor": "Tommy Hilfiger",
        "number": "12",
    },
    "FER": {
        "full_name": "Rafaela Ferreira",
        "team": "Campos Racing",
        "color": "#6692FF",
        "sponsor": "Racing Bulls",
        "number": "18",
    },
    "LLO": {
        "full_name": "Ella Lloyd",
        "team": "Rodin Motorsport",
        "color": "#FF8000",
        "sponsor": "McLaren",
        "number": "20",
    },
    "PAL": {
        "full_name": "Alisha Palmowski",
        "team": "Campos Racing",
        "color": "#001344",
        "sponsor": "Red Bull Racing",
        "number": "21",
    },
    "NOB": {
        "full_name": "Aurelia Nobels",
        "team": "ART Grand Prix",
        "color": "#FFC0CB",
        "sponsor": "Puma",
        "number": "22",
    },
    "CIC": {
        "full_name": "Joanne Ciconte",
        "team": "MP Motorsport",
        "color": "#cb007b",
        "sponsor": "F1 Academy",
        "number": "25",
    },
    "CHO": {
        "full_name": "Chloe Chong",
        "team": "Rodin Motorsport",
        "color": "#3F0F12",
        "sponsor": "Charlotte Tilbury",
        "number": "27",
    },
    "PIN": {
        "full_name": "Doriane Pin",
        "team": "Prema Racing",
        "color": "#00D7B6",
        "sponsor": "Mercedes",
        "number": "28",
    },
    "BLO": {
        "full_name": "Lia Block",
        "team": "ART Grand Prix",
        "color": "#1868DB",
        "sponsor": "Williams",
        "number": "57",
    },
    "WEU": {
        "full_name": "Maya Weug",
        "team": "MP Motorsport",
        "color": "#002663",
        "sponsor": "Scuderia Ferrari",
        "number": "64",
    },
    "HAU": {
        "full_name": "Tina Hausmann",
        "team": "Prema Racing",
        "color": "#229971",
        "sponsor": "Aston Martin",
        "number": "64",
    },
    # Add more drivers as needed...
}


def get_driver_info(code):
    return DRIVERS.get(
        code,
        {
            "full_name": "Unknown",
            "team": "Unknown",
            "color": "#CCCCCC",
            "sponsor": "Unknown",
            "number": "00",
        },
    )


def get_team_info(code):
    return TEAMS.get(code, {"color": "#CCCCCC"})
