form Get CPP
    sentence SoundFile
endform

Read from file... 'SoundFile$'
selectObject: 1
To PowerCepstrum: 75, 0.002, 5500, 50
cpp = Get peak prominence
writeInfoLine: cpp
