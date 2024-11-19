import time

def input_name(prompt):
    while True:
        s = input(prompt).strip()
        if len(s) == 0:
            print("[ERREUR] Le nom doit contenir au moins une lettre, un chiffre, ou un caractere special.\n")
        else:
            return s

def input_time(prompt):
    while True:
        s = input(prompt).strip()
        try:
            t = time.strptime(s, "%H:%M")
        except ValueError:
            print("[ERREUR] Heure incorrecte.\n")
        else:
            return t