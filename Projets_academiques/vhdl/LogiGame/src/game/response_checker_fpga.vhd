library ieee;
use ieee.std_logic_1164.all;
use work.reg_pkg.all; 

entity response_checker_fpga is
  port(
    clk        : in  std_logic;
    reset      : in  std_logic;
    led_color  : in  slv3;      
    btn_r      : in  std_logic;
    btn_g      : in  std_logic;  
    btn_b      : in  std_logic;  
    timeout    : in  std_logic;
    valid_hit  : out std_logic;  
    game_over  : out std_logic  
  );
end entity response_checker_fpga;

architecture rtl of response_checker_fpga is
  type state_t is (IDLE, WAIT_RESP, DONE);
  signal state : state_t := IDLE;
begin
  process(clk, reset)
  begin
    if reset = '1' then
      state     <= IDLE;
      valid_hit <= '0';
      game_over <= '0';
    elsif rising_edge(clk) then
      case state is
        when IDLE =>
          valid_hit <= '0';
          game_over <= '0';
          if led_color /= "000" then
            state <= WAIT_RESP;
          end if;
        when WAIT_RESP =>
          if timeout = '1' then
            game_over <= '1';
            state     <= DONE;
          elsif (led_color = "100" and btn_r = '1') or
                (led_color = "010" and btn_g = '1') or
                (led_color = "001" and btn_b = '1') then
            valid_hit <= '1';
            state     <= DONE;
          end if;
        when DONE =>
          null;
      end case;
    end if;
  end process;
end architecture rtl;
