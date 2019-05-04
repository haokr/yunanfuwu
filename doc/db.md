# 数据库设计

## 数据库配置

- MySQL

## 用户 User

- id            # shortuuid
- name
- username      # 登陆名
- password      # 密码
- parent        # 父账号 -> 用户
- group         # 组 -> 组表；分管的设备组
- record        # 操作记录
- address       # 地址
- describe      # 用户描述
- create_time
- modify_time

## 用户操作记录 user_record

- id            # uuid
- user          # -> 用户表
- ip            # 登陆IP
- operation     # 登陆/查看/处理报警信息
- create_time
- modify_time

## 报警记录 alarm_record

- id            # uuid
- equipment     # 设备 -> 设备表
- class         # 报警类型
- describe      # 描述
- create_time
- modify_time

## 分组管理 group

- id            # uuid
- name
- equipments    # 设备 -> 中间表
- account       # 账号 -> 用户表
- alarm_record  # 报警记录
- create_time 
- modify_time

## 设备分组中间表 gruop_equipment_relationship

- id
- group         # 指向组表
- equipment     # 指向设备表
- create_time
- modify_time

## 设备 equipment

- id            # uuid
- manufacturer  # 制造商
- model         # 型号
- groups        # 组 -> 中间表
- status        # 是否启动
- alarm_record  # 报警记录 -> 报警记录表
- create_time
- modify_time