library ieee;
use ieee.std_logic_1164.all;
use std.env.all;
use work.reg_pkg.all;  -- slv3

entity response_checker_fpga_tb is
end entity response_checker_fpga_tb;

architecture tb of response_checker_fpga_tb is
  signal clk        : std_logic := '0';
  signal reset      : std_logic := '1';
  signal led_color  : slv3     := (others=>'0');
  signal btn_r, btn_g, btn_b, timeout: std_logic := '0';
  signal valid_hit, game_over: std_logic;
begin
  clk_gen: process begin wait for 10 ns; clk<=not clk; end process;

  UUT: entity work.response_checker_fpga
    port map(
      clk        => clk,
      reset      => reset,
      led_color  => led_color,
      btn_r      => btn_r,
      btn_g      => btn_g,
      btn_b      => btn_b,
      timeout    => timeout,
      valid_hit  => valid_hit,
      game_over  => game_over
    );

  stim: process
  begin
    wait for 25 ns; reset <= '0'; wait until rising_edge(clk);

    led_color <= "100"; btn_r <= '1';
    wait until rising_edge(clk);
    assert valid_hit='1' report "Fail RED hit" severity error;

    led_color <= "010"; btn_r <= '0'; btn_g <= '1';
    wait until rising_edge(clk);
    assert valid_hit='0' and game_over='1'
      report "Fail GREEN game_over" severity error;

    reset <= '1'; wait for 20 ns; reset <= '0'; wait until rising_edge(clk);
    led_color <= "001"; timeout <= '1';
    wait until rising_edge(clk);
    assert game_over='1' report "Fail BLUE timeout" severity error;

    report "Response Checker FPGA OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
