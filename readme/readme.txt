================================================
 DTMF_GEN - DTMF (Touch-Tone) WAV Generator
================================================
Author:   Igor Brzezek
Email:    igor.brzezek@gmail.com
GitHub:   https://github.com/IgorBrzezek
Version:  1.1.0 (17.12.2025)

1. DESCRIPTION
------------------------------------------------
DTMF_GEN is a specialized audio utility designed to generate Dual-Tone 
Multi-Frequency (DTMF) signals, commonly known as "touch-tones" used in 
telephony. The script generates high-quality 16-bit WAV files by 
combining low-group and high-group frequencies for each digit.

It supports all standard DTMF characters: 0-9, *, #, and A-D.

2. KEY FEATURES
------------------------------------------------
- Standard DTMF Mapping: Accurate frequency generation according to ITU 
  telephony standards.
- Custom Timing: Independent control over tone duration and silence 
  gaps between digits.
- Batch Processing: Use a CSV-style list to generate multiple dialing 
  sequences automatically.
- Overwrite Protection: Integrated safety check to prevent accidental 
  deletion of existing files.

3. OPTIONS AND ARGUMENTS
------------------------------------------------
-h                      Show a short usage summary.
--help                  Show full documentation and usage examples.
-DIAL SEQUENCE          The digits to generate (e.g., 1,2,3 or 060123456).
-o, --output NAME       Filename for the generated WAV (default: dialed.wav).
-t, --tone TIME         Duration of each tone in seconds (default: 0.2).
-s, --silence TIME      Duration of silence between tones (default: 0.1).
--freq Hz               Sampling rate in Hz (default: 44100).
--overwrite             Force overwrite of existing files without asking.
--list FILE             Path to a CSV file for batch generation.

4. BATCH PROCESSING (--list)
------------------------------------------------
The batch list should be a plain text file where each line follows this format:
filename, NUMBER, tone_duration, silence_duration

Example list file content (dtmf_list.txt):
------------------------------------------------
emergency.wav, 911, 0.5, 0.2
office.wav, 101, 0.2, 0.1
test_seq.wav, 123456789, 0.1, 0.05
------------------------------------------------

5. USAGE EXAMPLES
------------------------------------------------
- Generate a standard dial sequence for "147":
  python dtmf_gen.py -DIAL 1,4,7 -o test.wav

- Generate a phone number with slower dialing speed:
  python dtmf_gen.py -DIAL 5551234 -t 0.4 -s 0.3 --overwrite

- Generate special characters (A-D, *, #):
  python dtmf_gen.py -DIAL *,#,A,B,C,D -o symbols.wav

- Run batch generation from a file:
  python dtmf_gen.py --list my_calls.csv --overwrite

6. DTMF FREQUENCY REFERENCE
------------------------------------------------
Each key is a combination of two frequencies:
          1209 Hz  1336 Hz  1477 Hz  1633 Hz
697 Hz      [1]      [2]      [3]      [A]
770 Hz      [4]      [5]      [6]      [B]
852 Hz      [7]      [8]      [9]      [C]
941 Hz      [*]      [0]      [#]      [D]

================================================
