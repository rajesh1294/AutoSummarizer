# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from pydub import AudioSegment
from ffmpeg import video
import speech_recognition as sr

import os

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
from playsound import playsound

# a function that splits the audio file into chunks
# and applies speech recognition
def silence_based_conversion(path1):
    # open the audio file stored in
    # the local system as a wav file.
    song = AudioSegment.from_wav(path1)

    # open a file where we will concatenate
    # and store the recognized text
    fh = open("recognized.txt", "w+")

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(song,
                              # must be silent for at least 0.5 seconds
                              # or 500 ms. adjust this value based on user
                              # requirement. if the speaker stays silent for
                              # longer, increase this value. else, decrease it.
                              min_silence_len=500,

                              # consider it silent if quieter than -16 dBFS
                              # adjust this per requirement
                              silence_thresh=-36
                              )
    print("Opened file and created chunks")
    nonsilent_data = detect_nonsilent(song, min_silence_len=500, silence_thresh=-36, seek_step=1)
    # create a directory to store the audio chunks.
    try:
        os.mkdir("E:/Shweta/audio_chunks")
    except(FileExistsError):
        pass

    # move into the directory to
    # store the audio files.
    os.chdir('E:/Shweta/audio_chunks')
    print("moving into directory")
    print("chunks length is", len(chunks))
    i = 0
    # process each chunk

    for chunk_silen in nonsilent_data:
        print([chunk_si/1000 for chunk_si in chunk_silen])

    for chunk in chunks:

        # Create 0.5 seconds silence chunk
        #chunk_silent = AudioSegment.silent(duration=10)

        # add 0.5 sec silence to beginning and
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        #audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'chunk' + str(i) + '.wav'

        print("Processing chunk " + str(i))

        #playsound(filename)
        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            #r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened, language='en-GB')
            # write the output to the file.
            fh.write(rec + ". ")

            # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1

    os.chdir('..')


if __name__ == '__main__':
    print('Enter the audio file path')

    path = input()

    silence_based_conversion(path)
