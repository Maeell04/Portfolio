library ieee;
use ieee.std_logic_1164.all;
use std.env.all;

entity lfsr4_tb is
end entity lfsr4_tb;

architecture tb of lfsr4_tb is
  signal clk           : std_logic := '0';
  signal reset         : std_logic := '1';
  signal enable        : std_logic := '0';
  signal lfsr_out_sig  : std_logic_vector(3 downto 0);
  signal feedback_sig  : std_logic;

  type seq_t is array(0 to 7) of std_logic_vector(3 downto 0);
  constant expected_seq : seq_t := (
    "0001", 
    "0010",  
    "0100",  
    "1001",  
    "0011",  
    "0110",  
    "1101",  
    "1010"  
  );
begin
  clk <= not clk after 5 ns;

  dut: entity work.lfsr4
    port map(
      clk          => clk,
      reset        => reset,
      enable       => enable,
      lfsr_out     => lfsr_out_sig,
      bit_feedback => feedback_sig
    );

  stim: process
    variable idx : integer := 0;
  begin
    reset  <= '1';
    enable <= '0';
    wait for 20 ns;
    reset  <= '0';
    wait for 10 ns;

    if lfsr_out_sig /= expected_seq(0) then
      report "Initial LFSR state incorrect" severity error;
    end if;

    enable <= '1';

    for idx in 1 to 7 loop
      wait until rising_edge(clk);
      if lfsr_out_sig /= expected_seq(idx) then
        report "LFSR sequence mismatch" severity error;
      end if;
    end loop;

    report "LFSR4 OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
