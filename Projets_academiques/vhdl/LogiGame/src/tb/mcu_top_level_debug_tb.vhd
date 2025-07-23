library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity mcu_top_level_debug_tb is
end entity mcu_top_level_debug_tb;

architecture tb of mcu_top_level_debug_tb is
  signal CLK100MHZ : std_logic := '0';
  signal BTN0      : std_logic := '1';
  signal BTN1      : std_logic := '0';
  signal BTN2      : std_logic := '0';
  signal BTN3      : std_logic := '0';
  signal SW        : std_logic_vector(3 downto 0) := (others => '0');
  signal LED       : std_logic_vector(3 downto 0);
  signal LD3_R     : std_logic;
  signal LD3_G     : std_logic;
  signal LD3_B     : std_logic;
  signal GAME_OVER : std_logic;
begin
  clk_gen: process
  begin
    wait for 5 ns;
    CLK100MHZ <= not CLK100MHZ;
  end process;

  UUT: entity work.mcu_top_level
    port map(
      CLK100MHZ => CLK100MHZ,
      BTN0      => BTN0,
      BTN1      => BTN1,
      BTN2      => BTN2,
      BTN3      => BTN3,
      SW        => SW,
      LED       => LED,
      LD3_R     => LD3_R,
      LD3_G     => LD3_G,
      LD3_B     => LD3_B,
      GAME_OVER => GAME_OVER
    );

  stim: process
  begin
    report "DEBUG: Etape 1 - Appliquer reset" severity note;
    BTN0 <= '0';
    wait until rising_edge(CLK100MHZ);
    BTN0 <= '1';
    report "DEBUG: Etape 1 - Reset relâché" severity note;
    wait for 1 ns;

    report "DEBUG: Etape 2 - Attendre LED non-U" severity note;
    wait until LED(0) /= 'U';
    wait until LED(1) /= 'U';
    wait until LED(2) /= 'U';
    wait until LED(3) /= 'U';
    report "DEBUG: Etape 2 - LED initialisée" severity note;

    report "DEBUG: Etape 3 - Presser BTN1" severity note;
    BTN1 <= '1';
    wait for 1 ns;
    wait until LED = "1001" or LED = "1000" or 
               LED = "0111" or LED = "0110" or 
               LED = "0101" or LED = "0100" or 
               LED = "0011" or LED = "0010" or 
               LED = "0001" or LED = "0000";
    report "DEBUG: Etape 3 - Score décrémenté" severity note;
    BTN1 <= '0';

    report "DEBUG: Etape 4 - Mettre SW=11" severity note;
    SW(3) <= '1';
    SW(2) <= '1';
    wait for 1 ns;
    report "DEBUG: Etape 4 - Attendre LD3_G" severity note;
    wait until LD3_G = '1';
    report "DEBUG: Etape 4 - LD3_G détecté" severity note;
    report "DEBUG: Etape 4 - Attendre GAME_OVER" severity note;
    wait until GAME_OVER = '1';
    report "DEBUG: Etape 4 - GAME_OVER détecté" severity note;

    report "DEBUG: Etape 5 - Fin du TB" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
