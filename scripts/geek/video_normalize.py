import os

from ffmpeg_normalize import FFmpegNormalize


def normalize_video(input_path, output_path=None, audio_codec='aac'):
    if output_path is None:
        # 获取输入文件的目录和文件名，然后添加 _normalized 后缀
        file_dir, file_name = os.path.split(input_path)
        file_root, file_ext = os.path.splitext(file_name)
        output_path = os.path.join(file_dir, f"{file_root}_normalized{file_ext}")

    norm = FFmpegNormalize(audio_codec=audio_codec, progress=True)
    norm.add_media_file(input_path, output_path)
    norm.run_normalization()
    print(f"output_path :{output_path}")


if __name__ == '__main__':
    # input_file = "/Users/xuxin14/Downloads/IMG_0992.mp4"
    input_file = "/Users/xuxin14/Downloads/v.f1093816-converted.mp4"
    # output_file = "/Users/xuxin14/Downloads/IMG_0992_normal.mp4"

    # 仅提供输入路径，输出路径将自动生成
    normalize_video(input_file)
