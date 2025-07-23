library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.reg_pkg.all; 

entity game_top is
  port(
    clk          : in  std_logic;
    reset        : in  std_logic;
    user_buttons : in  slv4;             
    sw_level     : in  slv2;        
    score_leds   : out slv4;              
    timeout_led  : out std_logic;     
    correct_led  : out std_logic       
  );
end entity game_top;

architecture rtl of game_top is
  -- Signaux internes
  signal lfsr_out_s    : std_logic_vector(3 downto 0);
  signal timeout_s     : std_logic;
  signal score_out_s   : unsigned(3 downto 0);
  signal resp_correct_s: std_logic;
begin
  U_LFSR: entity work.lfsr4
    port map(
      clk          => clk,
      reset        => reset,
      enable       => '1',  
      lfsr_out     => lfsr_out_s,
      bit_feedback => open
    );

  U_TIMER: entity work.difficulty_timer
    port map(
      clk       => clk,
      reset     => reset,
      start     => '1',      
      sw_level  => sw_level,
      timeout   => timeout_s
    );

  U_RESP: entity work.response_checker
    port map(
      clk       => clk,
      reset     => reset,
      user_in   => user_buttons,
      result    => lfsr_out_s,
      correct   => resp_correct_s
    );

  U_SCORE: entity work.score_counter
    port map(
      clk        => clk,
      reset      => reset,
      correct    => resp_correct_s,
      load_score => '1',           
      max_score  => to_unsigned(10, 4),
      score_out  => score_out_s
    );

  score_leds  <= std_logic_vector(score_out_s);
  timeout_led <= timeout_s;
  correct_led <= resp_correct_s;
end architecture rtl;
