import os
import sys
import time
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_vision.pipeline import VisionPipeline
from backend.services.traffic_service import master_traffic_service

def run_video_pipeline(video_path: str = "./data/videos/sample_traffic_640x480.mp4", max_frames: int = 50):
    print("=" * 70)
    print(f"Running Full AI Traffic Pipeline on: {video_path}")
    print("=" * 70)

    pipeline = VisionPipeline(video_source=video_path)
    print(f"Video Opened: {pipeline.video_processor.is_opened}, Frames: {pipeline.video_processor.total_frames}")
    print(f"Model Backend: {pipeline.model_loader.backend}")

    for idx, frame, meta in pipeline.video_processor.frame_generator(max_frames=max_frames):
        t0 = time.time()
        signal_states = master_traffic_service.signal_engine.current_signal_states
        vision_res = pipeline.process_frame(frame, meta, signal_states=signal_states)
        traffic_res = master_traffic_service.process_vision_payload(vision_res)
        elapsed_ms = (time.time() - t0) * 1000

        if idx % 5 == 0:
            print(f"Frame [{meta['frame_idx']:03d}] | Active Veh: {vision_res['active_vehicle_count']:2d} | "
                  f"Total Unique: {vision_res['total_unique_count']:2d} | "
                  f"Congestion: {traffic_res['traffic']['overall_congestion']:8s} | "
                  f"Active Green: {traffic_res['signals']['active_green_lane']:11s} | "
                  f"Latency: {elapsed_ms:5.1f}ms")

    print("\nPipeline execution completed successfully!")

if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "./data/videos/sample_traffic_640x480.mp4"
    run_video_pipeline(video)
