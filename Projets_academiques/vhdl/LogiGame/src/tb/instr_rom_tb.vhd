library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity instr_rom_tb is
end entity;

architecture tb of instr_rom_tb is
  signal clk  : std_logic := '0';
  signal addr : unsigned(6 downto 0) := (others=>'0');
  signal data : std_logic_vector(9 downto 0);
begin
  clk_gen: process
  begin
    wait for 10 ns; clk <= not clk;
  end process;

  UUT: entity work.instr_rom
    port map(clk => clk, addr => addr, data => data);

  stim: process
  begin
    addr <= to_unsigned(0,7);  wait until rising_edge(clk); wait for 1 ns;
    assert data = "0000000000"
      report "Addr 0 wrong" severity error;
    addr <= to_unsigned(1,7);  wait until rising_edge(clk); wait for 1 ns;
    assert data = "0001000001"
      report "Addr 1 wrong" severity error;
    report "instr_rom OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
