# A-Level Business Explained: video pipeline notes

Two videos per day. Both are 1080x1920, 30 fps, built with PIL frames piped to ffmpeg.

- `video_a_1min/` : Taylor vs Mayo (hook, concept columns, mnemonic box, question + 3-2-1 countdown, answer, "Comment MOCK" CTA). ~57 s.
- `video_b_quickhit/` : Pay or praise (hook, two columns, exam-trick box, follow CTA). ~32 s.
Copy a folder, edit `tl.py` (voice-line durations), `render.py` (board() content + CAPS captions), `audio.py` (number of voice files), then run:
`python3 tl.py && python3 audio.py && ffmpeg -y -i final_raw.wav -af "volume=-2.5dB,alimiter=limit=0.85" final_audio.wav && python3 render.py check && python3 render.py render`
Needs `vo/l1.wav ... lN.wav` in the folder (one per scene).

## Voice
Speko `audio_synthesize`, Cartesia voice `a5136bf9-224c-4d76-b823-52bd5efcffcc` (Jameson, American male), language en-US, constraints.allowedProviders.tts ["cartesia"]. The result is saved to a file: `jq -r .audio_base64 FILE | base64 -d > vo/lN.wav`.

## TikTok safe zone (hard rule)
Everything drawn must sit inside x 60..920, y 180..1380. The board is drawn on a virtual 1000x1250 canvas, scaled 0.84, pasted at (70,190). Captions are 58 px, max text width 740, at y=1262. `python3 render.py check` must print `violations 0` before delivering. Do not put anything in the top 150 px, the bottom 450 px, or the right 150 px.

## Hooks (every video, first 3 seconds)
Visual text on screen from frame 0 plus a spoken hook. Formats: "X isn't as hard as they make it seem", "POV: the exam asks X", "This one mistake costs marks". Keep video A about 1 minute and video B 20-30 s.

## Quality bar
Loudness about -15 LUFS, true peak below -0.5 dBFS. Review sample frames (use `sheet.py out.png t1 t2 ...`, it shades the TikTok UI zones) and fix any overlap or cut-off text before delivering. Facts must match Edexcel 9BS0. No copied Pearson text.

## Publishing
1. Save the MP4 in `videos/dayNN-topic.mp4` in this repo and push to main.
2. Create a Metricool DRAFT (draft:true) for brand blogId 7675872, networks tiktok + instagram (Reel, isAiGenerated true, tiktok isAigc true, tiktok title required), media = `https://raw.githubusercontent.com/ahmedidrees21-alt/alevel-videos/main/videos/<file>.mp4`, timezone Europe/London. Slots: video A 12:30, video B 18:00. Caption + 10 hashtags (#alevelbusiness #edexcelbusiness #alevels #businessstudies #studytok #revision #alevelrevision #ukstudent + 2 topic tags) and a CTA to comment MOCK.
3. Never publish without approval: keep drafts.
4. Append the day to `pipeline/progress.md`.

## Cover image (important)
The first frame is blank because text types in. Always set `videoCoverMilliseconds` on the Metricool post to a moment when the hook is fully on screen and no caption pill covers it (video A: 4000, video B: 3500; for new videos pick the time the hook text finishes typing and check that frame with render.py prev). Instagram applies it. TikTok may ignore it on personal accounts, so Ahmed may need to pick the cover in TikTok.
