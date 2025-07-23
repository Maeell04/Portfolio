library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity mcu_core is
  port(
    clk       : in  std_logic;
    reset     : in  std_logic;
    PC        : out unsigned(6 downto 0);
    INSTR     : out std_logic_vector(9 downto 0);
    SEL_ROUTE : out std_logic_vector(3 downto 0);
    SEL_FCT   : out std_logic_vector(3 downto 0);
    SEL_OUT   : out std_logic_vector(1 downto 0)
  );
end entity mcu_core;

architecture rtl of mcu_core is
  subtype instr_t is std_logic_vector(9 downto 0);
  type rom_t is array(0 to 127) of instr_t;
  constant instr_mem : rom_t := (
    0 => "0000001100",
    1 => "0110101101",
    2 => "1011000110",
    others => (others => '0')
  );

  signal PC_reg   : unsigned(6 downto 0) := (others => '0');
  signal inst     : std_logic_vector(9 downto 0);
begin
  process(clk, reset)
  begin
    if reset = '1' then
      PC_reg <= (others => '0');
    elsif rising_edge(clk) then
      PC_reg <= PC_reg + 1;
    end if;
  end process;

  PC <= PC_reg;
  inst <= instr_mem(to_integer(PC_reg));
  INSTR <= inst;
  SEL_ROUTE <= inst(9 downto 6);
  SEL_FCT   <= inst(5 downto 2);
  SEL_OUT   <= inst(1 downto 0);
end architecture rtl;
