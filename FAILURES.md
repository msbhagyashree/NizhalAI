# Failures we found and fixed

## Windows starter-kit compatibility (2 Nov 2026)
- What broke: NizhalAI test cases without temperature fields caused `cases show` to crash. BOM-formatted JSON caused parsing errors, and Chromium output caused a Windows UnicodeDecodeError.
- How we found it: Running the case-check, case-display and video-generation commands.
- What we changed: Updated `ship_kit/cases.py`, `ship_kit/cli.py` and `ship_kit/video.py` to handle NizhalAI cases, UTF-8 BOM files and Windows subprocess encoding.
- After: All five cases displayed correctly, Python syntax checks passed, and a 34.6-second demo video was generated. Agent-quality remeasurement is still pending; no quality improvement is claimed.
