library ieee;
use ieee.std_logic_1164.all;
use work.reg_pkg.all;  

entity response_checker is
  port(
    clk        : in  std_logic;
    reset      : in  std_logic;
    user_in  : in  slv4;    
    result   : in  slv4;    
    correct  : out std_logic
  );
end entity response_checker;

architecture rtl of response_checker is
begin
  correct <= '1' when user_in = result else '0';
end architecture rtl;
