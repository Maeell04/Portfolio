library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity mcu_top_level_tb is
end entity mcu_top_level_tb;

architecture tb of mcu_top_level_tb is
  signal CLK100MHZ : std_logic := '0';
  signal BTN0      : std_logic := '1';
  signal BTN1      : std_logic := '0';
  signal BTN2      : std_logic := '0';
  signal BTN3      : std_logic := '0';
  signal SW        : std_logic_vector(3 downto 0) := (others => '0');
  signal LED       : std_logic_vector(3 downto 0);
  signal LD3_R, LD3_G, LD3_B : std_logic;
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
    variable i: integer;
  begin
    BTN0 <= '0';
    wait until rising_edge(CLK100MHZ);
    BTN0 <= '1';
    wait until rising_edge(CLK100MHZ);

    wait until rising_edge(CLK100MHZ);
    assert LED = "1010"
      report "Initial score should be 10" severity error;

    BTN1 <= '1';  -- bouton rouge par exemple
    wait until LD3_R = '1';
    BTN1 <= '0';
    wait until rising_edge(CLK100MHZ);
    assert LED = "1001"
      report "Score did not decrement after correct hit" severity error;

    SW(3) <= '1'; SW(2) <= '1';
    wait until LD3_G = '1';
    wait until rising_edge(CLK100MHZ);
    assert GAME_OVER = '1'
      report "Game over did not assert on timeout" severity error;

    report "mcu_top_level TB OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
