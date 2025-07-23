library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;
use work.reg_pkg.all;

entity game_top_tb is
end entity game_top_tb;

architecture tb of game_top_tb is
  signal clk           : std_logic := '0';
  signal reset         : std_logic := '1';
  signal user_buttons  : slv4     := (others => '0');
  signal sw_level      : slv2     := "00";
  signal score_leds    : slv4;
  signal timeout_led   : std_logic;
  signal correct_led   : std_logic;
begin

  clk_gen: process
  begin
    wait for 5 ns; 
    clk <= not clk;
  end process;

  UUT: entity work.game_top
    port map(
      clk           => clk,
      reset         => reset,
      user_buttons  => user_buttons,
      sw_level      => sw_level,
      score_leds    => score_leds,
      timeout_led   => timeout_led,
      correct_led   => correct_led
    );

  stim: process
    variable i : integer;
  begin
    reset <= '1';
    wait until rising_edge(clk);
    reset <= '0';
    wait until rising_edge(clk);

    wait until rising_edge(clk);
    wait until rising_edge(clk);

    user_buttons <= "0001";
    wait until correct_led = '1';

    user_buttons <= "0010";
    wait until correct_led = '0';

    sw_level <= "11";
    wait until rising_edge(clk);
    for i in 1 to 12 loop
      wait until rising_edge(clk);
    end loop;
    wait until timeout_led = '1';
    wait until timeout_led = '0';

    report "Game Top OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
