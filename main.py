from events import EventPlanner, EventCreationException
from input_utils import input_name, input_time

def main():
    planner = EventPlanner()
    print("Planificateur d'evenements")
    while True:
        action = input("\nVeuillez saisir une action\n1. Lister evenements\n2. Ajouter evenement\n3. Quitter\n").strip()
        if action == "1":
            print()
            if len(planner.list_events()) == 0:
                print("Aucun evenement planifie.")
            else:
                for e in planner.list_events():
                    print("-", e)
        elif action == "2":
            while True:
                name = input_name("Nom de l'evenement : ")
                start = input_time("Heure de debut : ")
                end = input_time("Heure de fin : ")

                try:
                    conflicts = planner.add_event(name, start, end)
                except EventCreationException as e:
                    print(f"[ERREUR] {e}\n")
                    continue
                else:
                    if len(conflicts) > 0:
                        print(f"Evenements en conflit avec ce nouvel evenement :")
                        for e in conflicts:
                            print(f"- {e}")
                    print("\n\nUn evenement ajoute avec succes.")
                finally:
                    break
                
        elif action == "3":
            break

    print("Fin.")



if __name__ == "__main__":
    main()