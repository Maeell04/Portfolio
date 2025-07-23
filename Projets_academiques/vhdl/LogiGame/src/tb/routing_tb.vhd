library ieee;
use ieee.std_logic_1164.all;
use work.reg_pkg.all;
use std.env.all;

entity routing_tb is
end entity routing_tb;

architecture tb of routing_tb is
  signal SEL_ROUTE_sig : std_logic_vector(3 downto 0) := (others=>'0');
  signal A_IN_sig      : slv4 := (others=>'0');
  signal B_IN_sig      : slv4 := (others=>'0');
  signal MEM_C1_sig    : slv4 := (others=>'0');
  signal MEM_C2_sig    : slv4 := (others=>'0');
  signal S_OUT_sig     : std_logic_vector(7 downto 0) := (others=>'0');

  signal A_out, B_out : slv4;
begin
  dut: entity work.routing
    port map(
      SEL_ROUTE     => SEL_ROUTE_sig,
      Buffer_A_reg  => A_IN_sig,
      Buffer_B_reg  => B_IN_sig,
      MEM_C1        => MEM_C1_sig,
      MEM_C2        => MEM_C2_sig,
      S_OUT         => S_OUT_sig,
      A_IN          => A_IN_sig,
      B_IN          => B_IN_sig,
      A_in_sel      => A_out,
      B_in_sel      => B_out
    );

  stim: process
  begin
    A_IN_sig <= "1010"; MEM_C1_sig <= "0011"; MEM_C2_sig <= "0101"; S_OUT_sig <= x"5C"; B_IN_sig <= "1111";
    SEL_ROUTE_sig <= "0000"; wait for 10 ns;
    assert A_out = "1010" report "Err A_IN_select" severity error;

    SEL_ROUTE_sig <= "0001"; wait for 10 ns;
    assert A_out = "0011" report "Err C1_low" severity error;

    SEL_ROUTE_sig <= "0011"; wait for 10 ns;
    assert A_out = "0101" report "Err C2_low" severity error;

    SEL_ROUTE_sig <= "0101"; wait for 10 ns;
    assert A_out = "1100" report "Err S_low" severity error;

    SEL_ROUTE_sig <= "0111"; wait for 10 ns;
    assert B_out = "1111" report "Err B_IN_select" severity error;

    SEL_ROUTE_sig <= "1000"; wait for 10 ns;
    assert B_out = "0011" report "Err C1_low_B" severity error;

    SEL_ROUTE_sig <= "1101"; wait for 10 ns;
    assert B_out = "0101" report "Err S_high_B" severity error;

    report "Routing OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
