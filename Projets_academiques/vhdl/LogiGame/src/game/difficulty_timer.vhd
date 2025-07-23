library ieee;
use ieee.std_logic_1164.all;

entity difficulty_timer is
  generic (
    CYCLES_00 : integer := 100000000;
    CYCLES_01 : integer := 50000000;
    CYCLES_10 : integer := 25000000;
    CYCLES_11 : integer := 12500000
  );
  port (
    clk      : in  std_logic;
    reset    : in  std_logic;
    start    : in  std_logic;
    sw_level : in  std_logic_vector(1 downto 0);
    timeout  : out std_logic
  );
end entity difficulty_timer;

architecture rtl of difficulty_timer is
  signal count_reg   : integer range 0 to CYCLES_00 := 0;
  signal running     : std_logic := '0';
  signal timeout_reg : std_logic := '0';
begin
  process(clk, reset)
    variable threshold : integer;
  begin
    if reset = '1' then
      count_reg   <= 0;
      running     <= '0';
      timeout_reg <= '0';
    elsif rising_edge(clk) then
      if start = '1' then
        case sw_level is
          when "00" => threshold := CYCLES_00;
          when "01" => threshold := CYCLES_01;
          when "10" => threshold := CYCLES_10;
          when "11" => threshold := CYCLES_11;
          when others => threshold := CYCLES_00;
        end case;
        count_reg   <= threshold - 1;
        running     <= '1';
        timeout_reg <= '0';
      elsif running = '1' then
        if count_reg > 0 then
          count_reg <= count_reg - 1;
        else
          timeout_reg <= '1';
          running     <= '0';
        end if;
      else
        timeout_reg <= '0';
      end if;
    end if;
  end process;

  timeout <= timeout_reg;
end architecture rtl;
