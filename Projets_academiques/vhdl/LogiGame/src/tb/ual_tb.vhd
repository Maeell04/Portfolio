library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ual_tb is
end entity ual_tb;

architecture behavior of ual_tb is
    -- Signals connected to UUT
    signal A_s        : std_logic_vector(3 downto 0) := (others => '0');
    signal B_s        : std_logic_vector(3 downto 0) := (others => '0');
    signal SR_IN_L_s  : std_logic := '0';
    signal SR_IN_R_s  : std_logic := '0';
    signal SEL_FCT_s  : std_logic_vector(3 downto 0) := (others => '0');

    signal S_s        : std_logic_vector(7 downto 0);
    signal SR_OUT_L_s : std_logic;
    signal SR_OUT_R_s : std_logic;
begin
    -- Instantiate Unit Under Test (UUT)
    uut: entity work.ual
        port map(
            A        => A_s,
            B        => B_s,
            SR_IN_L  => SR_IN_L_s,
            SR_IN_R  => SR_IN_R_s,
            SEL_FCT  => SEL_FCT_s,
            S        => S_s,
            SR_OUT_L => SR_OUT_L_s,
            SR_OUT_R => SR_OUT_R_s
        );

    stim_proc: process
        variable idx             : integer;
        variable expected_slv    : std_logic_vector(7 downto 0);
        variable expected_sr_l   : std_logic;
        variable expected_sr_r   : std_logic;
        variable aval, bval      : integer;
        variable sumval          : integer;
        variable shrval, shlval  : integer;
    begin
        A_s       <= "0110";  
        B_s       <= "0011";  
        SR_IN_L_s <= '1';
        SR_IN_R_s <= '0';
        wait for 20 ns;

        aval := to_integer(unsigned(A_s));
        bval := to_integer(unsigned(B_s));

        for idx in 0 to 15 loop
            SEL_FCT_s <= std_logic_vector(to_unsigned(idx,4));
            wait for 20 ns;

            expected_slv  := (others => '0');
            expected_sr_l := '0';
            expected_sr_r := '0';

            case SEL_FCT_s is
                when "0000" => null;
                when "0001" => expected_slv(3 downto 0) := A_s;
                when "0010" => expected_slv(3 downto 0) := B_s;
                when "0011" => expected_slv(3 downto 0) := not A_s;
                when "0100" => expected_slv(3 downto 0) := not B_s;
                when "0101" => expected_slv(3 downto 0) := A_s and B_s;
                when "0110" => expected_slv(3 downto 0) := A_s or B_s;
                when "0111" => expected_slv(3 downto 0) := A_s xor B_s;
                when "1000" =>
                    shrval := aval / 2;
                    if SR_IN_L_s = '1' then shrval := shrval + 8; end if;
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(shrval,4));
                    expected_sr_r := '1' when (aval mod 2) = 1 else '0';
                when "1001" =>
                    shlval := (aval * 2) mod 16;
                    if SR_IN_R_s = '1' then shlval := shlval + 1; end if;
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(shlval,4));
                    expected_sr_l := '1' when aval >= 8 else '0';
                when "1010" =>
                    shrval := bval / 2;
                    if SR_IN_L_s = '1' then shrval := shrval + 8; end if;
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(shrval,4));
                    expected_sr_r := '1' when (bval mod 2) = 1 else '0';
                when "1011" =>
                    shlval := (bval * 2) mod 16;
                    if SR_IN_R_s = '1' then shlval := shlval + 1; end if;
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(shlval,4));
                    expected_sr_l := '1' when bval >= 8 else '0';
                when "1100" =>
                    sumval := aval + bval;
                    if SR_IN_R_s = '1' then sumval := sumval + 1; end if;
                    expected_sr_r := '1' when sumval > 15 else '0';
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(sumval mod 16,4));
                    expected_slv(4) := expected_sr_r;
                when "1101" =>
                    sumval := aval + bval;
                    expected_sr_r := '1' when sumval > 15 else '0';
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(sumval mod 16,4));
                    expected_slv(4) := expected_sr_r;
                when "1110" =>
                    sumval := aval - bval;
                    expected_sr_r := '1' when aval >= bval else '0';
                    expected_slv(3 downto 0) := std_logic_vector(to_unsigned(abs(sumval) mod 16,4));
                    expected_slv(4) := not expected_sr_r;
                when "1111" =>
                    sumval := aval * bval;
                    expected_slv := std_logic_vector(to_unsigned(sumval,8));
                when others => null;
            end case;

            assert S_s = expected_slv
                report "[ERROR] S mismatch" severity error;
            assert SR_OUT_L_s = expected_sr_l
                report "[ERROR] SR_OUT_L mismatch" severity error;
            assert SR_OUT_R_s = expected_sr_r
                report "[ERROR] SR_OUT_R mismatch" severity error;
        end loop;

        report "--- All UAL tests passed ---" severity note;
        wait;
    end process;

end architecture behavior;
