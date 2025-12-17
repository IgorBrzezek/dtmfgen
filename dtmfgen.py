import wave
import math
import struct
import argparse
import os
import sys
import time

_VERSION_ = "1.1.0"
_DATE_ = "17.12.2025"
_AUTHOR_ = "Igor Brzezek"
_EMAIL_ = "igor.brzezek@gmail.com"
_GITHUB_ = "https://github.com/IgorBrzezek"

# DTMF Frequency Mapping
DTMF_MAP = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}

def generate_dtmf_file(filename, dial_sequence, tone_dur, silence_dur, sample_rate, overwrite):
    """Generates a single DTMF WAV file."""
    if os.path.exists(filename) and not overwrite:
        print(f"Skipping '{filename}': File exists and --overwrite is off.")
        return

    # Clean sequence
    dial_sequence = dial_sequence.replace(',', '').upper()
    amplitude = 32767  # Max for 16-bit
    start_time = time.time()
    
    all_samples = []

    for i, char in enumerate(dial_sequence):
        if char in DTMF_MAP:
            # Tone generation
            f1, f2 = DTMF_MAP[char]
            num_tone_samples = int(tone_dur * sample_rate)
            for s in range(num_tone_samples):
                t = s / sample_rate
                val = (math.sin(2 * math.pi * f1 * t) + math.sin(2 * math.pi * f2 * t)) / 2
                all_samples.append(int(val * amplitude))
            
            # Silence generation (if not the last digit)
            if i < len(dial_sequence) - 1:
                num_silence_samples = int(silence_dur * sample_rate)
                all_samples.extend([0] * num_silence_samples)

    try:
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            for sample in all_samples:
                wav_file.writeframes(struct.pack('<h', sample))
        
        end_time = time.time()
        gen_duration = end_time - start_time
        file_size_kb = os.path.getsize(filename) / 1024
        
        print(f"File: {filename}, Params: [DTMF, {dial_sequence}, tone: {tone_dur}s, silence: {silence_dur}s], GenTime: {gen_duration:.4f}s, Size: {file_size_kb:.2f} KB")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

def main():
    metadata = (
        f"================================================\n"
        f" AUTHOR:   {_AUTHOR_}\n"
        f" EMAIL:    {_EMAIL_}\n"
        f" GITHUB:   {_GITHUB_}\n"
        f" VERSION:  {_VERSION_} ({_DATE_})\n"
        f"================================================"
    )

    rich_description = f"""
{metadata}

DTMF (Touch-Tone) WAV Generator
------------------------------------------------
Generates telephony dialing tones for digits 0-9, *, #, and A-D.

Batch processing with --list:
  The input file should be a CSV-formatted text file:
  filename, NUMBER, tone_duration, silence_duration
  Example: dial1.wav, 12345, 0.2, 0.1

Manual Usage Examples:
  1. Generate tones for 123 (default durations):
     python dtmf_gen.py -DIAL 1,2,3 -o dialed.wav
  
  2. Custom timing and overwrite:
     python dtmf_gen.py -DIAL 060123456 -t 0.5 -s 0.2 --overwrite
    """

    parser = argparse.ArgumentParser(
        description=rich_description if "--help" in sys.argv else "DTMF WAV Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    
    # Help Options
    parser.add_argument("-h", action="store_true", help="Show short help")
    parser.add_argument("--help", action="store_true", help="Show full documentation")

    # Output Options
    parser.add_argument("-o", "--output", default="dialed.wav", help="Output filename (default: dialed.wav)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files without prompting")
    parser.add_argument("--list", type=str, help="Path to a CSV file for batch generation")

    # Dialing Options
    parser.add_argument("-DIAL", help="Sequence to dial (e.g., 1,2,3 or 060123456)")
    parser.add_argument("-t", "--tone", type=float, default=0.2, help="Tone duration in seconds (default: 0.2)")
    parser.add_argument("-s", "--silence", type=float, default=0.1, help="Silence duration in seconds (default: 0.1)")
    parser.add_argument("--freq", type=int, default=44100, help="Sampling rate (default: 44100)")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)
    if args.h:
        print(f"DTMF Generator v{_VERSION_} by {_AUTHOR_}")
        print("Usage: dtmf_gen.py -DIAL SEQUENCE [-o OUTPUT] [-t TONE_DUR] [-s SILENCE_DUR] [--list FILE] [--overwrite]")
        sys.exit(0)

    # Batch Mode
    if args.list:
        if not os.path.exists(args.list):
            print(f"Error: List file '{args.list}' not found.")
            sys.exit(1)
            
        with open(args.list, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 4:
                    print(f"Skipping invalid line: {line}")
                    continue
                
                try:
                    f_name = parts[0]
                    number = parts[1]
                    t_dur = float(parts[2])
                    s_dur = float(parts[3])
                    generate_dtmf_file(f_name, number, t_dur, s_dur, args.freq, args.overwrite)
                except ValueError:
                    print(f"Error parsing line: {line}")

    # Single File Mode
    elif args.DIAL:
        if os.path.exists(args.output) and not args.overwrite:
            response = input(f"File '{args.output}' already exists. Overwrite? [y/N]: ").strip().lower()
            if response != 'y':
                print("Operation cancelled.")
                sys.exit(0)
        
        generate_dtmf_file(args.output, args.DIAL, args.tone, args.silence, args.freq, True)
    
    else:
        print("Error: You must provide -DIAL sequence or a --list file.")
        parser.print_usage()

if __name__ == "__main__":
    main()
