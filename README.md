# Synthesia Splitter

Simple python script to convert "Synthesia" videos, like from [Sheet Music Boss](https://www.youtube.com/@SheetMusicBoss) youtube channel, into an arrangement of images. This allows reading the video like a sheet music, especially when displayed on a tablet.

## Usage

### Prerequisites

- Python
- Packages: opencv-python, numpy, tkinter (Tk is usually included on Windows)
- Install with:

```python
pip install opencv-python numpy
```

### Run

From a terminal (or VS Code terminal) in the project folder:

```python
python capture.py
```

A file dialog opens — select the video file (.mp4, .avi, .mkv, .mov).

### Interactive preview & controls

The programm is not fully automatic, it does not know when to take a screenshot of the video.  
So, we will select the two first frames that will be captured.  
The second one must be very close to what should be the next image after the first one. Because, from the interval between thoses two, all the frames will be taken.  
And if there is a missing space/note between the first frames, there will be missing spaces/notes between all the frames.

i0 and i1 define the sampling interval: step = i1 - i0.

- w - cancel and exit
- a - move i0 (first frame index) left by 1
- z - move i0 right by 1
- r - move i0 left by 10
- t - move i0 right by 10
- q - move i1 (second frame index) left by 1
- s - move i1 right by 1
- f - move i1 left by 10
- g - move i1 right by 10
- e - move crop line (y_barre) up by 10 px
- d - move crop line (y_barre) down by 10 px
- y - decrease preview reduction (zoom in)
- h - increase preview reduction (zoom out)
- x - validate selection and start processing

Notes:
- Keys can be changed in the script
- y_barre is the horizontal crop line; frames are cropped to frame[:y_barre, :]. To remove partially the keys
- Pressing x closes the preview windows and continues.

### Output

- Output folder: "Photos Output" (created if missing) in the script working directory.
- Saved files: capture_000.jpg, capture_001.jpg, ...
- Default layout parameters used in the script: 3 frames stacked vertically per column and up to 5 columns horizontally (adjust in code by changing frames_layout call).

### Behavior & troubleshooting
- If the video cannot be opened, check codecs and file path.
- If the selection is cancelled (press w), no images will be produced.
- If interval (i1 - i0) ≤ 0 processing is skipped.
- To change layout or output folder, edit the main block in capture.py:
    - frames_layout(trimmed_frames, nb_vertical, nb_horizontal)
    - output_folder variable

## Example

### Video demonstration

![Demo](/Example/DemoSynthesiaSplitter.avif)

### Results

The first image generated :  

![ExampleResult](/Example/Relic%20(Minecraft%20Music%20Disc)%20-%20Piano%20Tutorial/capture_000.jpg)

Full results can be found [here](https://github.com/romaingallo/Synthesia-Splitter/tree/main/Example).