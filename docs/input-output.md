# Introduction

MIX provides for up to 21 input-output devices, indexed as follows:

| Unit Number | Device Type | Block Size | 
| ----------- | ----------- | ---------- |
| t, 0 <= t <= 7  | Tape                | 100 words | 
| d, 8 <= d <= 15 | Disk/Drum           | 100 words |
| 16              | Card Reader         | 16 words  |
| 17              | Card Punch          | 16 words  |
| 18              | Line Printer        | 24 words  |
| 19              | Typewriter Terminal | 14 words  |
| 20              | Paper Tape          | 14 words  |

## Notes

- Not every MIX installation will have all of this equipment available
- Some devices may not be used for both input and output
- IO with tape, disk, or drum reads/writes full words (five bytes and
  a sign)
- IO with units 16 through 20 is done with character code, where each
  byte represents one alphanumeric character.

# Implementation Notes

MIXpy outputs UTF-8-encoded text to support the select Greek letters
that MIX is capable of reading/writing.
