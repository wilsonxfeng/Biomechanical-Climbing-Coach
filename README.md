# Biomechanical Climbing Coach 🧗‍♂️
Video → Pose + Holds + Contacts → Movement Metrics → Coaching Feedback

ClimbBiomech Coach analyzes a climbing video and produces:
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
