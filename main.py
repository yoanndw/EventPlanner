from events import EventPlanner
from input_utils import input_name, input_time

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
            while True:
                name = input_name("Nom de l'evenement : ")
                if planner.event_exists(name):
                    print(f"[ERREUR] L'evenement avec le nom \"{name}\" existe deja.\n")
                else:
                    break

            start = input_time("Heure de debut : ")
            end = input_time("Heure de fin : ", start)

            planner.add_event(name, start, end)
            print("Un evenement ajoute avec succes.\n")
        elif action == "3":
            break

    print("Fin.")



if __name__ == "__main__":
    main()