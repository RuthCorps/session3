import pandas as pd 
from psychopy import visual, sound, event, core
import numpy as np
from pydub.playback import play

class Experiment:
    # initialising experiment window
    def __init__(self, window_size, text_color, backgound_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=backgound_color)
        self.fixation = visual.TextStim(self.window, text='+', color=text_color)
        self.word = visual.TextStim(self.window, text="z=Nonword; m=Word", alignHoriz="center", color=text_color)
        self.clock = core.Clock

    # showing instructions
    def show_message(self, message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        event.waitKeys()

class Trial: 
    # initialise a trial
    def __init__(self, experiment, name, condition, sound, fixation_time=0.5, max_key_wait=5, keys=['m', 'z']):
        self.experiment = experiment
        self.name = name
        self.condition = condition
        self.sound = sound
        self.fixation_time = fixation_time 
        self.max_key_wait = max_key_wait
        self.keys = keys

    def run(self): 
        self.experiment.fixation.draw()
        self.experiment.window.flip()
        core.wait(self.fixation_time)

        self.experiment.word.draw()
        self.experiment.window.flip()

        self.sound.play()

        # wait for user input
        start_time = self.experiment.clock.getTime()
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock, clearEvents=True)
        if keys is not None: 
            key, end_time = keys[0]
        else: 
            key = None
            end_time = self.clock.getTime()

        # Store the results
        return {
            'trial': self.name,
            'key': key, 
            'start_time': start_time, 
            'end_time': end_time
        }




# Read stimuli
stimuli = pd.read_csv("session_3/lexical_decision_stimuli.csv")

# rename NW sound folder to none to match the condition names
#os.rename("session_3/sounds/NW", "session_3/sounds/none")

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

# Randomise
audios = np.random.permutation(audios)

#Run trials and append results
results=[]
for audio in audios:
    result = audio.run()
    results.append(result)

# Create a dataframe based on the results, and store them to a csv file
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']  # Calculate all the reaction times
results.to_csv('results.csv')