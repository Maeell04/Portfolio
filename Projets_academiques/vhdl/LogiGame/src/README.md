# Nom du projet

Micro-contrôleur ludique en VHDL

Projet réalisé en VHDL dans le cadre du module TE608.

## Contenu du projet

* reg\_pkg.vhd : paquetage des types et constantes partagées
* buffers.vhd : buffers à trois états pour le bus de données
* routing.vhd : réseau interconnexion entre unités
* ual.vhd : unité arithmético logique 8 bits
* mcu\_core.vhd : cœur du micro contrôleur
* lfsr4.vhd : générateur pseudo aléatoire 4 bits
* difficulty\_timer.vhd : minuterie pour augmentation de difficulté
* score\_counter.vhd : compteur de score
* response\_checker.vhd : validation des réponses utilisateur

Les bancs de test associés \_tb.vhd se trouvent dans le dossier tb/.

## Lancer le projet

1. Pré-requis
   GHDL ≥ 4.0 backend mcode ou LLVM — GTKWave recommandé pour lire les fichiers VCD.

2. Compilation

# packages
ghdl -a --std=08 reg_pkg.vhd

# core
ghdl -a --std=08 buffers.vhd routing.vhd mcu_core.vhd

# calcul
ghdl -a --std=08 ual.vhd

# gameplay
ghdl -a --std=08 lfsr4.vhd difficulty_timer.vhd score_counter.vhd response_checker.vhd


3. Exécution des bancs de test

# core
ghdl -a --std=08 tb/mcu_core_tb.vhd
ghdl -e --std=08 mcu_core_tb
ghdl -r mcu_core_tb --vcd=mcu_core_tb.vcd

# calcul
ghdl -a --std=08 tb/ual_tb.vhd
ghdl -e --std=08 ual_tb
ghdl -r ual_tb --vcd=ual_tb.vcd

# gameplay
ghdl -a --std=08 tb/lfsr4_tb.vhd tb/difficulty_timer_tb.vhd tb/score_counter_tb.vhd tb/response_checker_tb.vhd
ghdl -e --std=08 lfsr4_tb difficulty_timer_tb score_counter_tb response_checker_tb
ghdl -r lfsr4_tb --vcd=lfsr4_tb.vcd
ghdl -r difficulty_timer_tb --vcd=difficulty_timer_tb.vcd
ghdl -r score_counter_tb --vcd=score_counter_tb.vcd
ghdl -r response_checker_tb --vcd=response_checker_tb.vcd
```

## Technologies utilisées

* VHDL-2008
* GHDL pour la simulation
* GTKWave pour analyse des chronogrammes
