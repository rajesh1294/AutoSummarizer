import os   # to use the filesystem
from pydub import AudioSegment  # to the processing the audio
import speech_recognition as sr # to recognize the the audio
from pydub.silence import split_on_silence  # to detect the silence in between sentences
from gensim.summarization import summarize  # for extractive summarization
from nltk.tokenize import sent_tokenize  # tokenize the summary
from rouge import Rouge # to evaluate the auto generated summary


def auto_summary(file_path):
    # Opening file and extracting segment
    song = AudioSegment.from_wav(file_path)

    # open a file where we will concatenate and store the recognized original text
    originalFile = open("originalText.txt", "w+")

    # split track where silence is 0.8 seconds or more and get chunks
    chunks = split_on_silence(song,
                              # must be silent for at least 0.8 seconds or 800 ms.
                              # adjust this value based on user requirement.
                              # if the speaker stays silent for longer, increase this value. else, decrease it.
                              min_silence_len=800,

                              # consider it silent if quieter than -16 dBFS
                              # adjust this per requirement
                              silence_thresh=-36)

    print("Procession File...")
    print("Number of Chunks Created -", len(chunks))

    i = 0

    # to-do ->>>>> find a data structure to avoid multiple entries of same sentence

    # process each chunk
    sentences = {}
    original_text = ""

    for chunk in chunks:
        # export audio chunk and save it in the current directory.
        print("Processing and Saving chunk{0}.wav".format(i) + "...")

        # specify the bitrate to be 192 k
        chunk.export("chunk{0}.wav".format(i), bitrate='192k', format="wav")

        # the name of the newly created chunk
        filename = 'chunk' + str(i) + '.wav'

        # get the name of the newly created chunk in the AUDIO_FILE variable for later use.
        file = filename

        # create a speech recognition object
        r = sr.Recognizer()

        # recognize the chunk
        with sr.AudioFile(file) as source:
            # remove this if it is not working correctly.
            # r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened, language='en-GB')

            # write the output to the file.
            originalFile.write(rec + ". ")

            sentences[rec + '.'] = i

            print(sentences[rec + '.'], rec + '.')
            original_text = original_text + rec + '. '

            # catch any errors.
        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print("Could not request results. check your internet connection")

        i += 1

    print("Original Text - ", original_text)

    short_summary = summarize(original_text)
    print("Short Summary - ", short_summary)

    # summarySen = short_summary.split('.')
    summarySen = sent_tokenize(short_summary)

    # pop = summarySen.pop()
    print(summarySen)
    print("Number of Sentences in Summary -", len(summarySen))

    combined_wav = AudioSegment.empty()

    # open a file where we will concatenate and store the summarized text
    summarizedFile = open("summarizedText.txt", "w+")

    for sen in summarySen:
        idx = sentences[sen]
        print(idx, sen)
        summarizedFile.write(sen)
        order = AudioSegment.from_wav('chunk' + str(idx) + '.wav')
        combined_wav += order

    # saving summarized audio file
    combined_wav.export(os.path.dirname(file_path) + '/' + 'extractiveSummary.wav', format="wav")
    human_summary = '''Microsoft is investigating a trojan program that attempts to switch off the firm's anti-spyware software. Microsoft said it did not believe the program was widespread and recommended users to use an anti-virus program.Stephen Toulouse, a security manager at Microsoft, said the malicious program was called Bankash-A Trojan and was being sent as an e-mail attachment. Microsoft said in a statement it is investigating what it called a criminal attack on its software.'''
    # print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.
    rouge = Rouge()
    scores1 = rouge.get_scores(short_summary, human_summary)
    print(scores1)
    # removing useless files and data
    for i in range(0, (len(chunks))):
        os.remove(os.path.dirname(file_path) + '/' + 'chunk' + str(i) + '.wav')


if __name__ == '__main__':
    file_path = input('Enter the Audio File Path - ')
    auto_summary(file_path)