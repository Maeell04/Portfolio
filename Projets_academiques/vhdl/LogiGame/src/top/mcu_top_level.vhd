library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.reg_pkg.all;

entity mcu_top_level is
  port(
    CLK100MHZ : in  std_logic;                  -- horloge 100 MHz
    BTN0      : in  std_logic;                  -- Reset (actif haut)
    BTN1      : in  std_logic;                  -- Bouton rouge
    BTN2      : in  std_logic;                  -- Bouton vert
    BTN3      : in  std_logic;                  -- Bouton bleu
    SW        : in  std_logic_vector(3 downto 0);-- Switches, SW(3 downto 2) = niveau
    LED       : out std_logic_vector(3 downto 0);-- LEDs 4 bits pour score
    LD3_R     : out std_logic;                  -- LED rouge du stimulus
    LD3_G     : out std_logic;                  -- LED verte du stimulus
    LD3_B     : out std_logic;                  -- LED bleue du stimulus
    GAME_OVER : out std_logic                   -- LED Game Over
  );
end entity mcu_top_level;

architecture rtl of mcu_top_level is
  -- Signaux internes pour connecter au game_top
  signal user_btns    : slv4;                 
  signal sw_level     : slv2;                
  signal score_leds_s : slv4;               
  signal timeout_s    : std_logic;            
  signal valid_hit_s  : std_logic;         
begin
  -- Mappe les boutons : user_btns = "0" & BTN3 & BTN2 & BTN1
  user_btns(3) <= '0';
  user_btns(2) <= BTN3;
  user_btns(1) <= BTN2;
  user_btns(0) <= BTN1;

  -- Mappe les switches pour la difficulté : sw_level = SW(3 downto 2)
  sw_level(1) <= SW(3);
  sw_level(0) <= SW(2);

  -- Instanciation de game_top
  U_GAME: entity work.game_top
    port map(
      clk          => CLK100MHZ,
      reset        => BTN0,
      user_buttons => user_btns,
      sw_level     => sw_level,
      score_leds   => score_leds_s,
      timeout_led  => timeout_s,
      correct_led  => valid_hit_s
    );

  -- Sorties physiques
  LED       <= std_logic_vector(score_leds_s);
  GAME_OVER <= timeout_s;
  LD3_R     <= valid_hit_s;
  LD3_G     <= timeout_s;
  LD3_B     <= '0'; 
end architecture rtl;
