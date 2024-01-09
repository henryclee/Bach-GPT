import music21
import pickle

pieces = {
    "/Users/henry/OneDrive/Coding/Bach/bach_central/invent/":[
        "invent1", "invent2", "invent3", "invent4", "invent5", "invent6", 
        "invent7", "invent8", "invent9", "invent10", "invent11", "invent12", 
        "invent13", "invent14", "invent15"
    ],
    "/Users/henry/OneDrive/Coding/Bach/bach_central/sinfon/":[
        "sinfon1", "sinfon2", "sinfon3", "sinfon4", "sinfon5", "sinfon6", 
        "sinfon7", "sinfon8", "sinfon9", "sinfon10", "sinfon11", "sinfon12", 
        "sinfon13", "sinfon14", "sinfon15"
    ],
    "/Users/henry/OneDrive/Coding/Bach/bwv988x/":[
        "988-aria", "988-v01", "988-v02", "988-v03", "988-v04", "988-v05", 
        "988-v06", "988-v07", "988-v08", "988-v09", "988-v10", "988-v11", 
        "988-v12", "988-v13", "988-v14", "988-v15", "988-v16", "988-v17", 
        "988-v18", "988-v19", "988-v20", "988-v21", "988-v22", "988-v23", 
        "988-v24", "988-v25", "988-v26", "988-v27", "988-v28", "988-v29", 
        "988-v30"],
    "/Users/henry/OneDrive/Coding/Bach/bach_central/partitas/":[
        "all1", "all2", "cap2", "cou1", "cou2", "gig1", "men1", "pre1",
        "ron2", "sar1", "sar2", "sin2"
    ],
    "/Users/henry/OneDrive/Coding/Bach/bach_central/aof/":[
        "can1", "can2", "can3", "can4", "cnt1", "cnt2", "cnt3", "dou1",
        "dou2", "inver1", "inver2", "mir1", "mir2", "reg1", "reg2", "tri1",
        "tri2", "unfin" 
    ]
}

for path, files in pieces.items():
    for file in files:

        stream = music21.converter.parse(f'{path}{file}.mid')
        parts = list(music21.instrument.partitionByInstrument(stream))

        allNotes = []

        for part in parts:
            templist = []
            notes = [note for element in part.notes for note in (element if isinstance(element, music21.chord.Chord) else ([element] if isinstance(element, music21.note.Note) else []))]
            p1 = 0
            p2 = 0
            while p1 < len(allNotes) and p2 < len(notes):
                if allNotes[p1].offset < notes[p2].offset:
                    templist += [allNotes[p1]]
                    p1 += 1
                else:
                    templist += [notes[p2]]
                    p2 += 1
            if p1 < len(allNotes):
                templist += allNotes[p1:]
            else:
                templist += notes[p2:]
            allNotes = templist
        noteString = [note.nameWithOctave for note in allNotes]

        offsets = []
        for n in allNotes:
            offsets.append(n.offset)
        currTime = 0.0
        currLength = 0
        noteTuples = []
        for i,n in enumerate(noteString):
            if offsets[i] == currTime:
                currLength += 1
            else:
                if currLength == 1:
                    noteTuples.append((noteString[i-1],''))
                elif currLength >= 2:
                    noteTuples.append((noteString[i-2],noteString[i-1]))
                currLength = 1
                currTime = offsets[i]
        if currLength == 1:
            noteTuples.append((noteString[-1],''))
        elif currLength >= 2:
            noteTuples.append((noteString[-2],noteString[-1]))

        with open(f'./data/{file}.pkl', 'wb') as fp:
            pickle.dump(noteTuples, fp)
        fp.close
