library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity score_counter is
  port (
    clk        : in  std_logic;
    reset      : in  std_logic;
    correct    : in  std_logic;
    load_score : in  std_logic;
    max_score  : in  unsigned(3 downto 0);
    score_out  : out unsigned(3 downto 0)
  );
end entity score_counter;

architecture rtl of score_counter is
  signal score_reg : unsigned(3 downto 0) := (others=>'0');
begin
  process(clk, reset)
  begin
    if reset = '1' then
      score_reg <= (others => '0');
    elsif rising_edge(clk) then
      if load_score = '1' then
        score_reg <= max_score;
      elsif correct = '1' then
        if score_reg > 0 then
          score_reg <= score_reg - 1;
        end if;
      end if;
    end if;
  end process;

  score_out <= score_reg;
end architecture rtl;
