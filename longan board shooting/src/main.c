#include "lcd/lcd.h"
#include "utils.h"
#include "assembly/example.h"
#include <stdlib.h> 
#include "enemy.h"
#include "n200_func.c"

#define BULLET_COOLDOWN 200    
#define PLAYER_MIN_X 3
#define PLAYER_MAX_X 157
#define PLAYER_MIN_Y 3
#define PLAYER_MAX_Y 77
#define TICKS_PER_SEC get_timer_freq() 

const char* scenes[] = {"Scene_1", "Scene_2", "Scene_3"};

#define ENEMY_BULLET_SPEED 3

int bullet = 0;

void IO_init(void) {
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_GPIOC);
    gpio_init(GPIOA, GPIO_MODE_IPD, GPIO_OSPEED_50MHZ,
            GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);
    gpio_init(GPIOC, GPIO_MODE_IPD, GPIO_OSPEED_50MHZ,
            GPIO_PIN_13 | GPIO_PIN_14 | GPIO_PIN_15);
    Lcd_Init();
    
    init_red_bullet_pool();
    init_yellow_bullet_pool();
    init_green_bullet_pool(); // 添加这一行
    init_player_bullet_pool();
}


int check_buttons() {
    int new_state = 0;
    static int last_state;
    new_state |= Get_Button(JOY_LEFT)   ? 0x1 : 0;
    new_state |= Get_Button(JOY_CTR)    ? 0x2 : 0;
    new_state |= Get_Button(JOY_RIGHT)  ? 0x4 : 0;
    new_state |= Get_Button(BUTTON_1)   ? 0x8 : 0;

  if(new_state != last_state && new_state == 0) {
    return last_state;
  }
    return new_state;
}


void update_fps_display(uint64_t current_time, char* fps_str, char* bullet_num) {
    static uint64_t last_fps_time = 0;
    static uint32_t frame_count = 0;
    const uint32_t timer_freq = get_timer_freq(); 
    
    frame_count++;
    
    if (current_time - last_fps_time >= timer_freq) { 
        uint32_t fps = frame_count;
        frame_count = 0;
        last_fps_time = current_time;
        
     
        fps_str[0] = (fps >= 1000) ? (fps / 1000) + '0' : ' ';
        fps_str[1] = (fps >= 100) ? ((fps / 100) % 10) + '0' : ' ';
        fps_str[2] = (fps >= 10) ? ((fps / 10) % 10) + '0' : ' ';
        fps_str[3] = (fps % 10) + '0';
        fps_str[4] = '\0';

        bullet_num[0] = (bullet >= 1000) ? (bullet/ 1000) + '0' : ' ';
        bullet_num[1] = (bullet>= 100) ? ((bullet/ 100) % 10) + '0' : ' ';
        bullet_num[2] = (bullet>= 10) ? ((bullet/ 10) % 10) + '0' : ' ';
        bullet_num[3] = (bullet% 10) + '0';
        bullet_num[4] = '\0';
   
        LCD_ShowString(40, 62, (unsigned char *)fps_str, WHITE);
        LCD_ShowString(100, 62, (unsigned char *)bullet_num, WHITE);
    }
}


int main(void) {
    IO_init();
    LCD_Clear(BLACK);
    int initial_selection = 1;
    int selected = scenario_selector(initial_selection);

    LCD_Clear(BLACK);
    LCD_ShowString(50, 30, (u8*)scenes[selected-1], RED);
    delay_1ms(200);
    LCD_Clear(BLACK);
    
    int player_x = 80;
    int player_y = 30;
    int attack_true = 0;
    
    LCD_DrawPoint_big(player_x,player_y,WHITE);
    LCD_ShowString(10,62,(const unsigned char*)"FPS",WHITE);
    LCD_ShowString(80,62,(const unsigned char*)"BUL",WHITE);
    
    char bullet_num[5]="0000";
    char fps_str[5]="0000";
    #define BUTTON_COOLDOWN 300
    
    // 按键冷却计时器
    static uint64_t last_button1_time = 0;
    static uint64_t last_button2_time = 0;
    
    while(1) {
        uint64_t current_time = get_timer_value() * 1000 / TICKS_PER_SEC;
        //red_enemy_bullet and player_bullet update
        static int bullet_speed_divider = 3;
        if(bullet_speed_divider>=2){bullet_speed_divider = 0;update_red_enemy_bullets(&bullet); update_bullets(&bullet);}
        else{update_red_enemy_bullets_not_move();update_bullets_not_move();}
        bullet_speed_divider++;
        
        //yellow_enemy_bullet_update
        static int yellow_bullet_speed_divider = 5;
        if(yellow_bullet_speed_divider>=5){update_yellow_enemy_bullets(&bullet);yellow_bullet_speed_divider=0;}
        else{update_yellow_enemy_bullets_not_move();}
        yellow_bullet_speed_divider ++;
      
        //player_update
        static int count = 5;
        LCD_DrawPoint_big(player_x,player_y,BLACK);
        if(Get_Button(JOY_LEFT)&&player_x>=6 &&count >= 1){player_x -= 2;count = 0;}
        else if(Get_Button(JOY_RIGHT)&&player_x<=154&&count >= 1 ){player_x += 2;count = 0;}
        else if(Get_Button(JOY_DOWN)&&player_y<=58&&count >=1){player_y += 2;count = 0;}
        else if(Get_Button(JOY_UP)&&player_y>=6&&count >= 1){player_y -= 2;count = 0;}
        LCD_DrawPoint_big(player_x,player_y,WHITE);
        count += 1;
        
        //green_enemy_bullet_update
        static int green_bullet_speed_divider = 5;
        if(green_bullet_speed_divider>=5){update_green_enemy_bullets(&bullet);green_bullet_speed_divider=0;}
        else{update_green_enemy_bullets_not_move();}
        green_bullet_speed_divider ++;


        //player_bullet_create
        static int attack_mode = 0; // 0: 追踪弹, 1: 红色敌人子弹, 2: 绿色敌人子弹
        static int attack_counter = 5;
        int b2 = Get_Button(BUTTON_2);
        int b1 = Get_Button(BUTTON_1);
        int button1_ready = (current_time - last_button1_time >= BUTTON_COOLDOWN);
        int button2_ready = (current_time - last_button2_time >= BUTTON_COOLDOWN);
        
        // BUTTON2控制追踪弹发射
        if(b2 && button2_ready) {
            attack_mode = 0;
            attack_true ^= 1;
            last_button2_time = current_time;
        }
        // BUTTON1控制切换到红色敌人子弹
        if(b1 && button1_ready) {
            attack_mode = 1;
            attack_true ^= 1;
            last_button1_time = current_time;
        }
        // JOY-CTR控制切换到绿色敌人子弹
        // BUTTON2控制追踪弹发射
        if(b2||b1) attack_true ^= 1;
        if(b2) attack_mode = 0;
        // BUTTON1控制切换到红色敌人子弹
        if(b1) attack_mode = 1;
        
        // JOY-CTR控制切换到绿色敌人子弹
        
        if(attack_true) {
            if(++attack_counter>=5){
                if(attack_mode == 0) {
                    // 发射追踪弹
                    create_tracking_bullet(player_x, player_y, &bullet);
                } else if(attack_mode == 1) {
                    // 发射红色敌人子弹
                    for (int j = 0; j < MAX_RED_BULLETS; j++) {
                        if (!red_bullet_pool.bullets[j].active) {
                            EnemyBullet* new_bullet = &red_bullet_pool.bullets[j];
                            
                            new_bullet->initial_x = player_x;
                            new_bullet->initial_y = player_y-5;
                            new_bullet->x = player_x;
                            new_bullet->y = player_y-5;
                            new_bullet->dx = 3;
                            new_bullet->dy = 0;
                            new_bullet->phase = 0;
                            new_bullet->active = 1;
                            
                            red_bullet_pool.active_count++;
                            bullet++;
                            break;
                        }
                    }
                } 
            }
        } else {
            attack_counter = 0;
        }

        //yellow_enemy_update and green_enemy_update
        update_yellow_enemy(&bullet);update_green_enemy(&bullet,player_x,player_y);
            
        //red_enemy_update
        static int red_enemy_speed_counter = 5;
        if(++red_enemy_speed_counter >= 5) { 
            update_red_enemy();
            red_enemy_speed_counter = 0;
        }
        else{update_red_enemy_not_move();}

        //red_enemy_bullet_create - 现在使用黄色子弹，只有死后才发射
        static int red_enemy_attack_counter = 10; 
        if(++red_enemy_attack_counter >= 10) {
                red_enemy_attack_counter = 0;
                // 让红色敌人死后发射黄色子弹
                for(int i = 0; i < NUM_RED_ENEMIES; i++){
                    if(!red_enemies[i].active) {
                        create_yellow_bullet(red_enemies[i].x, red_enemies[i].y, &bullet);
                    }
                }
        }
        
        // FPS count
        update_fps_display(get_timer_value(),fps_str,bullet_num);

    }
}
    
