import time
import base64
import sys
import os
import json
from dotenv import load_dotenv
from volcengine.visual.VisualService import VisualService

load_dotenv()

# ========== 配置 ==========
AK = os.environ.get("VOLC_ACCESS_KEY", "your-access-key-here")
SK = os.environ.get("VOLC_SECRET_KEY", "your-secret-key-here")

STORYBOARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storyboard")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 初始化 ==========
visual_service = VisualService()
visual_service.set_ak(AK)
visual_service.set_sk(SK)

# ========== 邵氏风格前缀 ==========
# Customize this style prefix for your project
STYLE = (
    "Classic 1970s Hong Kong wuxia film, "
    "shot on Eastmancolor film stock, anamorphic widescreen 2.35:1, "
    "high saturation oil painting texture with vivid red green blue, "
    "visible film grain and dust scratches, "
    "warm practical lighting with deep shadows, "
    "no horizontal anamorphic lens flare streaks. "
    "IMPORTANT: absolutely no text, no letters, no Chinese characters, "
    "no subtitles, no watermarks, no writing of any kind in the image. "
)

# ========== 示例镜头定义 ==========
# Replace these with your own storyboard shots.
# Each shot needs: id, name, image (storyboard path), frames, prompt.
SHOTS = [
    {
        "id": "S01",
        "name": "Master Meditating",
        "image": f"{STORYBOARD_DIR}/S01_master.png",
        "frames": 121,
        "prompt": STYLE + (
            "Interior of a traditional Chinese martial arts hall at night. "
            "An elderly master in grey robes with long white beard sits cross-legged "
            "on a raised platform, eyes half-closed in meditation. "
            "Dozens of red candles flicker around him, casting warm dancing shadows "
            "on carved wooden walls. Red lanterns hang from ceiling beams. "
            "Camera slowly dollies forward toward the master's weathered face. "
            "The atmosphere is peaceful but ominous, calm before the storm."
        ),
    },
    {
        "id": "S02",
        "name": "Villain Entrance",
        "image": f"{STORYBOARD_DIR}/S02_villain.png",
        "frames": 121,
        "prompt": STYLE + (
            "Exterior moonlit courtyard of a Chinese manor at night. "
            "A menacing villain in all-black traditional Chinese robes, "
            "with a prominent scar across his left cheek, strong jawline, "
            "cold piercing eyes, walks slowly toward camera holding a broad dao saber. "
            "Moonlight reflects off the blade with a cold blue gleam. "
            "His black robes billow slightly in the night wind. "
            "He smirks with cruel confidence. "
            "Camera at low angle, slowly tracking backward as he advances. "
            "Deep blue moonlight contrasts with warm interior light behind him."
        ),
    },
    {
        "id": "S03",
        "name": "Witness",
        "image": f"{STORYBOARD_DIR}/S03_witness.png",
        "frames": 241,
        "prompt": STYLE + (
            "Split dramatic composition inside a candlelit hall. "
            "Background: the villain in black robes raises his dao saber high "
            "and strikes down at the old master in grey, a violent decisive blow, "
            "the master collapses. Red candles topple and scatter. "
            "Foreground right: a young Asian man with glasses "
            "hides behind an ornate wooden pillar, gripping it with white knuckles, "
            "trembling violently, tears streaming down his face, "
            "one hand pressed over his mouth to stifle a scream. "
            "Camera starts wide then SUDDEN FAST ZOOM into extreme close-up "
            "of the young man's terrified eyes reflecting candlelight."
        ),
    },
    {
        "id": "S04",
        "name": "Training in Rain",
        "image": f"{STORYBOARD_DIR}/S04_training.png",
        "frames": 241,
        "prompt": STYLE + (
            "Exterior mountain cliff in torrential rain, dramatic storm lighting. "
            "A young swordsman in soaking wet white robes "
            "practices intense sword techniques with a jian sword. "
            "He performs rapid consecutive slashes, thrusts, and sweeping arcs. "
            "Rainwater sprays off the blade in slow motion arcs. "
            "His white robes cling to his body, hair wild and drenched. "
            "Each strike carries fury and determination. "
            "Camera circles around him in a dynamic tracking shot. "
            "Lightning flashes illuminate the mountain peaks behind him."
        ),
    },
    {
        "id": "S05",
        "name": "Standoff",
        "image": f"{STORYBOARD_DIR}/S05_standoff.png",
        "frames": 241,
        "prompt": STYLE + (
            "Exterior dusty desert courtyard among ancient red sandstone ruins. "
            "Two martial artists face each other ten paces apart in a tense standoff. "
            "Left: swordsman in white robes holding a jian sword, calm determined expression. "
            "Right: villain in black robes with scarred face holding a dao saber, arrogant smirk. "
            "Strong wind blows sand and dust between them in swirling patterns. "
            "Their robes and hair whip in the wind. "
            "They slowly sidestep in a circle, sizing each other up. "
            "Camera starts as wide establishing shot, "
            "then SUDDEN FAST ZOOM alternating between their faces."
        ),
    },
    {
        "id": "S06",
        "name": "Intense Combat",
        "image": f"{STORYBOARD_DIR}/S06_combat.png",
        "frames": 241,
        "prompt": STYLE + (
            "Intense close-quarters combat in front of a Chinese temple. "
            "The swordsman in white and the saber fighter in black "
            "exchange rapid blows in fluid martial arts choreography. "
            "Bright orange sparks explode where blades clash. "
            "The black-robed villain swings his heavy dao in wide powerful arcs. "
            "The white-robed hero evades with agile footwork and counters with precise thrusts. "
            "Dust and debris fill the air. Stone lion statues in background. "
            "Dynamic tracking camera follows the action. "
            "Red temple pillars, green roof tiles, vivid orange sparks."
        ),
    },
    {
        "id": "S07",
        "name": "Final Strike",
        "image": f"{STORYBOARD_DIR}/S07_final_strike.png",
        "frames": 121,
        "prompt": STYLE + (
            "The climactic final strike of the duel. "
            "The swordsman in white surges forward with explosive speed, "
            "thrusting his jian sword in one decisive lunge. "
            "The villain's dao saber flies from his hand spinning through the air. "
            "The villain staggers backward and collapses to his knees in the dust, defeated. "
            "Dust particles float in golden sunlight around them. "
            "Low angle shot looking up at the hero standing over the fallen villain. "
            "SUDDEN FAST ZOOM into the hero's eyes, cold and resolute, no joy."
        ),
    },
    {
        "id": "S08",
        "name": "Walking Away",
        "image": f"{STORYBOARD_DIR}/S08_walking_away.png",
        "frames": 241,
        "prompt": STYLE + (
            "Exterior vast desolate landscape at golden hour sunset. "
            "A lone swordsman in blood-stained white robes walks away from camera "
            "into the endless horizon, completely alone. "
            "His right hand drags his jian sword on the ground, "
            "leaving a thin trail line in the dirt behind him. "
            "Dead barren trees silhouetted against a deep vivid red-orange sunset sky. "
            "His figure grows smaller and smaller as he walks further away. "
            "The camera is fixed in a wide cinematic shot, perfectly still. "
            "The image gradually darkens at the edges, vignetting into black."
        ),
    },
]


# ========== 工具函数 ==========
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def submit_shot(shot):
    """提交单个镜头任务"""
    img_b64 = image_to_base64(shot["image"])
    form = {
        "req_key": "jimeng_ti2v_v30_pro",
        "binary_data_base64": [img_b64],
        "prompt": shot["prompt"],
        "frames": shot["frames"],
        "aspect_ratio": "16:9",
    }
    try:
        resp = visual_service.cv_sync2async_submit_task(form)
        return resp
    except Exception as e:
        error_msg = str(e)
        if "Access Denied" in error_msg:
            return {"code": 50400, "message": "Access Denied: 请先在火山引擎控制台开通「即梦AI视频生成3.0 Pro」服务"}
        return {"code": -1, "message": error_msg}


def query_result(task_id):
    """查询任务结果"""
    form = {
        "req_key": "jimeng_ti2v_v30_pro",
        "task_id": task_id,
    }
    return visual_service.cv_sync2async_get_result(form)


# ========== 主流程（并发控制：每批2个）==========
BATCH_SIZE = 2

def wait_for_tasks(tasks_batch):
    """轮询等待一批任务完成，返回 (completed, failed)"""
    completed = {}
    failed = set()
    while len(completed) + len(failed) < len(tasks_batch):
        time.sleep(15)
        print(f"\n--- 轮询中 ({len(completed)}/{len(tasks_batch)} 完成) ---")
        for sid, info in tasks_batch.items():
            if sid in completed or sid in failed:
                continue
            try:
                result = query_result(info["task_id"])
            except Exception as e:
                print(f"  [{sid}] 查询异常: {e}")
                continue
            status = result.get("data", {}).get("status", "unknown")
            print(f"  [{sid}] {info['shot']['name']}: {status}")
            if status == "done":
                if result.get("code") == 10000:
                    video_url = result["data"]["video_url"]
                    completed[sid] = video_url
                    url_file = f"{OUTPUT_DIR}/{sid}_video_url.txt"
                    with open(url_file, "w") as f:
                        f.write(video_url)
                    # 立即下载
                    mp4_file = f"{OUTPUT_DIR}/{sid}.mp4"
                    print(f"    生成成功！下载中...")
                    import subprocess
                    subprocess.run(["curl", "-s", "-o", mp4_file, video_url])
                    print(f"    已保存: {mp4_file}")
                else:
                    failed.add(sid)
                    print(f"    生成失败: {result.get('message')}")
            elif status in ("not_found", "expired"):
                failed.add(sid)
                print(f"    任务异常: {status}")
    return completed, failed


if __name__ == "__main__":
    target_ids = sys.argv[1:] if len(sys.argv) > 1 else [s["id"] for s in SHOTS]
    shots_to_run = [s for s in SHOTS if s["id"] in target_ids]

    print(f"即梦视频生成 — 共 {len(shots_to_run)} 个镜头（每批 {BATCH_SIZE} 个）")
    print("=" * 50)

    all_completed = {}
    all_failed = set()

    # 分批提交
    for i in range(0, len(shots_to_run), BATCH_SIZE):
        batch = shots_to_run[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"\n{'='*50}")
        print(f"第 {batch_num} 批（{len(batch)} 个镜头）")

        tasks_batch = {}
        for shot in batch:
            duration = "10秒" if shot["frames"] == 241 else "5秒"
            print(f"\n[{shot['id']}] {shot['name']} ({duration})")
            print(f"  提交中...")

            resp = submit_shot(shot)
            if resp.get("code") == 10000:
                tid = resp["data"]["task_id"]
                tasks_batch[shot["id"]] = {"task_id": tid, "shot": shot}
                print(f"  任务ID: {tid}")
            else:
                all_failed.add(shot["id"])
                print(f"  提交失败: {resp.get('message')}")

        if tasks_batch:
            completed, failed = wait_for_tasks(tasks_batch)
            all_completed.update(completed)
            all_failed.update(failed)

    # 汇总
    print(f"\n{'=' * 50}")
    print("全部完成！")
    print(f"  成功: {len(all_completed)} 个")
    print(f"  失败: {len(all_failed)} 个")
    if all_failed:
        print(f"  失败镜头: {', '.join(sorted(all_failed))}")
    print(f"\n视频保存在: {OUTPUT_DIR}/")
    if all_completed:
        print("\n已下载文件:")
        for sid in sorted(all_completed):
            print(f"  {OUTPUT_DIR}/{sid}.mp4")
