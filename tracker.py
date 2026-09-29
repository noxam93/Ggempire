import os
import json
import requests

# Szukamy sojuszu o nazwie Reborn przez oficjalne API GGE Tracker
SEARCH_URL = "https://api.gge-tracker.com/api/v1/alliances"

def update_tracker():
    try:
        # Pobieramy listę/szukamy sojuszu
        response = requests.get(SEARCH_URL, params={"name": "Reborn"})
        if response.status_code == 200:
            alliances = response.json()
            # Szukamy na serwerze PL1
            target_alliance = None
            for a in alliances.get('alliances', alliances):
                if "reborn" in a.get('name', '').lower() and (a.get('server') == 'pl1' or 'pl' in str(a.get('server', '')).lower()):
                    target_alliance = a
                    break
            
            # Jeśli nie znaleziono po serwerze, bierzemy pierwsze pasujące
            if not target_alliance and len(alliances) > 0:
                target_alliance = alliances[0]

            if target_alliance:
                alliance_id = target_alliance.get('id')
                print(f"Znaleziono sojusz! ID: {alliance_id}, Nazwa: {target_alliance.get('name')}")
                
                # Pobieramy szczegółowe dane graczy tego sojuszu
                details_url = f"https://api.gge-tracker.com/api/v1/alliances/id/{alliance_id}"
                detail_res = requests.get(details_url)
                if detail_res.status_code == 200:
                    data = detail_res.json()
                    # Zapisujemy do pliku dane.json w repozytorium, żeby strona mogła je odczytać
                    with open('dane.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print("Zapisano dane do dane.json pomyślnie.")
            else:
                print("Nie znaleziono sojuszu Reborn.")
        else:
            print("Błąd połączenia z API GGE Tracker:", response.status_code)
    except Exception as e:
        print("Wystąpił błąd:", str(e))

if __name__ == "__main__":
    update_tracker()
  
