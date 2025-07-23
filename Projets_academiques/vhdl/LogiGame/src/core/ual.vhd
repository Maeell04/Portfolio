library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity ual is
    port (
        A        : in  std_logic_vector(3 downto 0);
        B        : in  std_logic_vector(3 downto 0);
        SR_IN_L  : in  std_logic;
        SR_IN_R  : in  std_logic;
        SEL_FCT  : in  std_logic_vector(3 downto 0);
        S        : out std_logic_vector(7 downto 0);
        SR_OUT_L : out std_logic;
        SR_OUT_R : out std_logic
    );
end entity ual;

architecture rtl of ual is
    signal a_u : unsigned(3 downto 0);
    signal b_u : unsigned(3 downto 0);
begin
    -- Conversion des entrées en type numérique
    a_u <= unsigned(A);
    b_u <= unsigned(B);

    process(a_u, b_u, SR_IN_L, SR_IN_R, SEL_FCT)
        variable v_tmp8 : unsigned(7 downto 0);
        variable v_tmp5 : unsigned(4 downto 0);
    begin
        -- initialisation des variables
        v_tmp8 := (others => '0');
        v_tmp5 := (others => '0');
        SR_OUT_L <= '0';
        SR_OUT_R <= '0';

        case SEL_FCT is
            when "0000" =>
                -- NOP
                null;
            when "0001" =>
                v_tmp8(3 downto 0) := a_u;
            when "0010" =>
                v_tmp8(3 downto 0) := b_u;
            when "0011" =>
                v_tmp8(3 downto 0) := unsigned(not A);
            when "0100" =>
                v_tmp8(3 downto 0) := unsigned(not B);
            when "0101" =>
                v_tmp8(3 downto 0) := a_u and b_u;
            when "0110" =>
                v_tmp8(3 downto 0) := a_u or b_u;
            when "0111" =>
                v_tmp8(3 downto 0) := a_u xor b_u;
            when "1000" =>
                v_tmp8(3 downto 0) := unsigned(SR_IN_L & A(3 downto 1));
                SR_OUT_R <= A(0);
            when "1001" =>
                v_tmp8(3 downto 0) := unsigned(A(2 downto 0) & SR_IN_R);
                SR_OUT_L <= A(3);
            when "1010" =>
                v_tmp8(3 downto 0) := unsigned(SR_IN_L & B(3 downto 1));
                SR_OUT_R <= B(0);
            when "1011" =>
                v_tmp8(3 downto 0) := unsigned(B(2 downto 0) & SR_IN_R);
                SR_OUT_L <= B(3);
            when "1100" =>
                v_tmp5 := ('0' & a_u) + ('0' & b_u);
                if SR_IN_R = '1' then
                    v_tmp5 := v_tmp5 + 1;
                end if;
                v_tmp8(3 downto 0) := v_tmp5(3 downto 0);
                v_tmp8(4)          := v_tmp5(4);
                SR_OUT_R           <= v_tmp5(4);
            when "1101" =>
                v_tmp5 := ('0' & a_u) + ('0' & b_u);
                v_tmp8(3 downto 0) := v_tmp5(3 downto 0);
                v_tmp8(4)          := v_tmp5(4);
                SR_OUT_R           <= v_tmp5(4);
            when "1110" =>
                v_tmp5 := ('0' & a_u) - ('0' & b_u);
                v_tmp8(3 downto 0) := v_tmp5(3 downto 0);
                v_tmp8(4)          := v_tmp5(4);
                SR_OUT_R           <= not v_tmp5(4);
            when "1111" =>
                v_tmp8 := a_u * b_u;
            when others =>
                null;
        end case;

        S <= std_logic_vector(v_tmp8);
    end process;

end architecture rtl;
