library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity score_counter_tb is
end entity score_counter_tb;

architecture tb of score_counter_tb is
  signal clk        : std_logic := '0';
  signal reset      : std_logic := '1';
  signal correct    : std_logic := '0';
  signal load_score : std_logic := '0';
  signal max_score  : unsigned(3 downto 0) := "1010"; 
  signal score_out  : unsigned(3 downto 0);
begin
  clk_gen: process
  begin
    wait for 5 ns;
    clk <= not clk;
  end process;


  dut: entity work.score_counter
    port map(
      clk        => clk,
      reset      => reset,
      correct    => correct,
      load_score => load_score,
      max_score  => max_score,
      score_out  => score_out
    );

  stim: process
    variable i : integer;
  begin
    reset <= '1';
    wait until rising_edge(clk);
    reset <= '0';

    load_score <= '1';
    wait until rising_edge(clk);
    load_score <= '0';

    if score_out /= max_score then
      report "Load score failed: got " & integer'image(to_integer(score_out)) severity error;
    end if;

    for i in 1 to 5 loop
      correct <= '1';
      wait until rising_edge(clk);
      correct <= '0';
      wait until rising_edge(clk);
    end loop;
    if score_out /= to_unsigned(5,4) then
      report "Score decrement failed: got " & integer'image(to_integer(score_out)) severity error;
    end if;

    for i in 1 to 10 loop
      correct <= '1';
      wait until rising_edge(clk);
      correct <= '0';
      wait until rising_edge(clk);
    end loop;
    if score_out /= to_unsigned(0,4) then
      report "Underflow protection failed: got " & integer'image(to_integer(score_out)) severity error;
    end if;

    report "Score Counter OK" severity note;
    wait for 20 ns;
    stop(0);
  end process;
end architecture tb;
