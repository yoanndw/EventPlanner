import time

def input_name(prompt):
    while True:
        s = input(prompt).strip()
        if len(s) == 0:
            print("[ERREUR] Le nom doit contenir au moins une lettre, un chiffre, ou un caractere special.\n")
        else:
            return s

def input_time(prompt, start_time=None):
    while True:
        s = input(prompt).strip()
        try:
            t = time.strptime(s, "%H:%M")
        except ValueError:
            print("[ERREUR] Heure incorrecte.\n")
        else:
            if start_time is not None and t <= start_time:
                print("[ERREUR] L'evenement doit se finir au moins une minute apres le debut.\n")
                continue
            return t