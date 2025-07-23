library ieee;
use ieee.std_logic_1164.all;

package reg_pkg is
  subtype slv4 is std_logic_vector(3 downto 0);
  subtype slv3 is std_logic_vector(2 downto 0);  
  subtype slv2 is std_logic_vector(1 downto 0);
end package reg_pkg;
