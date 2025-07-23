library ieee;
use ieee.std_logic_1164.all;
use std.env.all;

entity difficulty_timer_tb is
end entity difficulty_timer_tb;

architecture tb of difficulty_timer_tb is
  constant C00 : integer := 4;
  constant C01 : integer := 3;
  constant C10 : integer := 2;
  constant C11 : integer := 1;

  signal clk       : std_logic := '0';
  signal reset     : std_logic := '1';
  signal start_sig : std_logic := '0';
  signal sw        : std_logic_vector(1 downto 0) := "00";
  signal timeout_sig : std_logic;
begin
  clk_gen: process
  begin
    wait for 5 ns; clk <= not clk;
  end process;

  dut: entity work.difficulty_timer
    generic map (
      CYCLES_00 => C00,
      CYCLES_01 => C01,
      CYCLES_10 => C10,
      CYCLES_11 => C11
    )
    port map (
      clk      => clk,
      reset    => reset,
      start    => start_sig,
      sw_level => sw,
      timeout  => timeout_sig
    );

  stim: process
  begin
    reset <= '1';
    wait for 20 ns;
    reset <= '0';
    wait for 10 ns;

    sw <= "00";
    start_sig <= '1'; wait for 10 ns; start_sig <= '0';
    for i in 1 to C00 loop
      wait until rising_edge(clk);
    end loop;
    if timeout_sig /= '1' then
      report "Timeout not asserted at level 00" severity error;
    end if;

    wait until rising_edge(clk);
    if timeout_sig /= '0' then
      report "Timeout stuck at level 00" severity error;
    end if;

    sw <= "01";
    start_sig <= '1'; wait for 10 ns; start_sig <= '0';
    for i in 1 to C01 loop
      wait until rising_edge(clk);
    end loop;
    if timeout_sig /= '1' then
      report "Timeout not asserted at level 01" severity error;
    end if;
    wait until rising_edge(clk);
    if timeout_sig /= '0' then
      report "Timeout stuck at level 01" severity error;
    end if;

    sw <= "10";
    start_sig <= '1'; wait for 10 ns; start_sig <= '0';
    for i in 1 to C10 loop
      wait until rising_edge(clk);
    end loop;
    if timeout_sig /= '1' then
      report "Timeout not asserted at level 10" severity error;
    end if;
    wait until rising_edge(clk);
    if timeout_sig /= '0' then
      report "Timeout stuck at level 10" severity error;
    end if;

    sw <= "11";
    start_sig <= '1'; wait for 10 ns; start_sig <= '0';
    for i in 1 to C11 loop
      wait until rising_edge(clk);
    end loop;
    if timeout_sig /= '1' then
      report "Timeout not asserted at level 11" severity error;
    end if;
    wait until rising_edge(clk);
    if timeout_sig /= '0' then
      report "Timeout stuck at level 11" severity error;
    end if;

    report "Difficulty Timer OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
