library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity instr_rom is
  generic (
    DEPTH  : integer := 128;  
    WIDTH  : integer := 10
  );
  port (
    clk   : in  std_logic;
    addr  : in  unsigned(6 downto 0);                 
    data  : out std_logic_vector(WIDTH-1 downto 0)
  );
end entity instr_rom;

architecture rtl of instr_rom is
  type rom_t is array(0 to DEPTH-1) of std_logic_vector(WIDTH-1 downto 0);
  constant MEM : rom_t := (
    0   => "0000000000", 
    1   => "0001000001",  
    2   => "0010000010",    
    others => (others=>'0')
  );
begin
  process(clk)
  begin
    if rising_edge(clk) then
      data <= MEM(to_integer(addr));
    end if;
  end process;
end architecture rtl;
