import music21
import pickle

with open('./output/gpt11', 'rb') as fp:
    notes = pickle.load(fp)
fp.close

recoveredscore = music21.stream.Score()
for i,t in enumerate(notes):
    for n in [j for j in t if j]:
        note = music21.note.Note(nameWithOctave=n, type = "eighth")
        recoveredscore.append(note)
        recoveredscore.notes[-1].offset = i * .50
    i+=1

recoveredscore.show("midi")