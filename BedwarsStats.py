import requests
import json
import math
import os
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==============================================
# 1. 精确计算 Bedwars 星级（含威望循环）
# ==============================================
def calculate_bedwars_stars(exp):
    if exp < 0:
        return 0, 0, 0
    exp_per_prestige = 7000 + 96 * 5000
    prestige = exp // exp_per_prestige
    remaining = exp % exp_per_prestige
    stars_in_prestige = 0
    costs = [500, 1000, 2000, 3500]
    for cost in costs:
        if remaining >= cost:
            remaining -= cost
            stars_in_prestige += 1
        else:
            return prestige * 100 + stars_in_prestige, remaining, cost
    extra = remaining // 5000
    stars_in_prestige += extra
    remaining -= extra * 5000
    if stars_in_prestige >= 100:
        prestige += 1
        stars_in_prestige = 0
        return prestige * 100 + stars_in_prestige, remaining, 5000
    return prestige * 100 + stars_in_prestige, remaining, 5000

# ==============================================
# 2. 安全除法
# ==============================================
def safe_div(a, b):
    if b == 0:
        return float('inf') if a > 0 else 0.0
    return round(a / b, 2)

# ==============================================
# 3. 比率颜色映射
# ==============================================
def get_ratio_color(value, ratio_type):
    if math.isinf(value):
        return "\033[97m"
    if ratio_type == 'KD':
        if value < 0.5:
            return "\033[90m"
        elif value < 1:
            return "\033[97m"
        elif value < 2:
            return "\033[93m"
        elif value < 3:
            return "\033[38;5;208m"
        else:
            return "\033[91m"
    elif ratio_type == 'FKDR':
        if value < 1:
            return "\033[90m"
        elif value < 2:
            return "\033[97m"
        elif value < 3:
            return "\033[93m"
        elif value < 5:
            return "\033[38;5;208m"
        else:
            return "\033[91m"
    elif ratio_type == 'WL':
        if value < 0.4:
            return "\033[90m"
        elif value < 1:
            return "\033[97m"
        elif value < 2:
            return "\033[93m"
        elif value < 3:
            return "\033[38;5;208m"
        else:
            return "\033[91m"
    elif ratio_type == 'BBL':
        if value < 0.5:
            return "\033[90m"
        elif value < 1:
            return "\033[97m"
        elif value < 2:
            return "\033[93m"
        elif value < 3:
            return "\033[38;5;208m"
        else:
            return "\033[91m"
    return "\033[97m"

# ==============================================
# 4. 颜色映射（根据玩家数据判断）
# ==============================================
def get_display_color(player):
    if player.get("rank") == "YOUTUBER":
        return "\033[91m"
    if player.get("monthlyPackageRank") == "SUPERSTAR":
        return "\033[93m"
    rank = player.get("newPackageRank", "NORMAL")
    rank_colors = {
        "NORMAL": "\033[97m",
        "VIP": "\033[92m",
        "VIP_PLUS": "\033[92m",
        "MVP": "\033[96m",
        "MVP_PLUS": "\033[96m"
    }
    return rank_colors.get(rank, "\033[97m")

# ==============================================
# 5. 查询单个玩家（返回格式化后的行字符串）
# ==============================================
def query_player(api_key, player_name):
    """查询单个玩家，返回格式化好的行字符串（含颜色代码）"""
    url = f"https://api.hypixel.net/v2/player?key={api_key}&name={player_name}"
    RESET = "\033[0m"
    WHITE = "\033[97m"

    try:
        resp = requests.get(url, timeout=15)
        data = resp.json()
    except Exception as e:
        return f"[????]  {WHITE}{player_name:<18}{RESET}  请求异常      ".center(8) + " " * 8 + " " * 8

    if not data.get("success"):
        return f"[????]  {WHITE}{player_name:<18}{RESET}  API错误       ".center(8) + " " * 8 + " " * 8

    player = data.get("player")
    if not player:
        level_col = f"[????]".ljust(8)
        id_col = f"{WHITE}{player_name:<18}{RESET}"
        fkdr_col = "Nick或者不存在".center(8)
        wlr_col = " " * 8
        bblr_col = " " * 8
        return f"{level_col}{id_col}{fkdr_col}{wlr_col}{bblr_col}"

    # 保存原始 JSON 到本地（临时）
    filename = f"raw_data_{player_name}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    bw = player.get("stats", {}).get("Bedwars", {})
    display_name = player.get("displayname", "未知")
    color = get_display_color(player)

    if not bw:
        level_col = f"[????]".ljust(8)
        id_col = f"{WHITE}{display_name:<18}{RESET}"
        fkdr_col = "Nick或者不存在".center(8)
        wlr_col = " " * 8
        bblr_col = " " * 8
        # 清理临时文件
        if os.path.exists(filename):
            os.remove(filename)
        return f"{level_col}{id_col}{fkdr_col}{wlr_col}{bblr_col}"

    exp = bw.get("Experience", 0)
    stars, _, _ = calculate_bedwars_stars(exp)

    wins = bw.get("wins_bedwars", 0)
    losses = bw.get("losses_bedwars", 0)
    final_kills = bw.get("final_kills_bedwars", 0)
    final_deaths = bw.get("final_deaths_bedwars", 0)
    beds_broken = bw.get("beds_broken_bedwars", 0)
    beds_lost = bw.get("beds_lost_bedwars", 0)

    fkdr = safe_div(final_kills, final_deaths)
    wlr = safe_div(wins, losses)
    bblr = safe_div(beds_broken, beds_lost)

    fkdr_color = get_ratio_color(fkdr, 'FKDR')
    wlr_color = get_ratio_color(wlr, 'WL')
    bblr_color = get_ratio_color(bblr, 'BBL')

    fkdr_display = "∞" if math.isinf(fkdr) else fkdr
    wlr_display = "∞" if math.isinf(wlr) else wlr
    bblr_display = "∞" if math.isinf(bblr) else bblr

    level_str = f"[{stars}☆]"
    level_col = f"{level_str:<8}"
    id_col = f"{color}{display_name:<18}{RESET}"
    fkdr_col = f"{fkdr_color}{fkdr_display:^8}{RESET}"
    wlr_col = f"{wlr_color}{wlr_display:^8}{RESET}"
    bblr_col = f"{bblr_color}{bblr_display:^8}{RESET}"

    # 清理临时文件
    if os.path.exists(filename):
        os.remove(filename)

    return f"{level_col}{id_col}{fkdr_col}{wlr_col}{bblr_col}"

# ==============================================
# 6. 批量查询玩家（多线程并发，按顺序输出）
# ==============================================
def query_players(api_key, player_ids):
    if not player_ids:
        return

    print(f"🔍 正在查询 {len(player_ids)} 个玩家...")
    print("\n等级      ID                FKDR     W/L    BB/L")
    print("-" * 50)

    # 使用线程池并发查询
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有任务，保存 future 与原始索引的映射
        future_to_index = {executor.submit(query_player, api_key, pid): idx for idx, pid in enumerate(player_ids)}
        results = [None] * len(player_ids)

        # 收集结果（按完成顺序，但我们会根据索引填充）
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                # 如果异常，放入错误信息
                results[idx] = f"[????]  {player_ids[idx]:<18}  查询异常       ".center(8) + " " * 8 + " " * 8

    # 按顺序打印结果
    for row in results:
        if row:
            print(row)

    print(f"✅ 所有玩家查询完成。")

# ==============================================
# 7. 自动监控线程函数
# ==============================================
stop_monitor = threading.Event()

def auto_monitor(api_key, log_path):
    print(f"📂 后台监控已启动: {log_path}")
    pos = 0
    if os.path.exists(log_path):
        pos = os.path.getsize(log_path)

    while not stop_monitor.is_set():
        time.sleep(0.5)
        if not os.path.exists(log_path):
            continue
        current_size = os.path.getsize(log_path)
        if current_size <= pos:
            continue
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(pos)
                new_text = f.read()
                pos = f.tell()
        except Exception:
            continue

        lines = new_text.splitlines()
        for line in lines:
            if "[CHAT] ONLINE:" in line:
                parts = line.split("[CHAT] ONLINE:", 1)
                if len(parts) == 2:
                    name_str = parts[1].strip()
                    if name_str:
                        player_ids = [p.strip() for p in name_str.replace('，', ',').split(',') if p.strip()]
                        if player_ids:
                            query_players(api_key, player_ids)

# ==============================================
# 8. 主程序
# ==============================================
def main():
    print("=== ⚔️ Hypixel Bedwars 查询器 v1.0.0（by Rancy） ===\n")

    api_key = input("👉 请输入Hypixel API密钥: ").strip()
    if not api_key:
        print("❌ 密钥不能为空！")
        return

    # 选择启动器类型
    print("\n请选择你的启动器类型:")
    print("  pojav  -> PojavLauncher")
    print("  zl1    -> ZalithLauncher")
    print("  其它   -> 自定义路径")
    launcher = input("👉 请输入启动器名称 (pojav/zl1/其它): ").strip().lower()

    if launcher == "pojav":
        log_path = "/storage/emulated/0/Android/data/net.kdt.pojavlaunch.debug/files/latestlog.txt"
    elif launcher == "zl1":
        log_path = "/storage/emulated/0/Android/data/com.movtery.zalithlauncher/files/latestlog.txt"
    else:
        log_path = input("👉 请输入日志文件的完整路径: ").strip()
        if not log_path:
            print("❌ 路径不能为空！使用默认路径（pojav）")
            log_path = "/storage/emulated/0/Android/data/net.kdt.pojavlaunch.debug/files/latestlog.txt"

    print(f"📄 日志文件路径: {log_path}")

    # 启动后台监控线程
    monitor_thread = threading.Thread(target=auto_monitor, args=(api_key, log_path), daemon=True)
    monitor_thread.start()
    print("💡 后台监控已开启，检测到 [CHAT] ONLINE: 将自动查询。")
    print("💡 您可以随时手动输入玩家ID进行查询。")

    while True:
        print("\n" + "-"*40)
        player_input = input("👉 请输入玩家ID (多个用逗号分隔，直接回车退出): ").strip()
        if not player_input:
            stop_monitor.set()
            monitor_thread.join(timeout=1)
            print("👋 已退出查询。")
            break

        player_ids = [p.strip() for p in player_input.replace('，', ',').split(',') if p.strip()]
        if not player_ids:
            print("⚠️ 未输入有效玩家ID，请重新输入。")
            continue

        query_players(api_key, player_ids)

    print("\n程序结束。")

if __name__ == "__main__":
    main()