from pocketsphinx import LiveSpeech

#Paramètres audio
DEVICE = "default"    # via ~/.asoundrc pour hw:3,0 @ 16000Hz
RATE = 16000

#Chemins vers modèle & dictionnaire
MODEL_PATH = "/home/pi/Robot_Files/Voice_Control/pocketsphinx-fr"
DICT_PATH  = "/home/pi/Robot_Files/Voice_Control/fr.dict"
KWS_PATH   = "/home/pi/Robot_Files/Voice_Control/keywords.txt"

#Configuration LiveSpeech pour le keyword-spotting
speech = LiveSpeech(
    audio_device=DEVICE,
    sampling_rate=RATE,
    buffer_size=2048,
    lm=False,
    hmm=MODEL_PATH,
    dict=DICT_PATH,
    kws=KWS_PATH
)

def voice_control():
    print("En ecoute… (Ctrl-C pour quitter)")
    try:
        for phrase in speech:
            raw = (phrase.hypothesis() or "").strip().lower()
            if not raw:
                continue

            # Debug : afficher le brut et les tokens
            tokens = [tok for tok in raw.split() if tok]
            print(f"brut detecte : «{raw}» → tokens: {tokens}")

            # Calcul des scores pour chaque action
            scores = {act: 0 for act in actions}
            for tok in tokens:
                for act, matcher in matchers.items():
                    if matcher(tok):
                        scores[act] += 1

            # Choix de l'action la plus fréquente
            best_act, best_score = max(scores.items(), key=lambda x: x[1])
            if best_score > 0:
                print(f"Action choisie : {best_act} (score {best_score})")
                actions[best_act]()
            else:
                print(f"Aucune action reconnue dans «{raw}»")

    except KeyboardInterrupt:
        print("\nArret manuel, a bientot !")