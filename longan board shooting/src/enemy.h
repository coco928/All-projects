#ifndef ENEMIES_H
#define ENEMIES_H

#include <stdlib.h>

#define NUM_YELLOW_ENEMIES 8
#define NUM_RED_ENEMIES 3
#define NUM_GREEN_ENEMIES 1
#define TRACKING_SPEED 2
#define BULLET_RADIUS 2
#define ENEMY_HIT_RANGE 3
#define WAVE_LENGTH 16
#define WAVE_AMPLITUDE 3

// 子弹池定义
#define MAX_RED_BULLETS 8
#define MAX_YELLOW_BULLETS 256
#define MAX_PLAYER_BULLETS 1 
#define MAX_GREEN_BULLETS 6 // 新增绿色子弹池大小

// 修改Bullet结构体 - 移除next指针
typedef struct Bullet {
    int x;
    int y;
    int dx;
    int dy;
    int is_tracking;
    int active;
} Bullet;

typedef struct Enemy {
    int x;
    int y;
    int initial_x;
    int initial_y;
    int active;
} Enemy;

// 修改EnemyBullet结构体 - 移除next指针
typedef struct EnemyBullet {
    int initial_x;
    int initial_y;
    int x;
    int y;
    int dx;
    int dy;
    int phase;
    int active;
} EnemyBullet;

// 子弹池结构
typedef struct {
    EnemyBullet bullets[MAX_RED_BULLETS];
    int active_count;
} RedBulletPool;

typedef struct {
    EnemyBullet bullets[MAX_YELLOW_BULLETS];
    int active_count;
} YellowBulletPool;

typedef struct {
    EnemyBullet bullets[MAX_GREEN_BULLETS];
    int active_count;
} GreenBulletPool;

typedef struct {
    Bullet bullets[MAX_PLAYER_BULLETS];
    int active_count;
} PlayerBulletPool;

// 声明全局变量
extern Enemy enemy;
extern Enemy yellow_enemies[NUM_YELLOW_ENEMIES];
extern Enemy red_enemies[NUM_RED_ENEMIES];
extern Enemy green_enemies[NUM_GREEN_ENEMIES];
extern RedBulletPool red_bullet_pool;
extern YellowBulletPool yellow_bullet_pool;
extern GreenBulletPool green_bullet_pool;
extern PlayerBulletPool player_bullet_pool;

// 函数声明
void init_red_bullet_pool(void);
void init_yellow_bullet_pool(void);
void init_green_bullet_pool(void); // 新增绿色子弹池初始化
void init_player_bullet_pool(void);
void update_red_enemy(void);
void create_red_enemy_bullet(int* bullet_num);
void update_red_enemy_bullets(int* bullet_num);
void update_yellow_enemy(int* bullet_num);
void update_yellow_enemy_bullets(int* bullet_num);
void create_yellow_bullet(int x, int y, int* bullet_num);
void update_green_enemy(int* bullet_num,int player_x,int player_y);
void update_green_enemy_bullets(int* bullet_num);
void create_green_bullet(int x, int y, int dx, int* bullet_num);
void create_tracking_bullet(int x, int y,int* bullet_num);
void update_bullets(int* bullet_num);
void update_green_enemy_not_move();
void update_red_enemy_not_move();
void update_red_enemy_bullets_not_move();
void update_yellow_enemy_not_move();
void update_green_enemy_bullets_not_move();
void update_bullets_not_move();
void update_yellow_enemy_bullets_not_move();
#endif