from fastapi import APIRouter
from ai_vision.pipeline import VisionPipeline
from backend.services.traffic_service import master_traffic_service
from backend.config import settings

router = APIRouter(prefix="/detection", tags=["AI Vision Pipeline"])

pipeline_instance = None

def get_pipeline():
    global pipeline_instance
    if pipeline_instance is None:
        pipeline_instance = VisionPipeline(video_source=settings.SAMPLE_VIDEO_PATH)
    return pipeline_instance

@router.get("/status")
def get_detection_status():
    pipe = get_pipeline()
    return {
        "video_source": pipe.video_processor.source,
        "is_opened": pipe.video_processor.is_opened,
        "total_frames": pipe.video_processor.total_frames,
        "model_backend": pipe.model_loader.backend,
        "total_unique_vehicles": pipe.counter.total_unique_vehicles
    }

@router.post("/process-frame")
def trigger_process_frame():
    pipe = get_pipeline()
    signal_states = master_traffic_service.signal_engine.current_signal_states
    vision_result = pipe.process_next_frame(signal_states=signal_states)
    if vision_result:
        master_traffic_service.process_vision_payload(vision_result)
    return vision_result or {"status": "NO_FRAME_OR_EOF"}
