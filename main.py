from tkinter import *
from tkinter import filedialog
import pygame
from pdf import Reader
from audio import Polly


#---------- UPLOAD PDF ----------#
def upload_file():
    """Opens file dialog and extracts text"""
    global text
    # Open file dialog box
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    # Extract text from pdf
    text = reader.reader(pdf_name=file_path)


#---------- OPEN TEXT BOX ----------#
def text_box():
    """Places text box and buttons when "Enter text" pressed"""
    global text
    confirm_text.grid(column=4, row=3, columnspan=2, padx=10, pady=5)
    close_text.grid(column=4, row=4, columnspan=2, padx=10, pady=5)
    text_box.grid(column=1, row=3, columnspan=2, rowspan=2, padx=10)


def confirm_text():
    """Saves text entered and closes box & buttons when 'Confirm text' pressed"""
    global text
    # Gets hold of the text starting at the first character
    text = text_box.get("1.0", END)
    # Closes text box and buttons
    text_box.grid_forget()
    close_text.grid_forget()
    confirm_text.grid_forget()
    return text


#---------- CLOSE TEXT BOX ----------#
def close_text_box():
    """Closes text box and buttons"""
    text_box.grid_forget()
    close_text.grid_forget()
    confirm_text.grid_forget()

#---------- VOICE SELECTION ----------#
def neural():
    """Places neural voice options in grid"""
    close_ntts_voices.grid(column=3, row=7, columnspan=2, padx=10, pady=5)
    ntts_listbox.grid(column=0, row=6, columnspan=2, rowspan=3)
    select_ntts_voice.grid(column=3, row=8, columnspan=2, pady=5)


def close_ntts_voices():
    """Closes neural voice options"""
    close_ntts_voices.grid_forget()
    ntts_listbox.grid_forget()
    select_ntts_voice.grid_forget()

def standard():
    """Places standard voice options in grid"""
    close_stts_voices.grid(column=3, row=7, columnspan=2, padx=10, pady=5)
    stts_listbox.grid(column=0, row=6, columnspan=2, rowspan=3)
    select_stts_voice.grid(column=3, row=8, columnspan=2, pady=5)


def close_stts_voices():
    """Closes standard voice options"""
    close_stts_voices.grid_forget()
    stts_listbox.grid_forget()
    select_stts_voice.grid_forget()


#---------- GET STTS VOICE ----------#
def standard_listbox(event):
    """Plays samples of standard voices"""
    #     Gets current selection from listbox
    voice_sample_name = (stts_listbox.get(stts_listbox.curselection())).lower()
    pygame.mixer.music.load(f"voices/{voice_sample_name}.mp3")
    pygame.mixer.music.play()


def select_stts_voice():
    """Saves user voice selection to variable & closes options"""
    global voice_to_use
    voice_to_use += (stts_listbox.get(stts_listbox.curselection()))
    close_stts_voices.grid_forget()
    stts_listbox.grid_forget()
    select_stts_voice.grid_forget()



#---------- GET NTTS VOICE ----------#
def neural_listbox(event):
    """Plays samples of neural voices"""
    voice_sample_name = (ntts_listbox.get(ntts_listbox.curselection())).lower()
    pygame.mixer.music.load(f"voices/{voice_sample_name}.mp3")
    pygame.mixer.music.play()


def select_ntts_voice():
    """Saves user voice selection to variable & closes options"""
    global voice_to_use
    voice_to_use = (ntts_listbox.get(ntts_listbox.curselection()))
    close_ntts_voices.grid_forget()
    ntts_listbox.grid_forget()
    select_ntts_voice.grid_forget()


#---------- OUTPUT ----------#
def stream():
    """Synthesizes speech and streams audio"""
    if "NTTS" in voice_to_use:
        voice = voice_to_use.split("-")[0]
        engine = "neural"
    else:
        voice = voice_to_use.split("-")[0]
        engine = "standard"

    input_audio = polly.synthesize_speech(text, voice, engine)
    polly.stream_audio(audio_data=input_audio)

def download():
    """Synthesizes speech and downloads audio"""
    if "NTTS" in voice_to_use:
        voice = voice_to_use.split("-")[0]
        engine = "neural"
    else:
        voice = voice_to_use.split("-")[0]
        engine = "standard"

    input_audio = polly.synthesize_speech(text, voice, engine)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Audio Files", "*.mp3"),
                                                        ("All Files", "*.*")])

    if file_path:
        with open(file_path, 'wb') as file:
            file.write(input_audio)


#---------- UI SETUP ----------#
window = Tk()
window.title("Audiobook creator")
window.config(padx=150, pady=150, bg="#DFFFD8")

#---------- TITLE TEXT ----------#
title_text = Label(text="Audiobook Creator",
                   fg="black",
                   bg="#DFFFD8",
                   font=("Montserrat", 14, "bold")
                   )
title_text.grid(column=1, row=1, columnspan=2, padx=10, pady=5)

#---------- BUTTONS ----------#
enter_text = Button(text="Enter text", command=text_box, bg="#BEF0CB")
enter_text.grid(column=0, row=2, columnspan=2, padx=10, pady=5)

confirm_text = Button(text="Confirm text", command=confirm_text, bg="#BEF0CB")

close_text = Button(text="Close text box", command=close_text_box, bg="#BEF0CB")

upload_pdf = Button(text="Upload PDF", command=upload_file, bg="#BEF0CB")
upload_pdf.grid(column=3, row=2, columnspan=2, padx=10, pady=5)

neural_choice = Button(text="Neural voice", command=neural, bg="#BEF0CB")
neural_choice.grid(column=0, row=5, columnspan=2, padx=10, pady=5)

standard_voice = Button(text="Standard voice", command=standard, bg="#BEF0CB")
standard_voice.grid(column=3, row=5, columnspan=2, padx=10, pady=5)

stream_choice = Button(text="Stream audio", command=stream, bg="#BEF0CB")
stream_choice.grid(column=0, row=9, columnspan=2, padx=10, pady=5)

download_choice = Button(text="Download audio", command=download, bg="#BEF0CB")
download_choice.grid(column=3, row=9, columnspan=2, padx=10, pady=5)

#---------- TEXT BOX ----------#
text_box = Text(height=5, width=30)
text_box.focus()
text_box.insert(END, "Enter your text here")

#---------- NEURAL VOICE BUTTONS ----------#
close_ntts_voices = Button(text="Close voices", command=close_ntts_voices, bg="#BEF0CB")
select_ntts_voice = Button(text="Select voice", command=select_ntts_voice, bg="#BEF0CB")

ntts_voices = ["Amy (newscaster)-NTTS", "Amy-NTTS", "Emma-NTTS", "Brian-NTTS", "Arthur-NTTS"]
ntts_listbox = Listbox(height=len(ntts_voices))

for item in ntts_voices:
    ntts_listbox.insert(ntts_voices.index(item), item)

ntts_listbox.bind("<<ListboxSelect>>", neural_listbox)

#---------- STANDARD VOICE BUTTONS ----------#
close_stts_voices = Button(text="Close voices", command=close_stts_voices, bg="#BEF0CB")
select_stts_voice = Button(text="Select voice", command=select_stts_voice, bg="#BEF0CB")

stts_voices = ["Amy-STTS", "Emma-STTS", "Brian-STTS"]
stts_listbox = Listbox(height=len(stts_voices))

for item in stts_voices:
    stts_listbox.insert(stts_voices.index(item), item)

stts_listbox.bind("<<ListboxSelect>>", standard_listbox)




if __name__ == "__main__":
    polly = Polly()
    reader = Reader()


pygame.mixer.init()
window.mainloop()
