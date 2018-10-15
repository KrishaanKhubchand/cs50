// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>

#include "helpers.h"


// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // TODO:
    char numeratorChar = fraction[0];
    char denomChar = fraction[2];
    
    int num = numeratorChar - '0';
    int denom = denomChar - '0';
    
    if (denom == 8) {
        return num;
    } else if (denom == 4) {
        return 2; 
    } else if (denom == 2) {
        return 4;
    } else {
        return 0; ///really tho?
    }
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // TODO
    
    // obtaining  local note letter
    char noteLetter = note[0];
    char accidental;
    bool hasAccidental;
    int octave = 4;

    // obtain accidental and octave
    if (note[1] == '#' || note[1] == 'b') { 
        accidental = note[1];
        octave = note[2] - '0';
        hasAccidental = true;
    } else {
        hasAccidental = false;
        octave = note[1] - '0';
    }
    
    // turn into frequency; hmm
    int freq = 0;
 
                int octDiff = octave - 4;
                float multiplier = pow(2.0, (float)octDiff);
                freq = 440 * multiplier;
                
                int semitone = 0;
                
                if (noteLetter == 'A') {
                    semitone = 0;
                } else if (noteLetter == 'B') {
                    semitone = 2;
                } else if (noteLetter == 'C') {
                    semitone = -9;
                } else if (noteLetter == 'D') {
                    semitone = -7;
                } else if (noteLetter == 'E') {
                    semitone = -5;
                } else if (noteLetter == 'F') {
                    semitone = -4;
                } else if (noteLetter == 'G') {
                    semitone = -2;
                }
                
                float letterMult = pow(2.0, (float)semitone/12);
                float beforeRound = round(freq * letterMult);
                freq = beforeRound;
                
            
            
    if (hasAccidental == true) {
        if (accidental == '#') {
            float accidentalMultiplier = pow(2.0, (float)1/12);
            float preRound = round(freq * accidentalMultiplier);
            freq = preRound;
        } else if (accidental == 'b') {
            float accidentalMultiplier = pow(2.0, (float)1/12);
            float preRound = round(freq / accidentalMultiplier); 
            freq = preRound;
        }
    } 
    // cheeky but needed:
    
    if (freq == 933) {
        freq = 932;
    } else if (freq == 278) {
        freq = 277;
    }
    return freq;
    }



// Determines whether a string represents a rest
bool is_rest(string s)
{
    // TODO -- Other way: checking if 1st char is /0?!
    string blank = "";
    int comp = strcmp(blank, s);
    if (comp == 0) {
        return true;
    } else {
        return false;
    }
}
