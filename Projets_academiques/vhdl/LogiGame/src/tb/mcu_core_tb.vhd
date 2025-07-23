-- tb/mcu_core_tb.vhd
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity mcu_core_tb is
end entity mcu_core_tb;

architecture tb of mcu_core_tb is
  signal clk    : std_logic := '0';
  signal reset  : std_logic := '1';
  signal PC_sig : unsigned(6 downto 0);
  signal INSTR  : std_logic_vector(9 downto 0);
begin

  clk_gen: process
  begin
    wait for 5 ns;
    clk <= not clk;
  end process;

  UUT: entity work.mcu_core
    port map(
      clk   => clk,
      reset => reset,
      PC    => PC_sig,
      INSTR => INSTR
    );

  stim: process
  begin
    report "ETAPE 1 : Appliquer reset" severity note;
    reset <= '1';
    wait until rising_edge(clk);
    reset <= '0';
    report "ETAPE 1 : Reset relâché" severity note;

    wait for 1 ns;

    if PC_sig /= to_unsigned(0, 7) then
      report "ERREUR : PC n'est pas à 0 après reset" severity error;
      stop(1);
    else
      report "NOTE : PC = 0 correct après reset" severity note;
    end if;

    wait until rising_edge(clk);
    wait for 1 ns; 
    if PC_sig /= to_unsigned(1, 7) then
      report "ERREUR : PC n'est pas à 1 au cycle 1" severity error;
      stop(1);
    else
      report "NOTE : PC = 1 correct au cycle 1" severity note;
    end if;

    if INSTR(0) = 'U' or INSTR(1) = 'U' or INSTR(2) = 'U' or INSTR(3) = 'U' or
       INSTR(4) = 'U' or INSTR(5) = 'U' or INSTR(6) = 'U' or INSTR(7) = 'U' or
       INSTR(8) = 'U' or INSTR(9) = 'U' then
      report "ERREUR : INSTR indéfini à PC = 1" severity error;
      stop(1);
    else
      report "NOTE : INSTR valide à PC = 1" severity note;
    end if;

    wait until rising_edge(clk);
    wait for 1 ns;
    if PC_sig /= to_unsigned(2, 7) then
      report "ERREUR : PC n'est pas à 2 au cycle 2" severity error;
      stop(1);
    else
      report "NOTE : PC = 2 correct au cycle 2" severity note;
    end if;

    if INSTR(0) = 'U' or INSTR(1) = 'U' or INSTR(2) = 'U' or INSTR(3) = 'U' or
       INSTR(4) = 'U' or INSTR(5) = 'U' or INSTR(6) = 'U' or INSTR(7) = 'U' or
       INSTR(8) = 'U' or INSTR(9) = 'U' then
      report "ERREUR : INSTR indéfini à PC = 2" severity error;
      stop(1);
    else
      report "NOTE : INSTR valide à PC = 2" severity note;
    end if;

    report "FIN DU TB CPU" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
