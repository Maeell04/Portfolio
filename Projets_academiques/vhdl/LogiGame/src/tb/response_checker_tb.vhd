library ieee;
use ieee.std_logic_1164.all;
use std.env.all;
use work.reg_pkg.all;  -- pour slv4

entity response_checker_tb is
end entity response_checker_tb;

architecture tb of response_checker_tb is
  signal clk       : std_logic := '0';
  signal reset     : std_logic := '1';
  signal user_in   : slv4 := (others => '0');
  signal result_s  : slv4 := (others => '0');
  signal correct_s : std_logic;
begin
  clk_gen: process
  begin
    wait for 5 ns;
    clk <= not clk;
  end process;

  dut: entity work.response_checker
    port map(
      clk     => clk,
      reset   => reset,
      user_in => user_in,
      result  => result_s,
      correct => correct_s
    );

  stim: process
  begin
    reset <= '1';
    wait for 20 ns;
    reset <= '0';
    wait for 10 ns; 

    user_in  <= "0011";
    result_s <= "0011";
    wait until rising_edge(clk);
    wait for 1 ns;

    user_in  <= "0100";
    result_s <= "0011";
    wait until rising_edge(clk);
    wait for 1 ns;

    user_in  <= "1010";
    result_s <= "1010";
    wait until rising_edge(clk);
    wait for 1 ns;

    user_in  <= "1111";
    result_s <= "0000";
    wait until rising_edge(clk);
    wait for 1 ns;

    report "Response Checker OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
