from events import EventPlanner

def main():
    planner = EventPlanner()
    print("Planificateur d'evenements")
    while True:
        action = input("Veuillez saisir une action\n1. Lister evenements\n2. Ajouter evenement\n3. Quitter\n").strip()
        if action == "1":
            if len(planner.list_events()) == 0:
                print("Aucun evenement planifie.")
            else:
                for e in planner.list_events():
                    print("-", e)
        elif action == "2":
            name = input("Nom de l'evenement : ")
            start = input("Heure de debut : ")
            end = input("Heure de fin : ")

            planner.add_event(name, start, end)
            print("Un evenement ajoute avec succes.")
        elif action == "3":
            break

    print("Fin.")



if __name__ == "__main__":
    main()