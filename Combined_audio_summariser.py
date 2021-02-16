
# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from pydub import AudioSegment
import speech_recognition as sr
from pydub.silence import split_on_silence
from gensim.summarization import summarize
from nltk.tokenize import sent_tokenize


def auto_summary(path1):
    #file_name = 'test'
    # Opening file and extracting segment
    song = AudioSegment.from_wav(path1)

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(song,
                              # must be silent for at least 0.5 seconds
                              # or 500 ms. adjust this value based on user
                              # requirement. if the speaker stays silent for
                              # longer, increase this value. else, decrease it.
                              min_silence_len=800,

                              # consider it silent if quieter than -16 dBFS
                              # adjust this per requirement
                              silence_thresh=-36
                              )
    print("Opened file and created chunks")
    print("chunks length is", len(chunks))
    i = 0

    #### To Do ->>>>> Find a data structure to avoid multiple entries of same sentence

    # process each chunk
    sentences = {}
    original_text = ""
    for chunk in chunks:

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        chunk.export("chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'chunk' + str(i) + '.wav'

        print("Processing chunk " + str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working
            # correctly.
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened, language='en-GB')
            # write the output to the file.
            print(rec+'.')
            sentences[rec+'.'] = i

            print(sentences[rec+'.'])
            original_text = original_text + rec + '. '

            # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1
    print("original text is: ", original_text)
    short_summary = summarize(original_text)
    print("short summary is :", short_summary)

    #comment this
    #summarySen = short_summary.split('.')


    #uncomment this
    summarySen = sent_tokenize(short_summary)
   # pop = summarySen.pop()
    print(summarySen)
    print("length is :", len(summarySen))
    combined_wav = AudioSegment.empty()

    for sen in summarySen:
        print(sen)
        idx = sentences[sen]
        print(idx)
        order = AudioSegment.from_wav('chunk' + str(idx) + '.wav')
        combined_wav += order

    combined_wav.export(path + '-extract.wav', format="wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = input()
    auto_summary(path)