library ieee;
use ieee.std_logic_1164.all;

entity lfsr4 is
  port(
    clk          : in  std_logic;
    reset        : in  std_logic;
    enable       : in  std_logic;
    lfsr_out     : out std_logic_vector(3 downto 0);
    bit_feedback : out std_logic
  );
end entity lfsr4;

architecture rtl of lfsr4 is
  signal state    : std_logic_vector(3 downto 0) := "0001";
  signal feedback : std_logic;
begin
  feedback <= state(3) xor state(2);
  bit_feedback <= feedback;

  process(clk, reset)
  begin
    if reset = '1' then
      state <= "0001";
    elsif rising_edge(clk) then
      if enable = '1' then
        state <= state(2 downto 0) & feedback;
      end if;
    end if;
  end process;

  lfsr_out <= state;
end architecture rtl;
