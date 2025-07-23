library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;
use work.reg_pkg.all;

entity buffers_tb is
end entity buffers_tb;

architecture tb of buffers_tb is
  signal clk       : std_logic := '0';
  signal reset     : std_logic := '1';
  signal SEL_ROUTE : std_logic_vector(3 downto 0) := (others=>'0');
  signal A_IN, B_IN: slv4 := (others=>'0');
  signal S_OUT     : std_logic_vector(7 downto 0) := (others=>'0');
  signal SR_OUT_L, SR_OUT_R : std_logic := '0';
  signal SEL_FCT   : slv4 := (others=>'0');
  signal SEL_OUT   : slv2 := (others=>'0');

  signal Buffer_A, Buffer_B, MEM_C1, MEM_C2 : slv4;
  signal MEM_SR_L, MEM_SR_R : std_logic;
  signal MEM_SFCT           : slv4;
  signal MEM_SOUT           : slv2;
begin
  clk_proc: process
  begin
    wait for 5 ns; clk <= not clk;
  end process;

  uut: entity work.buffers
    port map(
      clk       => clk,
      reset     => reset,
      SEL_ROUTE => SEL_ROUTE,
      A_IN      => A_IN,
      B_IN      => B_IN,
      S_OUT     => S_OUT,
      SR_OUT_L  => SR_OUT_L,
      SR_OUT_R  => SR_OUT_R,
      SEL_FCT   => SEL_FCT,
      SEL_OUT   => SEL_OUT,
      Buffer_A  => Buffer_A,
      Buffer_B  => Buffer_B,
      MEM_C1    => MEM_C1,
      MEM_C2    => MEM_C2,
      MEM_SR_L  => MEM_SR_L,
      MEM_SR_R  => MEM_SR_R,
      MEM_SFCT  => MEM_SFCT,
      MEM_SOUT  => MEM_SOUT
    );

  stim: process
  begin
    reset <= '1'; wait for 20 ns;
    reset <= '0'; wait for 20 ns;

    A_IN <= "1010"; S_OUT <= x"5C";
    SEL_ROUTE <= "0000"; wait for 20 ns;
    assert Buffer_A="1010" report "Err A_IN" severity error;

    SEL_ROUTE <= "0110"; wait for 20 ns;
    assert Buffer_A="0101" report "Err S_OUT_MSB" severity error;

    SR_OUT_L <= '1'; SR_OUT_R<='0'; SEL_FCT<="1101"; SEL_OUT<="10";
    wait for 20 ns;
    assert MEM_SR_L='1'   report "Err MEM_SR_L"   severity error;
    assert MEM_SR_R='0'   report "Err MEM_SR_R"   severity error;
    assert MEM_SFCT="1101" report "Err MEM_SFCT"  severity error;
    assert MEM_SOUT="10"   report "Err MEM_SOUT"  severity error;

    report "Buffers OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
