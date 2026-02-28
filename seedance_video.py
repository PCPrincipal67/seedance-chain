"""
Seedance Video Generator — Ark API
===================================
支持 Seedance 1.5 Pro / 1.0 Pro / 1.0 Pro Fast / 1.0 Lite

能力矩阵:
  1.5 Pro:  文生视频 | 图生视频(首帧/首尾帧) | 音频生成 | 草稿预览 | 末帧返回
  1.0 Fast: 文生视频 | 图生视频(首帧/首尾帧) | 参考图(1-4张) | 末帧返回
  1.0 Pro:  文生视频 | 图生视频(首帧/首尾帧) | 末帧返回
  1.0 Lite: 图生视频(i2v) 或 文生视频(t2v)

用法:
  python seedance_video.py                    # 生成全部镜头
  python seedance_video.py S01 S03            # 生成指定镜头
  python seedance_video.py --draft S01        # 草稿快速预览
  python seedance_video.py --chain            # 续拍模式(自动首尾帧衔接)
  python seedance_video.py --chain --draft    # 续拍+草稿
"""

import argparse
import base64
import mimetypes
import os
import subprocess
import sys
import time

from volcenginesdkarkruntime import Ark

# ========== 配置 ==========
ARK_API_KEY = os.environ.get("VOLC_ARK_API_KEY", "your-api-key-here")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== 模型 ==========
MODELS = {
    "1.5pro":    "doubao-seedance-1-5-pro-251215",
    "1.0pro":    "doubao-seedance-1-0-pro-250528",
    "1.0fast":   "doubao-seedance-1-0-pro-fast-251015",
    "1.0lite-i": "doubao-seedance-1-0-lite-i2v-250428",
    "1.0lite-t": "doubao-seedance-1-0-lite-t2v-250428",
}

# ========== 初始化 Ark 客户端 ==========
client = Ark(api_key=ARK_API_KEY)

# ========== 镜头定义 ==========
# 示例: 在这里定义你的镜头列表, 每个 shot 是一个 dict
# 所有字段除 id/name/prompt 外均可选, 会使用默认值
#
# 字段说明:
#   id             str   镜头编号 (必填)
#   name           str   镜头名称 (必填)
#   prompt         str   文本描述 (必填)
#   model          str   模型简称: "1.5pro" / "1.0fast" / "1.0pro" 等 (默认 "1.5pro")
#   first_frame    str   首帧图片路径 (可选)
#   last_frame     str   尾帧图片路径 (可选, 仅 1.5pro/1.0pro/1.0fast)
#   ref_images     list  参考图路径列表, 1-4张 (可选, 仅 1.0fast)
#   duration       int   时长秒数 4-12 (默认 5)
#   resolution     str   "480p" / "720p" / "1080p" (默认 "1080p")
#   ratio          str   "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" (默认 "16:9")
#   generate_audio bool  生成音频 (默认 False, 仅 1.5pro)
#   camera_fixed   bool  固定镜头 (默认 False)
#   return_last_frame bool 返回末帧用于续拍 (默认 False)

# ========== 影片风格前缀 ==========
# Customize this style prefix for your project
STYLE = (
    "Cinematic photorealistic scene, dramatic lighting, "
    "film grain, cinematic 2.39:1 framing, "
    "no text no subtitles no watermarks. "
)

# ========== 首帧图 ==========
# Set this to your first-frame image path, or None to skip
S01_FIRST_FRAME = None  # e.g. "assets/first_frame.png"

# ========== 示例镜头定义 ==========
# Replace with your own shot definitions.
# Each shot needs: id, name, prompt. Optional: first_frame, duration, generate_audio, etc.

SHOTS = [
    # ---- S01 Example Shot (12s) ----
    {
        "id": "S01",
        "name": "Opening Scene",
        "first_frame": S01_FIRST_FRAME,
        "duration": 12,
        "generate_audio": True,
        "prompt": STYLE + (
            "A person sits at a table in a dramatic interior setting. "
            "Camera slowly pushes from wide to medium shot. "
            "Ambient: room tone, subtle background sounds."
        ),
    },
    # ---- S02 Example Shot (12s) ----
    {
        "id": "S02",
        "name": "Confrontation",
        "duration": 12,
        "generate_audio": True,
        "prompt": STYLE + (
            "Two people face each other across a table in a tense scene. "
            "Medium shot, stable camera. "
            "Ambient: tense atmosphere sounds."
        ),
    },
]

# ========== 默认值 ==========
DEFAULTS = {
    "model": "1.5pro",
    "duration": 5,
    "resolution": "1080p",
    "ratio": "16:9",
    "generate_audio": False,
    "camera_fixed": False,
    "return_last_frame": False,
}

BATCH_SIZE = 2
POLL_INTERVAL = 15  # 秒


# ========== 工具函数 ==========

def image_to_data_uri(path):
    """将本地图片转为 data URI (data:image/png;base64,...)"""
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def build_content(shot):
    """根据 shot 配置构建 API content 数组"""
    content = []

    # 文本 prompt
    content.append({"type": "text", "text": shot["prompt"]})

    # 首帧图
    if shot.get("first_frame"):
        content.append({
            "type": "image_url",
            "image_url": {"url": image_to_data_uri(shot["first_frame"])},
            "role": "first_frame",
        })

    # 尾帧图
    if shot.get("last_frame"):
        content.append({
            "type": "image_url",
            "image_url": {"url": image_to_data_uri(shot["last_frame"])},
            "role": "last_frame",
        })

    # 参考图 (仅 1.0fast)
    for ref_path in shot.get("ref_images", []):
        content.append({
            "type": "image_url",
            "image_url": {"url": image_to_data_uri(ref_path)},
            "role": "reference_image",
        })

    # 草稿任务引用
    if shot.get("draft_task_id"):
        content.append({
            "type": "draft_task",
            "draft_task": {"id": shot["draft_task_id"]},
        })

    return content


def submit_task(shot, force_draft=False):
    """提交生成任务, 返回 task_id 或 None"""
    model_key = shot.get("model", DEFAULTS["model"])
    model_id = MODELS.get(model_key)
    if not model_id:
        print(f"  [错误] 未知模型: {model_key}")
        return None

    content = build_content(shot)

    kwargs = {
        "model": model_id,
        "content": content,
        "duration": shot.get("duration", DEFAULTS["duration"]),
        "resolution": shot.get("resolution", DEFAULTS["resolution"]),
        "ratio": shot.get("ratio", DEFAULTS["ratio"]),
    }

    # 仅 1.5pro 支持的参数
    if model_key == "1.5pro":
        if shot.get("generate_audio", DEFAULTS["generate_audio"]):
            kwargs["generate_audio"] = True
        if force_draft or shot.get("draft"):
            kwargs["draft"] = True
            kwargs["resolution"] = "480p"  # 草稿仅支持 480p

    # 通用可选参数
    if shot.get("camera_fixed", DEFAULTS["camera_fixed"]):
        kwargs["camera_fixed"] = True
    if shot.get("return_last_frame", DEFAULTS["return_last_frame"]):
        kwargs["return_last_frame"] = True
    if shot.get("seed") is not None:
        kwargs["seed"] = shot["seed"]

    try:
        resp = client.content_generation.tasks.create(**kwargs)
        return resp.id
    except Exception as e:
        print(f"  [错误] 提交失败: {e}")
        return None


def query_task(task_id):
    """查询任务状态, 返回 ContentGenerationTask 对象"""
    return client.content_generation.tasks.get(task_id=task_id)


def download_file(url, path):
    """下载文件到本地"""
    subprocess.run(["curl", "-s", "-o", path, url], check=True)


def wait_for_tasks(tasks_batch):
    """
    轮询等待一批任务完成
    tasks_batch: {shot_id: {"task_id": str, "shot": dict}}
    返回: (completed, failed)
      completed: {shot_id: {"video_url": str, "last_frame_url": str|None}}
      failed: set of shot_ids
    """
    completed = {}
    failed = set()
    total = len(tasks_batch)

    while len(completed) + len(failed) < total:
        time.sleep(POLL_INTERVAL)
        print(f"\n--- 轮询中 ({len(completed)}/{total} 完成) ---")

        for sid, info in tasks_batch.items():
            if sid in completed or sid in failed:
                continue

            try:
                result = query_task(info["task_id"])
            except Exception as e:
                print(f"  [{sid}] 查询异常: {e}")
                continue

            status = result.status
            print(f"  [{sid}] {info['shot']['name']}: {status}")

            if status == "succeeded":
                video_url = result.content.video_url if result.content else None
                last_frame_url = result.content.last_frame_url if result.content else None

                if video_url:
                    completed[sid] = {
                        "video_url": video_url,
                        "last_frame_url": last_frame_url,
                    }

                    # 保存 URL
                    with open(f"{OUTPUT_DIR}/{sid}_video_url.txt", "w") as f:
                        f.write(video_url)
                    if last_frame_url:
                        with open(f"{OUTPUT_DIR}/{sid}_last_frame_url.txt", "w") as f:
                            f.write(last_frame_url)

                    # 下载视频
                    mp4_path = f"{OUTPUT_DIR}/{sid}.mp4"
                    print(f"    下载视频...")
                    download_file(video_url, mp4_path)
                    print(f"    已保存: {mp4_path}")

                    # 下载末帧
                    if last_frame_url:
                        frame_path = f"{OUTPUT_DIR}/{sid}_last_frame.png"
                        download_file(last_frame_url, frame_path)
                        print(f"    末帧已保存: {frame_path}")
                else:
                    failed.add(sid)
                    print(f"    任务完成但无视频URL")

            elif status == "failed":
                failed.add(sid)
                err_msg = result.error.message if result.error else "未知错误"
                err_code = result.error.code if result.error else ""
                print(f"    生成失败: [{err_code}] {err_msg}")

            elif status == "cancelled":
                failed.add(sid)
                print(f"    任务已取消")

    return completed, failed


def concat_videos(shot_ids):
    """用 ffmpeg 将多段视频拼接为完整短片, 重编码 + 去重复帧处理衔接跳帧"""
    # 第一步: 对每段视频裁掉首尾重复帧 (续拍链的尾帧=下段首帧, 会导致衔接处静止/跳帧)
    # 除第一段保留完整外, 后续每段裁掉开头 0.15 秒 (约4-5帧@30fps) 避免重复
    trimmed_dir = f"{OUTPUT_DIR}/_trimmed"
    os.makedirs(trimmed_dir, exist_ok=True)

    list_file = f"{OUTPUT_DIR}/_concat_list.txt"
    with open(list_file, "w") as f:
        for idx, sid in enumerate(shot_ids):
            mp4 = f"{OUTPUT_DIR}/{sid}.mp4"
            if not os.path.exists(mp4):
                continue

            if idx == 0:
                # 第一段: 完整保留
                f.write(f"file '{mp4}'\n")
            else:
                # 后续段: 裁掉开头 0.15s 去重复帧
                trimmed = f"{trimmed_dir}/{sid}_trimmed.mp4"
                subprocess.run(
                    ["ffmpeg", "-y", "-ss", "0.15", "-i", mp4,
                     "-c:v", "libx264", "-c:a", "aac",
                     "-movflags", "+faststart", trimmed],
                    capture_output=True, text=True,
                )
                f.write(f"file '{trimmed}'\n")

    output_path = f"{OUTPUT_DIR}/final_film.mp4"
    print(f"\n拼接中: {len(shot_ids)} 段 → {output_path}")
    print("  (已裁剪衔接处重复帧 0.15s)")

    # 重编码拼接 (避免编码参数不一致导致的跳帧/花屏)
    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-c:v", "libx264", "-c:a", "aac",
         "-movflags", "+faststart", output_path],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"拼接完成: {output_path}")
    else:
        print(f"  拼接失败: {result.stderr[-200:]}")

    # 清理临时文件
    os.remove(list_file)
    import shutil
    shutil.rmtree(trimmed_dir, ignore_errors=True)


# ========== 主流程 ==========

def main():
    parser = argparse.ArgumentParser(description="Seedance 视频生成")
    parser.add_argument("shots", nargs="*", help="要生成的镜头 ID (如 S01 S03), 不指定则全部生成")
    parser.add_argument("--draft", action="store_true", help="草稿快速预览模式 (480p, 仅 1.5pro)")
    parser.add_argument("--chain", action="store_true", help="续拍模式: 自动用前一镜头末帧作为下一镜头首帧")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help=f"每批并发数 (默认 {BATCH_SIZE})")
    parser.add_argument("--no-concat", action="store_true", help="跳过 ffmpeg 拼接")
    args = parser.parse_args()

    if not SHOTS:
        print("SHOTS 列表为空, 请先在脚本中定义镜头。")
        print("参考脚本顶部的示例注释。")
        sys.exit(1)

    # 筛选镜头
    if args.shots:
        shots_to_run = [s for s in SHOTS if s["id"] in args.shots]
        if not shots_to_run:
            print(f"未找到指定镜头: {args.shots}")
            sys.exit(1)
    else:
        shots_to_run = SHOTS[:]

    # 续拍模式: 为每个镜头开启 return_last_frame
    if args.chain:
        for s in shots_to_run:
            s["return_last_frame"] = True

    total = len(shots_to_run)
    batch_size = args.batch_size
    mode_str = []
    if args.draft:
        mode_str.append("草稿预览")
    if args.chain:
        mode_str.append("续拍链")
    mode_label = f" ({' + '.join(mode_str)})" if mode_str else ""

    print(f"Seedance 视频生成{mode_label} — 共 {total} 个镜头 (每批 {batch_size} 个)")
    print("=" * 60)

    all_completed = {}
    all_failed = set()
    prev_last_frame_url = None  # 续拍链: 上一镜头末帧

    # 分批提交
    for i in range(0, total, batch_size):
        batch = shots_to_run[i:i + batch_size]
        batch_num = i // batch_size + 1
        print(f"\n{'=' * 60}")
        print(f"第 {batch_num} 批 ({len(batch)} 个镜头)")

        # 续拍链: 将上一批最后一个镜头的末帧注入到这一批第一个镜头
        if args.chain and prev_last_frame_url and not batch[0].get("first_frame"):
            # 下载末帧到本地, 作为下一个镜头的首帧
            chain_frame_path = f"{OUTPUT_DIR}/_chain_frame_{batch[0]['id']}.png"
            if not os.path.exists(chain_frame_path):
                download_file(prev_last_frame_url, chain_frame_path)
            batch[0]["first_frame"] = chain_frame_path
            print(f"  [续拍] {batch[0]['id']} 使用上一镜头末帧作为首帧")

        tasks_batch = {}
        for shot in batch:
            model_key = shot.get("model", DEFAULTS["model"])
            dur = shot.get("duration", DEFAULTS["duration"])
            print(f"\n[{shot['id']}] {shot['name']} (模型:{model_key}, {dur}秒)")
            print(f"  提交中...")

            task_id = submit_task(shot, force_draft=args.draft)
            if task_id:
                tasks_batch[shot["id"]] = {"task_id": task_id, "shot": shot}
                print(f"  任务ID: {task_id}")
            else:
                all_failed.add(shot["id"])
                print(f"  提交失败")

        if tasks_batch:
            completed, failed = wait_for_tasks(tasks_batch)
            all_completed.update(completed)
            all_failed.update(failed)

            # 续拍链: 记录这一批最后一个完成的镜头末帧
            if args.chain:
                last_sid = batch[-1]["id"]
                if last_sid in completed and completed[last_sid].get("last_frame_url"):
                    prev_last_frame_url = completed[last_sid]["last_frame_url"]

    # 汇总
    print(f"\n{'=' * 60}")
    print("全部完成!")
    print(f"  成功: {len(all_completed)} 个")
    print(f"  失败: {len(all_failed)} 个")
    if all_failed:
        print(f"  失败镜头: {', '.join(sorted(all_failed))}")
    print(f"\n输出目录: {OUTPUT_DIR}/")
    if all_completed:
        print("\n已下载文件:")
        for sid in sorted(all_completed):
            print(f"  {OUTPUT_DIR}/{sid}.mp4")
            if all_completed[sid].get("last_frame_url"):
                print(f"  {OUTPUT_DIR}/{sid}_last_frame.png")

    # ffmpeg 拼接
    if len(all_completed) > 1 and not args.no_concat:
        concat_videos(sorted(all_completed.keys()))


if __name__ == "__main__":
    main()
