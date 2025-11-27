#include "lcd/lcd.h"
#include "utils.h"
#include "enemy.h"
#include "limits.h"
#define SCREEN_LEFT 2
#define SCREEN_RIGHT 158
#define SCREEN_TOP 2
#define SCREEN_BOTTOM 60
#define NUM_RED_ENEMIES 3
#define NUM_GREEN_ENEMIES 1

// 全局子弹池变量
RedBulletPool red_bullet_pool = {0};
YellowBulletPool yellow_bullet_pool = {0};
GreenBulletPool green_bullet_pool = {0};
PlayerBulletPool player_bullet_pool = {0};


void init_red_bullet_pool(void) {
    for (int i = 0; i < MAX_RED_BULLETS; i++) {
        red_bullet_pool.bullets[i].active = 0;
    }
    red_bullet_pool.active_count = 0;
}

void init_yellow_bullet_pool(void) {
    for (int i = 0; i < MAX_YELLOW_BULLETS; i++) {
        yellow_bullet_pool.bullets[i].active = 0;
    }
    yellow_bullet_pool.active_count = 0;
}

void init_green_bullet_pool(void) {
    for (int i = 0; i < MAX_GREEN_BULLETS; i++) {
        green_bullet_pool.bullets[i].active = 0;
    }
    green_bullet_pool.active_count = 0;
}

void init_player_bullet_pool(void) {
    for (int i = 0; i < MAX_PLAYER_BULLETS; i++) {
        player_bullet_pool.bullets[i].active = 0;
    }
    player_bullet_pool.active_count = 0;
}



Enemy red_enemies[NUM_RED_ENEMIES] = {
    {4,3,4,3,1},
    {10, 20,10, 20, 1},  // 第一个敌人
    {20, 5, 20, 5, 1} // 第二个敌人
}; 
EnemyBullet* red_enemy_bullet_list=NULL;

EnemyBullet* yellow_enemy_bullet_list = NULL; 
EnemyBullet* green_enemy_bullet_list = NULL;
Bullet* player_bullet_list=NULL;
Enemy yellow_enemies[NUM_YELLOW_ENEMIES] = {
    {5, 4, 5, 4,1},// ,  // 新增敌人1
    {15, 4, 15, 4,1}, 
    {25, 4, 25, 4,1}, // 新增敌人2
    {35, 4, 35, 4,1},  // 新增敌人3
    {45, 4, 45, 4, 1},
    {55, 4, 55, 4,1},
    {65, 4, 65, 4, 1},
    {75, 4, 75, 4, 1}   // 原有敌人
};

















void update_red_enemy() {
    static int respawn_timer[NUM_RED_ENEMIES] = {0};
    // 擦除旧位置
    for(int i=0; i<NUM_RED_ENEMIES; i++){
    LCD_DrawTriangle(red_enemies[i].x,red_enemies[i].y,BLACK);
    if(!red_enemies[i].active) {
        if(++respawn_timer[i] >= 100) { // 3秒后重生（假设60帧/秒）
            red_enemies[i].x = red_enemies[i].initial_x;
            red_enemies[i].y = red_enemies[i].initial_y;
            red_enemies[i].active = 1;
            respawn_timer[i] = 0;
        }
        continue;
    }
    if(red_enemies[i].active) {
        // 移动逻辑（每次移动1像素）
        if(red_enemies[i].y < 60) {
            red_enemies[i].y += 1;
        } else {
            // 到达右边界后重置位置
            red_enemies[i].x = red_enemies[i].initial_x;
            red_enemies[i].y = red_enemies[i].initial_y;
        }
        
        // 绘制新位置
        LCD_DrawTriangle(red_enemies[i].x,red_enemies[i].y,RED);
    }
  }
}


void create_red_enemy_bullet(int* bullet_num) {
    for(int i = 0; i < NUM_RED_ENEMIES; i++){
        if(red_enemies[i].active) continue;
        
        // 在子弹池中寻找空闲位置
        for (int j = 0; j < MAX_RED_BULLETS; j++) {
            if (!red_bullet_pool.bullets[j].active) {
                EnemyBullet* new_bullet = &red_bullet_pool.bullets[j];
                
                new_bullet->initial_x = red_enemies[i].x;
                new_bullet->initial_y = red_enemies[i].y-5;
                new_bullet->x = red_enemies[i].x;
                new_bullet->y = red_enemies[i].y-5;
                new_bullet->dx = 3;
                new_bullet->dy = 0;
                new_bullet->phase = 0;
                new_bullet->active = 1;
                
                red_bullet_pool.active_count++;
                (*bullet_num)++;
                break;
            }
        }
    }
}

// 波形数据表（16个相位点的正弦近似值）
const int8_t wave_table[WAVE_LENGTH] = {
    0, 2, 3, 2, 0, -2, -3, -2,
    0, 2, 3, 2, 0, -2, -3, -2
};

void update_red_enemy_bullets(int* bullet_num) {
    for (int i = 0; i < MAX_RED_BULLETS; i++) {
        if (!red_bullet_pool.bullets[i].active) continue;
        
        EnemyBullet* bullet = &red_bullet_pool.bullets[i];
        int prev_x = bullet->x;
        int prev_y = bullet->y;

        // 更新相位
        bullet->phase = (bullet->phase + 1) % WAVE_LENGTH;
        int dy_offset = wave_table[bullet->phase];
        bullet->x += bullet->dx;
        bullet->y += dy_offset;

        // 碰撞检测 - 红色敌人
        int hit_enemy = 0;
        for (int j = 0; j < NUM_RED_ENEMIES; j++) {
            if (red_enemies[j].active &&
                abs(red_enemies[j].x - bullet->x) <= 4 &&
                abs(red_enemies[j].y - bullet->y) <= 4) {
                red_enemies[j].active = 0;
                LCD_DrawTriangle(red_enemies[j].x, red_enemies[j].y, BLACK);
                hit_enemy = 1;
                break;
            }
        }
        
        // 碰撞检测 - 黄色敌人
        if (!hit_enemy) {
            for (int j = 0; j < NUM_YELLOW_ENEMIES; j++) {
                if (yellow_enemies[j].active &&
                    abs(yellow_enemies[j].x - bullet->x) <= 3 &&
                    abs(yellow_enemies[j].y - bullet->y) <= 3) {
                    yellow_enemies[j].active = 0;
                    LCD_DrawRectangle(yellow_enemies[j].x-2, yellow_enemies[j].y-2,
                                     yellow_enemies[j].x+2, yellow_enemies[j].y+2, BLACK);
                    hit_enemy = 1;
                    break;
                }
            }
        }
        
        // 碰撞检测 - 绿色敌人
        if (!hit_enemy) {
            for (int j = 0; j < NUM_GREEN_ENEMIES; j++) {
                if (green_enemies[j].active &&
                    abs(green_enemies[j].x - bullet->x) <= 3 &&
                    abs(green_enemies[j].y - bullet->y) <= 3) {
                    green_enemies[j].active = 0;
                    LCD_DrawCircle(green_enemies[j].x, green_enemies[j].y, 3, BLACK);
                    hit_enemy = 1;
                    break;
                }
            }
        }
        
        // 如果击中敌人，子弹消失
        if (hit_enemy) {
            LCD_DrawCircle(prev_x, prev_y, 1, BLACK);
            bullet->active = 0;
            red_bullet_pool.active_count--;
            (*bullet_num)--;
            continue;
        }

        // 边界检查
        if (bullet->x < SCREEN_LEFT || bullet->x > SCREEN_RIGHT || 
            bullet->y < (SCREEN_TOP - WAVE_AMPLITUDE) || 
            bullet->y > (SCREEN_BOTTOM + WAVE_AMPLITUDE)) {
            LCD_DrawCircle(prev_x, prev_y, 1, BLACK);
            bullet->active = 0;
            red_bullet_pool.active_count--;
            (*bullet_num)--;
            continue;
        }

        // 原子操作：擦旧绘新
        LCD_DrawCircle(prev_x, prev_y, 1, BLACK);
        LCD_DrawCircle(bullet->x, bullet->y, 1, BLUE);
    }
}














void create_yellow_bullet(int x, int y, int* bullet_num) {
    for (int j = 0; j < MAX_YELLOW_BULLETS; j++) {
        if (!yellow_bullet_pool.bullets[j].active) {
            EnemyBullet* new_bullet = &yellow_bullet_pool.bullets[j];
            
            new_bullet->initial_x = x;
            new_bullet->initial_y = y+3;
            new_bullet->x = x;
            new_bullet->y = y+3;
            new_bullet->dx = 0;
            new_bullet->dy = 1;
            new_bullet->phase = 0;
            new_bullet->active = 1;
            
            yellow_bullet_pool.active_count++;
            (*bullet_num)++;
            break;
        }
    }
}








// 修改黄色敌人更新函数
void update_yellow_enemy(int* bullet_num) {
    static int re_timer[NUM_YELLOW_ENEMIES] = {0};
    static int move_counter = 0;
    move_counter++;
    if(move_counter<10){update_yellow_enemy_not_move();}
    // 修改移动逻辑为逐敌人更新
    if(move_counter >= 10) { // 加快移动频率到每3帧
        move_counter = 0;
        
        for(int i=0; i<NUM_YELLOW_ENEMIES; i++){
            if(yellow_enemies[i].active) {
                // 保存旧位置
                int old_x = yellow_enemies[i].x;
                int old_y = yellow_enemies[i].y;
                
                // 计算新位置
                yellow_enemies[i].x = (yellow_enemies[i].x % 158) + 1;
                
                // 原子操作：擦旧绘新
                LCD_DrawRectangle(old_x-2, old_y-2, old_x+2, old_y+2, BLACK);
                LCD_DrawRectangle(yellow_enemies[i].x-2, yellow_enemies[i].y-2,
                                yellow_enemies[i].x+2, yellow_enemies[i].y+2, YELLOW);
                create_yellow_bullet(yellow_enemies[i].x,yellow_enemies[i].y,bullet_num);
            }
        }
    }

    // 处理重生（独立于移动时序）
    for(int i=0; i<NUM_YELLOW_ENEMIES; i++){
        if(!yellow_enemies[i].active && ++re_timer[i] >= 180) {
            yellow_enemies[i].x = 20 + i*10;
            yellow_enemies[i].active = 1;
            re_timer[i] = 0;
            // 立即绘制新生成的敌人
            LCD_DrawRectangle(yellow_enemies[i].x-2, yellow_enemies[i].y-2,
                             yellow_enemies[i].x+2, yellow_enemies[i].y+2, YELLOW);
                             
        }
    }
    
    
}



// 添加敌人子弹更新函数（使用子弹池）
void update_yellow_enemy_bullets(int* bullet_num) {
    for (int i = 0; i < MAX_YELLOW_BULLETS; i++) {
        if (!yellow_bullet_pool.bullets[i].active) continue;
        
        EnemyBullet* bullet = &yellow_bullet_pool.bullets[i];
        LCD_DrawLine(bullet->x, bullet->y, bullet->x+3, bullet->y+3, BLACK);
        
        bullet->y += bullet->dy;
        
        if (bullet->y > 60) {
            bullet->active = 0;
            yellow_bullet_pool.active_count--;
            (*bullet_num)--;
        } else {
            LCD_DrawLine(bullet->x, bullet->y, bullet->x+3, bullet->y+3, BROWN);
        }
    }
}




















void create_green_bullet(int x, int y, int dx, int* bullet_num) {
    for (int j = 0; j < MAX_GREEN_BULLETS; j++) {
        if (!green_bullet_pool.bullets[j].active) {
            EnemyBullet* new_bullet = &green_bullet_pool.bullets[j];
            
            new_bullet->initial_x = x;
            new_bullet->x = x;
            new_bullet->initial_y = y;
            new_bullet->y = y;
            new_bullet->dx = dx;
            new_bullet->dy = 0;
            new_bullet->phase = 0;
            new_bullet->active = 1;
            
            green_bullet_pool.active_count++;
            (*bullet_num)++;
            break;
        }
    }
}




Enemy green_enemies[NUM_GREEN_ENEMIES] = {
    {10, 50, 10, 50,1},// ,  // 新增敌人1
};


void update_green_enemy(int* bullet_num,int player_x,int player_y) {
    static int re_timer[NUM_GREEN_ENEMIES] = {0};
    static int shoot_counter = 0;
    static int move_counter = 0;
    static int delays[NUM_GREEN_ENEMIES] = {0};
    static int dirs[NUM_GREEN_ENEMIES]={0};
    static int initialized = 0;
    if(!initialized){
        for(int i=0; i<NUM_GREEN_ENEMIES; i++) {
            dirs[i] = 1;  // 初始向右移动
            delays[i] = 1;
        }
        initialized = 1;
    }

    // 修改移动逻辑为逐敌人更新
    move_counter++;
    shoot_counter++;
    if(move_counter<1){update_green_enemy_not_move();}
    if(move_counter >= 1) { // 加快移动频率到每3帧
        move_counter = 0;

        for(int i=0; i<NUM_GREEN_ENEMIES; i++){
            if(green_enemies[i].active) {
                // 保存旧位置
                int old_x = green_enemies[i].x;
                int old_y = green_enemies[i].y;
                
                // 计算新位置
                int new_x = green_enemies[i].x  + dirs[i];
                if(new_x >= SCREEN_RIGHT) {
                    if(delays[i] <= 0) {
                        new_x = SCREEN_RIGHT - 1;
                        dirs[i] *= -1;      // 反转方向
                        delays[i] = 1;      // 重置延迟
                    } else {
                        new_x = SCREEN_RIGHT;
                        delays[i]--;       // 递减延迟
                    }
                }
                else if(new_x <= SCREEN_LEFT) {
                    if(delays[i] <= 0) {
                        new_x = SCREEN_LEFT + 1;
                        dirs[i] *= -1;
                        delays[i] = 1;
                    } else {
                        new_x = SCREEN_LEFT;
                        delays[i]--;
                    }
                }
                green_enemies[i].x = new_x;
                // 原子操作：擦旧绘新
                LCD_DrawCircle(old_x, old_y, 3, BLACK);
                LCD_DrawCircle(green_enemies[i].x, green_enemies[i].y, 3, GREEN);
               if(shoot_counter >= 10) {if(abs(green_enemies[i].x-player_x)<=15&&player_y<green_enemies[i].y){
                    shoot_counter = 0;
                    // 让绿色敌人发射黄色子弹
                    create_green_bullet(green_enemies[i].x, green_enemies[i].y, -1,bullet_num);}
                }
            }
        }
    }
    

    // 处理重生（独立于移动时序）
    for(int i=0; i<NUM_GREEN_ENEMIES; i++){
        if(!green_enemies[i].active && ++re_timer[i] >= 580) {
            green_enemies[i].x = 20 + i*10;
            green_enemies[i].active = 1;
            re_timer[i] = 0;
            // 立即绘制新生成的敌人
             LCD_DrawCircle(green_enemies[i].x ,green_enemies[i].y, 3, GREEN);
        }
    }
}




// 添加敌人子弹更新函数
void update_green_enemy_bullets(int* bullet_num) {
    for (int i = 0; i < MAX_GREEN_BULLETS; i++) {
        if (!green_bullet_pool.bullets[i].active) continue;
        
        EnemyBullet* bullet = &green_bullet_pool.bullets[i];
        LCD_DrawRectangle(bullet->x, bullet->y, bullet->x+2, bullet->y+2, BLACK);
        
        bullet->dy = (bullet->x - bullet->initial_x) * (bullet->x - bullet->initial_x);
        bullet->y -= bullet->dy;
        bullet->x += bullet->dx;
        
        // 碰撞检测 - 红色敌人
        int hit_enemy = 0;
        
        // 碰撞检测 - 绿色敌人
        
        // 如果击中敌人，子弹消失
        if (hit_enemy) {
            bullet->active = 0;
            green_bullet_pool.active_count--;
            (*bullet_num)--;
            continue;
        }
        
        if (bullet->y >= 61 || bullet->y <= 0) {
            bullet->active = 0;
            green_bullet_pool.active_count--;
            (*bullet_num)--;
        } else {
            LCD_DrawRectangle(bullet->x, bullet->y, bullet->x+2, bullet->y+2, BRED);
        }
    }
}


































// 新增函数：创建追踪弹
void create_tracking_bullet(int x, int y, int* bullet_num) {
    for (int i = 0; i < MAX_PLAYER_BULLETS; i++) {
        if (!player_bullet_pool.bullets[i].active) {
            Bullet* new_bullet = &player_bullet_pool.bullets[i];
            
            new_bullet->x = x;
            new_bullet->y = y;
            new_bullet->dx = 0;
            new_bullet->dy = 0;
            new_bullet->is_tracking = 1;
            new_bullet->active = 1;
            
            player_bullet_pool.active_count++;
            (*bullet_num)++;
            break;
        }
    }
}


// 修改后的子弹更新函数
void update_bullets(int* bullet_num) {
    for (int i = 0; i < MAX_PLAYER_BULLETS; i++) {
        if (!player_bullet_pool.bullets[i].active) continue;
        
        Bullet* ptr = &player_bullet_pool.bullets[i];
        int old_x = ptr->x;
        int old_y = ptr->y;
        
        // 追踪弹逻辑
        if (ptr->is_tracking) {
            // 寻找最近敌人
            Enemy* closest = NULL;
            int min_dist = INT_MAX;
            
            // 检查红色敌人
            for (int i = 0; i < NUM_RED_ENEMIES; i++){
            if (red_enemies[i].active) {
                int dx = red_enemies[i].x - ptr->x;
                int dy = red_enemies[i].y - ptr->y;
                int dist = dx*dx + dy*dy;
                if (dist < min_dist) {
                    min_dist = dist;
                    closest = &red_enemies[i];
                }
            }
        }
            
            // 检查黄色敌人
            for (int i = 0; i < NUM_YELLOW_ENEMIES; i++) {
                if (yellow_enemies[i].active) {
                    int dx = yellow_enemies[i].x - ptr->x;
                    int dy = yellow_enemies[i].y - ptr->y;
                    int dist = dx*dx + dy*dy;
                    if (dist < min_dist) {
                        min_dist = dist;
                        closest = &yellow_enemies[i];
                    }
                }
            }
            


            for (int i = 0; i < NUM_GREEN_ENEMIES; i++) {
                if (green_enemies[i].active) {
                    int dx = green_enemies[i].x - ptr->x;
                    int dy = green_enemies[i].y - ptr->y;
                    int dist = dx*dx + dy*dy;
                    if (dist < min_dist) {
                        min_dist = dist;
                        closest = &green_enemies[i];
                    }
                }
            }

            // 更新方向
            if (closest) {
                int dx = closest->x - ptr->x;
                int dy = closest->y - ptr->y;
                int abs_dx = abs(dx);
                int abs_dy = abs(dy);

                // 纯整数方向计算
                if (abs_dx > abs_dy) {
                    // X轴主导方向
                    ptr->dx = (dx > 0) ? TRACKING_SPEED : -TRACKING_SPEED;
                    ptr->dy = (abs_dx != 0) ? (dy * TRACKING_SPEED) / abs_dx : 0;
                } else if (abs_dy != 0) {
                    // Y轴主导方向
                    ptr->dy = (dy > 0) ? TRACKING_SPEED : -TRACKING_SPEED;
                    ptr->dx = (dx * TRACKING_SPEED) / abs_dy;
                } else {
                    // 静止状态
                    ptr->dx = 0;
                    ptr->dy = 0;
                }
            }
        }
        
        // 更新位置
        ptr->x += ptr->dx;
        ptr->y += ptr->dy;
        
        // 擦除旧位置（使用稍大的半径确保完全清除）
        LCD_DrawCircle(old_x, old_y, BULLET_RADIUS, BLACK);
        
        // 碰撞检测
        int hit = 0;
        for (int i = 0; i < NUM_RED_ENEMIES; i++) {
        if (red_enemies[i].active && 
            abs(red_enemies[i].x - ptr->x) <= ENEMY_HIT_RANGE && 
            abs(red_enemies[i].y - ptr->y) <= ENEMY_HIT_RANGE) {
            red_enemies[i].active = 0;
            LCD_DrawTriangle(red_enemies[i].x,red_enemies[i].y,BLACK);
            hit = 1;
        }
    }
        
        for (int i = 0; i < NUM_YELLOW_ENEMIES; i++) {
            if (yellow_enemies[i].active && 
                abs(yellow_enemies[i].x - ptr->x) <= ENEMY_HIT_RANGE && 
                abs(yellow_enemies[i].y - ptr->y) <= ENEMY_HIT_RANGE) {
                // yellow_enemies[i].active = 0;
                // LCD_DrawRectangle(yellow_enemies[i].x-2, yellow_enemies[i].y-2,
                //                  yellow_enemies[i].x+2, yellow_enemies[i].y+2, BLACK);
                hit = 1;
            }
        }

        for (int i = 0; i < NUM_GREEN_ENEMIES; i++) {
            if (green_enemies[i].active && 
                abs(green_enemies[i].x - ptr->x) <= ENEMY_HIT_RANGE && 
                abs(green_enemies[i].y - ptr->y) <= ENEMY_HIT_RANGE) {
                green_enemies[i].active=0;
                LCD_DrawCircle(green_enemies[i].x ,green_enemies[i].y, 3, BLACK);
                hit = 1;
            }
        }

        
         if (hit || ptr->x < 2 || ptr->x > 156 || ptr->y < 2 || ptr->y > 58) {
            ptr->active = 0;
            player_bullet_pool.active_count--;
            (*bullet_num)--;
        } else {
            LCD_DrawCircle(ptr->x, ptr->y, BULLET_RADIUS, CYAN);
        }
    }
}












void update_green_enemy_not_move() {
        for(int i=0; i<NUM_GREEN_ENEMIES; i++){
            if(green_enemies[i].active) {
                LCD_DrawCircle(green_enemies[i].x, green_enemies[i].y, 3, GREEN);
            }
        }
    }
    
void update_red_enemy_not_move(){
     for(int i=0; i<NUM_RED_ENEMIES; i++){
        if(red_enemies[i].active)LCD_DrawTriangle(red_enemies[i].x,red_enemies[i].y,RED);
    }
}


void update_red_enemy_bullets_not_move() {
    for (int i = 0; i < MAX_RED_BULLETS; i++) {
        if (red_bullet_pool.bullets[i].active) {
            EnemyBullet* bullet = &red_bullet_pool.bullets[i];
            LCD_DrawCircle(bullet->x, bullet->y, 1, BLUE);
        }
    }
}

void update_yellow_enemy_not_move() {
        for(int i=0; i<NUM_YELLOW_ENEMIES; i++){
            if(yellow_enemies[i].active) {
                LCD_DrawRectangle(yellow_enemies[i].x-2, yellow_enemies[i].y-2,
                                yellow_enemies[i].x+2, yellow_enemies[i].y+2, YELLOW);
            }
        }
}

void update_green_enemy_bullets_not_move() {
    for (int i = 0; i < MAX_GREEN_BULLETS; i++) {
        if (green_bullet_pool.bullets[i].active) {
            EnemyBullet* bullet = &green_bullet_pool.bullets[i];
            LCD_DrawRectangle(bullet->x, bullet->y, bullet->x+2, bullet->y+2, BRED);
        }
    }
}

void update_bullets_not_move() {
    // 重绘所有active的追踪子弹
    for (int i = 0; i < MAX_PLAYER_BULLETS; i++) {
        if (!player_bullet_pool.bullets[i].active) continue;
        LCD_DrawCircle(player_bullet_pool.bullets[i].x, player_bullet_pool.bullets[i].y, BULLET_RADIUS, CYAN);}
}

void update_yellow_enemy_bullets_not_move() {
    for (int i = 0; i < MAX_YELLOW_BULLETS; i++) {
        if (yellow_bullet_pool.bullets[i].active) {
            EnemyBullet* bullet = &yellow_bullet_pool.bullets[i];
            LCD_DrawLine(bullet->x, bullet->y, bullet->x+3, bullet->y+3, BROWN);
        }
    }
}