library ieee;
use ieee.std_logic_1164.all;
use work.reg_pkg.all;

entity routing is
  port(
    SEL_ROUTE    : in  std_logic_vector(3 downto 0);
    Buffer_A_reg : in  slv4;
    Buffer_B_reg : in  slv4;
    MEM_C1       : in  slv4;
    MEM_C2       : in  slv4;
    S_OUT        : in  std_logic_vector(7 downto 0);
    B_IN         : in  slv4;
    A_IN         : in  slv4;
    A_in_sel     : out slv4;
    B_in_sel     : out slv4
  );
end entity routing;

architecture rtl of routing is
begin
  process(SEL_ROUTE, Buffer_A_reg, Buffer_B_reg, MEM_C1, MEM_C2, S_OUT, A_IN, B_IN)
  begin
    A_in_sel <= (others=>'0');
    B_in_sel <= (others=>'0');

    case SEL_ROUTE is
      -- Buffer_A selections
      when "0000" => A_in_sel <= A_IN;
      when "0001" => A_in_sel <= MEM_C1;
      when "0010" => A_in_sel <= MEM_C1;         
      when "0011" => A_in_sel <= MEM_C2;
      when "0100" => A_in_sel <= MEM_C2;          
      when "0101" => A_in_sel <= S_OUT(3 downto 0);
      when "0110" => A_in_sel <= S_OUT(7 downto 4);

      -- Buffer_B selections
      when "0111" => B_in_sel <= B_IN;
      when "1000" => B_in_sel <= MEM_C1;
      when "1001" => B_in_sel <= MEM_C1;           
      when "1010" => B_in_sel <= MEM_C2;
      when "1011" => B_in_sel <= MEM_C2;         
      when "1100" => B_in_sel <= S_OUT(3 downto 0);
      when "1101" => B_in_sel <= S_OUT(7 downto 4);

      when "1110" =>
        null;
      when "1111" =>
        null;

      when others =>
        null;
    end case;
  end process;
end architecture rtl;
