library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.reg_pkg.all;

entity buffers is
  port(
    clk       : in  std_logic;
    reset     : in  std_logic;
    SEL_ROUTE : in  std_logic_vector(3 downto 0);
    -- Entrées
    A_IN      : in  slv4;
    B_IN      : in  slv4;
    S_OUT     : in  std_logic_vector(7 downto 0);
    SR_OUT_L  : in  std_logic;
    SR_OUT_R  : in  std_logic;
    SEL_FCT   : in  slv4;
    SEL_OUT   : in  slv2;
    -- Sorties mémorisées
    Buffer_A  : out slv4;
    Buffer_B  : out slv4;
    MEM_C1    : out slv4;
    MEM_C2    : out slv4;
    MEM_SR_L  : out std_logic;
    MEM_SR_R  : out std_logic;
    MEM_SFCT  : out slv4;
    MEM_SOUT  : out slv2
  );
end entity buffers;

architecture rtl of buffers is
  signal rA, rB       : slv4 := (others=>'0');
  signal rC1, rC2     : slv4 := (others=>'0');
  signal rSR_L, rSR_R : std_logic := '0';
  signal rSFCT        : slv4 := (others=>'0');
  signal rSOUT        : slv2 := (others=>'0');
begin
  process(clk, reset)
  begin
    if reset='1' then
      rA    <= (others=>'0');
      rB    <= (others=>'0');
      rC1   <= (others=>'0');
      rC2   <= (others=>'0');
      rSR_L <= '0';
      rSR_R <= '0';
      rSFCT <= (others=>'0');
      rSOUT <= (others=>'0');
    elsif rising_edge(clk) then
      -- mémoires toujours chargées
      rSR_L <= SR_OUT_L;
      rSR_R <= SR_OUT_R;
      rSFCT <= SEL_FCT;
      rSOUT <= SEL_OUT;
      -- mémoires conditionnelles
      case SEL_ROUTE is
        when "0000" => rA  <= A_IN;
        when "0001" => rA  <= rC1;
        when "0010" => rA  <= rC1; -- LSB selection can be added if needed
        when "0011" => rA  <= rC2;
        when "0100" => rA  <= rC2; -- MSB selection if needed
        when "0101" => rA  <= S_OUT(3 downto 0);
        when "0110" => rA  <= S_OUT(7 downto 4);
        when "0111" => rB  <= B_IN;
        when "1000" => rB  <= rC1;
        when "1001" => rB  <= rC1; -- LSB selection if needed
        when "1010" => rB  <= rC2;
        when "1011" => rB  <= rC2; -- MSB selection if needed
        when "1100" => rB  <= S_OUT(3 downto 0);
        when "1101" => rB  <= S_OUT(7 downto 4);
        when "1110" => rC1 <= S_OUT(3 downto 0);
        when "1111" => rC2 <= S_OUT(3 downto 0);
        when others => null;
      end case;
    end if;
  end process;

  -- Assignation des sorties
  Buffer_A  <= rA;
  Buffer_B  <= rB;
  MEM_C1    <= rC1;
  MEM_C2    <= rC2;
  MEM_SR_L  <= rSR_L;
  MEM_SR_R  <= rSR_R;
  MEM_SFCT  <= rSFCT;
  MEM_SOUT  <= rSOUT;
end architecture rtl;
