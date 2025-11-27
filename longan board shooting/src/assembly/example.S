.global scenario_selector
.global check_buttons
.global LCD_ShowString
.extern scenes

.section .rodata
prompt1: .asciz "L-R-C to select:"
prompt2: .asciz "<           >"
prompt3: .asciz "SW1 to confirm"

.section .text
scenario_selector:
    # 参数: a0 = initial_choice
    # 返回值: a0 = 最终选择
    
    addi sp, sp, -24         
    sw ra, 20(sp)            
    sw s0, 16(sp)            
    sw s1, 12(sp)
    sw s2, 8(sp)
    sw s3, 4(sp)
    sw a0, 0(sp)             # initial_selection->a0
    
    li s2, 0xFF              # 初始化按钮状态
    
    # 初始显示 - 直接传递选择值
    mv a0, sp                # 将栈指针作为参数传递
    jal update_display

main_loop:
    jal check_buttons
    mv s1, a0                # s1 = 当前按钮状态
    
    beq s1, s2, check_confirm # 状态未变化
    
    mv s2, s1                # 更新last_state
    
    andi t0, s1, 0x07        # 检查方向键
    beqz t0, check_confirm
    
    lw t1, 0(sp)             # 加载当前选择
    
    # 方向键处理
    andi t2, t0, 1
    bnez t2, set_left
    andi t2, t0, 2
    bnez t2, set_center
    andi t2, t0, 4
    bnez t2, set_right

set_left:
    li t1, 1
    j update

set_center:
    li t1, 2
    j update

set_right:
    li t1, 3

update:
    sw t1, 0(sp)             # 保存新选择值
    mv a0, sp                # 传递栈指针给显示函数
    jal update_display

check_confirm:
    andi t0, s1, 0x8         # 检查确认键(SW1)
    beqz t0, main_loop
    
    lw a0, 0(sp)             # 加载返回值
    
    
    lw s3, 4(sp)
    lw s2, 8(sp)
    lw s1, 12(sp)
    lw s0, 16(sp)
    lw ra, 20(sp)
    addi sp, sp, 24
    ret

# 更新显示函数 - 接收栈指针参数
# 参数: a0 = 主函数栈指针
update_display:
    addi sp, sp, -20        
    sw ra, 16(sp)            
    sw a0, 12(sp)            
    sw a1, 8(sp)
    sw a2, 4(sp)
    sw a3, 0(sp)
    
    # 显示固定提示文本
    la a2, prompt1
    li a0, 10
    li a1, 10
    li a3, 0xFFFF            
    jal LCD_ShowString
    
    la a2, prompt2
    li a0, 20
    li a1, 30
    li a3, 0xFFFF
    jal LCD_ShowString
    
    la a2, prompt3
    li a0, 20
    li a1, 50
    li a3, 0xFFFF
    jal LCD_ShowString
    
    # 获取当前选择值
    lw t0, 12(sp)            # 加载主栈指针
    lw t1, 0(t0)             # 获取选择值(偏移0)
    
    # 场景字符串
    addi t1, t1, -1          
    slli t1, t1, 2           
    la t2, scenes            # 加载全局数组基址
    add t2, t2, t1           
    lw a2, 0(t2)             
    
    # 显示场景字符串
    li a0, 50
    li a1, 30
    li a3, 0x07FF            
    jal LCD_ShowString
    
    
    lw a3, 0(sp)
    lw a2, 4(sp)
    lw a1, 8(sp)
    lw a0, 12(sp)
    lw ra, 16(sp)
    addi sp, sp, 20
    ret