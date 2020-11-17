#Option 1: Lexical decision task
#In a lexical decision task, the participant is presented with a word for a given period of time, and asked to respond whether they think it is a real word (or not). Typically, participants will respond faster to high-frequency words than to low-frequency words. We are going to build an experiment that can do this. You can use the stimuli you created for session 2b (HF/LF/NW); but if you did not manage to create the stimuli, or do not like the result, all the stimuli are also in the repository of session 3.
#We have high frequency, low frequency, and non-word stimuli. For the first version, we will make a demo that presents a couple of auditory stimuli regardless of the condition. After making an experiment that can simply present auditory stimuli and record the response, you can think of a way to neatly randomize the three conditions.
#Key elements of the experiment:
#-        Read the csv with stimulus information
#-        Present an auditory stimulus
#-        Fixation cross-screen
#-        Decision screen
#-        Clock
#-        Keys to press
#-        Record the response & timing

import pandas as pd 
from psychopy import visual, sound, event, core
import numpy as np
from pydub.playback import play

# Create a window and define all text elements. Read the stimuli csv file
window = visual.Window((800, 600), color=(1, 1, 1)) # colour = r, g, b
fixation = visual.TextStim(window, text="+", color=(-1, -1, -1)) # create a fixation cross and specify which window to draw it on
instructions = visual.TextStim(window, text="In this experiment, you will hear some audio. If you think you hear a word, press 'm', If you think you hear a nonword, press 'z'", alignHoriz='center', color=(-1, -1, -1))
word = visual.TextStim(window, text="z=Nonword; m=Word", alignHoriz="center", color=(-1, -1, -1))
stimuli = pd.read_csv("session_3/lexical_decision_stimuli.csv")
#print(stimuli)


# rename NW sound folder to none to match the condition names
#os.rename("session_3/sounds/NW", "session_3/sounds/none")

# randomise stimuli
stimuli = stimuli.iloc[np.random.permutation(len(stimuli))]
#print(stimuli)

# Load the audio and randomize
high_path = "session_3/sounds/HF/"
low_path = "session_3/sounds/LF/"
none_path = "session_3/sounds/none/"

audios = []
for i, row in stimuli.iterrows(): 
    if row['freq_category'] == 'HF': 
        audios.append(sound.Sound(high_path+row['word']+'.wav'))
    elif row['freq_category'] == 'LF':
        audios.append(sound.Sound(low_path+row['word']+'.wav'))
    else: 
        audios.append(sound.Sound(none_path+row['word']+'.wav'))


clock = core.Clock() # start clock

# present the instructions
instructions.draw()
window.flip()
keys = event.waitKeys(keyList=['space'])

# define trial structure 
results = []
trialnum = 0
for audio in audios[:5]:
    fixation.draw()
    window.flip()
    core.wait(1)

    audio.play()
    word.draw()
    window.flip()
    start_time = clock.getTime()
    keys = event.waitKeys(maxWait=5,keyList=['z','m'], timeStamped=clock, clearEvents=True) #timestamp shows that the first item in the list is earlier
    if keys is not None:
        key, reaction_time = keys[0]
    else:
        key = None
        reaction_time = 5

    results.append({
        'audio': stimuli["word"].iloc[trialnum],
        'condition': stimuli['freq_category'].iloc[trialnum], 
        'key': key,
        'reaction_time': reaction_time - start_time

    })

    trialnum = trialnum + 1

print(results)
results = pd.DataFrame(results)
print(results)
results.to_csv('results.csv') # saves the results to a csv file










