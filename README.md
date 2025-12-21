# Biomechanical Climbing Coach 🧗‍♂️
Video → Pose + Holds + Contacts → Movement Metrics → Coaching Feedback

Biomechanical Climbing Coach analyzes a climbing video and produces:
- an **annotated replay** (skeleton, holds, contact points, angles), and
- a **movement efficiency report** (thrash, straight-arm usage, cut-feet events, pauses, etc.)

This project is built around a practical goal:
> Identify inefficient movement patterns (e.g., over-pulling, hips drifting out, excessive regripping) and turn them into actionable coaching cues.

## What this is (and isn't)
✅ Great at:
- pose tracking (2D + model-estimated 3D)
- joint angles, velocities, movement economy
- contact inference (hand/foot → hold) with simple heuristics
- generating "top moments" with suggested corrections

⚠️ Not (yet) a biomechanics lab:
- It does **not** compute exact joint torques/forces from a single RGB video.
- Instead, it computes **relative efficiency indices** and flags high-cost patterns.

## MVP Features
- MediaPipe pose extraction on video
- Manual or simple hold detection (MVP uses manual hold labeling)
- Contact inference (hands/feet “on hold” segments)
- Kinematics: angles + velocities + path length + pauses
- Event detection: cut-feet, thrashing, regrip spam (heuristics)
- Outputs:
  - `annotated.mp4`
  - `report.json`
  - `report.html`

## Pipeline (high level)
1. **Ingest video** (frames + timestamps)
2. **Pose estimation** (landmarks per frame)
3. **Wall/holds** (manual labeling for MVP)
4. **Contact inference** (closest hold + stability thresholds)
5. **Metrics & events** (angles, thrash, economy, cut-feet)
6. **Coaching layer** (top moments + suggestions)
7. **Render & export** (annotated video + report)

## Installation
### Requirements
- Python 3.10+ recommended
- Works best with tripod footage (stable camera) for MVP

### Setup
```bash
git clone <your-repo-url>
cd climbbiomech-coach
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### Quickstart (MVP)
1) Add a video

Put a test video in:

examples/input/video.mp4

2) Label holds (MVP)

Extract a wall frame and label holds:

```bash
python -m climbbiomech.cli extract-frame examples/input/video.mp4 --out examples/wall.jpg --time 3.0
python -m climbbiomech.cli label-holds examples/wall.jpg --out examples/holds.json
```

3) Run analysis

```bash
python -m climbbiomech.cli analyze \
  --video examples/input/video.mp4 \
  --holds examples/holds.json \
  --outdir outputs/session_001
```

### Outputs

outputs/session_001/annotated.mp4
outputs/session_001/report.json
outputs/session_001/report.html

### CLI Commands

extract-frame: save a frame from a video (used for labeling holds)
label-holds: interactive hold labeling tool (click holds; saves JSON)
analyze: full pipeline run
render: re-render overlays from stored JSON (no reprocessing)
compare (later): compare two attempts on same problem

### Report Metrics (MVP)

Time on wall
Vertical gain / progress
Path length (hips)
Movement economy (gain / path length)
Straight-arm usage (per arm) during contact
Thrash index (end-effector motion not yielding progress)
Cut-feet events (foot contact loss + hip velocity spike)
Pause/rest segments

### Limitations (MVP)

Assumes a single climber is visible
Hold detection is manual (for now)
“3D” landmarks are model-estimated; treat as relative
Camera angle changes can reduce accuracy











