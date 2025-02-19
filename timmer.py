import ffmpeg
import os

def trim_video(input_path, output_folder, timestamps):
    """
    Trim a video based on given timestamps using ffmpeg.
    
    :param input_path: Path to the input video file.
    :param output_folder: Folder to save trimmed video clips.
    :param timestamps: List of tuples with (start_time, end_time) in seconds.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    for i, (start, end) in enumerate(timestamps):
        output_path = os.path.join(output_folder, f"trimmed_{i+1}.mp4")
        
        (
            ffmpeg
            .input(input_path, ss=start, to=end)
            .output(output_path, c="copy")  # Copy codec to avoid re-encoding
            .run(overwrite_output=True)
        )

# Example usage
if __name__ == "__main__":
    input_video = "./input.mp4"  # Change this to your actual video file
    output_dir = "trimmed_videos"
    trim_timestamps = [(240, 250)]  # Trim from 4 to 5 minutes

    trim_video(input_video, output_dir, trim_timestamps)
    print("Trimming completed!")
