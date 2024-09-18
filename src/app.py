import customtkinter as ctk
from tkinter import filedialog
from pytubefix import YouTube as yt
import datetime
import os

# Get the absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(BASE_DIR, "resources", "red.json")

# Set appearance mode to dark and load custom color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(THEME_PATH)

class App(ctk.CTk):

  # Declare all widgets and variables
  ui_button_plus = None
  ui_button_minus = None
  wres = ["1080p", "1440p", "4K", "Manual"]
  scaling = None
  url_entry = None
  content_frame = None
  av_res = []
  video = None
  dw_mode_select = None
  dw_res_select = None
  progress_frame = None
  progress_bar = None
  progress_percent = None
  finish_frame = None
  footer_destination = None
  footer_name = None

  # Initialize the app
  def __init__(self):
    super().__init__()
    self.title("Youtube Downloader")
    # Set window size based on screen resolution
    if (self.winfo_screenwidth() < 1920) or (self.winfo_screenheight() < 1080):
      self.geometry("1820x980")
      ctk.set_widget_scaling(float(1))
      self.scaling = 1
    elif (self.winfo_screenwidth() < 2560) or (self.winfo_screenheight() < 1440):
      self.geometry("2420x1340")
      self.wres[0], self.wres[1] = self.wres[1], self.wres[0]
      ctk.set_widget_scaling(float(1.5))
      self.scaling = 1.5
    else:
      self.geometry("3720x1960")
      self.wres[0], self.wres[2] = self.wres[2], self.wres[0]
      ctk.set_widget_scaling(float(2))
      self.scaling = 2

    # configure grid layout
    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)
    

    # create sidebar frame with widgets
    self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
    self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(1, weight=1)
    self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Youtube\n\nDownloader", font=ctk.CTkFont(size=20, weight="bold"))
    self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))


    self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
    self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0))
    self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode)
    self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
    self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
    self.scaling_label.grid(row=6, column=0, padx=20, pady=(10, 0))
    self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=self.wres,
                                                               command=self.change_scaling)
    self.scaling_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 20))
    self.ui_button_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
    self.ui_button_frame.grid(row=8, column=0)
    self.ui_button_frame.grid_columnconfigure((0,1), weight=1)
    self.ui_button_minus = ctk.CTkButton(self.ui_button_frame, state="disabled", text="-", command=lambda:self.modify_scaling(-1), width=70, corner_radius=0)
    self.ui_button_minus.grid(row=0, column=0, padx=(20,0), pady=10)
    self.ui_button_plus = ctk.CTkButton(self.ui_button_frame, state="disabled", text="+", command=lambda:self.modify_scaling(1), width=70, corner_radius=0)
    self.ui_button_plus.grid(row=0, column=1, padx=(0,20), pady=10)

    # create main frame with widgets
    self.frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
    self.frame.grid(row=0, column=1, sticky="nsew")
    self.frame.grid_columnconfigure(0, weight=1)
    self.frame.grid_rowconfigure(0, weight=1)
    self.frame_content = ctk.CTkFrame(self.frame, corner_radius=0, fg_color="transparent")
    self.frame_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    # create footer frame with credits
    self.credit = ctk.CTkLabel(self.frame, text="Made by @IPG2004", font=ctk.CTkFont(size=20, weight="bold"))
    self.credit.grid(row=1, column=0, sticky="nsew", padx=0, pady=0, ipadx=20, ipady=20)

    self.frame_content.grid_columnconfigure(0, weight=1)
    self.frame_content.grid_rowconfigure(1, weight=1)

    # create widgets in main frame
    frame_header = ctk.CTkFrame(self.frame_content, corner_radius=20)
    frame_header.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    frame_header.grid_columnconfigure(0, weight=1)
    self.url_entry = ctk.CTkEntry(frame_header, corner_radius=20, placeholder_text="Enter video URL here")
    self.url_entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    header_clear = ctk.CTkButton(frame_header, text="Clear", command=self.clear_scfr)
    header_clear.grid(row=0, column=1, sticky="nsew", padx=10, pady=10, ipadx=10, ipady=10)
    header_search = ctk.CTkButton(frame_header, text="Search", command=self.search_video)
    header_search.grid(row=0, column=2, sticky="nsew", padx=10, pady=10, ipadx=10, ipady=10)

    self.content_frame = ctk.CTkFrame(self.frame_content, corner_radius=20)
    self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    frame_footer = ctk.CTkFrame(self.frame_content, corner_radius=20)
    frame_footer.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame_footer.grid_columnconfigure(0, weight=1)

    self.footer_destination = ctk.CTkLabel(frame_footer, text="Destination folder", corner_radius=20)
    self.footer_destination.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
    footer_destination_search = ctk.CTkButton(frame_footer, text="Destination", command=self.select_destination_folder)
    footer_destination_search.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    self.footer_name = ctk.CTkEntry(frame_footer, corner_radius=20, placeholder_text="Filename")
    self.footer_name.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    footer_dw = ctk.CTkButton(frame_footer, text="Download", command=self.download)
    footer_dw.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

  # Function to change appearance mode
  def change_appearance_mode(self, mode):
    ctk.set_appearance_mode(mode)

  # Function to change UI scaling
  def change_scaling(self, new_scaling: str):
    if new_scaling == "Manual":
      self.ui_button_minus.configure(state="enabled")
      self.ui_button_plus.configure(state="enabled")
    else:
      self.ui_button_minus.configure(state="disabled")
      self.ui_button_plus.configure(state="disabled")

    if new_scaling == "1080p":
      self.geometry("1920x1080")
      ctk.set_widget_scaling(float(1))
      self.scaling = 1
    elif new_scaling == "1440p":
      self.geometry("2560x1440")
      ctk.set_widget_scaling(float(1.5))
      self.scaling = 1.5
    elif new_scaling == "4k":
      self.geometry("3840x2160")
      ctk.set_widget_scaling(float(2))
      self.scaling = 2
      
  # Function to modify UI scaling manually
  def modify_scaling(self, value: int):
    if (value > 0):
      self.scaling += 0.1
    else:
      self.scaling -= 0.1
    ctk.set_widget_scaling(self.scaling)

  # Function to search for video
  def search_video(self):
    url = self.url_entry.get()
    if url:
      self.url_entry.configure(fg_color=("#F9F9FA", "#343638"))
      self.video = yt(url, on_progress_callback=self.on_progress)
      self.content = [self.video.title, self.video.author, str(datetime.timedelta(seconds=self.video.length)), self.video.views, self.video.publish_date.strftime("%d/%m/%Y")]
      res = set()
      # Get available resolutions
      for stream in self.video.streams.filter(progressive=True):
        res.add(f"{stream.resolution}")
      res.discard("None")
      self.av_res = list(res)
      self.build_content_frame()
    else:
      # If no URL is entered, highlight the entry field
      self.url_entry.configure(fg_color="red")

  # Function to clear search content
  def clear_scfr(self):
    self.url_entry.configure(fg_color=("#F9F9FA", "#343638"))
    self.url_entry.delete(0, "end")
    self.content = []
    self.content_frame.destroy()
    self.av_res = []
    self.video = True
    self.content_frame = ctk.CTkFrame(self.frame_content, corner_radius=20)
    self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    self.footer_destination.configure(text="Destination folder", fg_color="transparent")
    self.footer_name.delete(0, "end")
    self.footer_name.configure(fg_color=("#F9F9FA", "#343638"))
    
  # Function to build information frame acording to video
  def build_content_frame(self):
    self.content_frame = ctk.CTkFrame(self.frame_content, corner_radius=20, fg_color="transparent")
    self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    self.content_frame.grid_columnconfigure(0, weight=1)
    info_frame = ctk.CTkFrame(self.content_frame, corner_radius=20)
    info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    info_frame.grid_columnconfigure(1, weight=1)

    # Display video information
    ctk.CTkLabel(info_frame, text="Title:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text="Author:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=1, column=0, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text="Length:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=2, column=0, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text="Views:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=3, column=0, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text="Publish Date:", font=ctk.CTkFont(size=18, weight="bold")).grid(row=4, column=0, sticky="nsw", padx=20, pady=20)

    ctk.CTkLabel(info_frame, text=f"{self.content[0]}", font=ctk.CTkFont(size=15)).grid(row=0, column=1, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text=f"{self.content[1]}", font=ctk.CTkFont(size=15)).grid(row=1, column=1, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text=f"{self.content[2]}", font=ctk.CTkFont(size=15)).grid(row=2, column=1, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text=f"{'{:,}'.format(self.content[3]).replace(",",".")}", font=ctk.CTkFont(size=15)).grid(row=3, column=1, sticky="nsw", padx=20, pady=20)
    ctk.CTkLabel(info_frame, text=f"{self.content[4]}", font=ctk.CTkFont(size=15)).grid(row=4, column=1, sticky="nsw", padx=20, pady=20)

    # Widgets of options for download
    dwoptions_frame = ctk.CTkFrame(self.content_frame, corner_radius=20)
    dwoptions_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    self.dw_mode_select = ctk.CTkOptionMenu(dwoptions_frame, values=["Video", "Audio"], command=self.change_dw_mode)
    self.dw_mode_select.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    self.dw_res_select = ctk.CTkOptionMenu(dwoptions_frame, values=self.av_res)
    self.dw_res_select.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    self.progress_frame = ctk.CTkFrame(self.content_frame, corner_radius=20)
    self.progress_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    self.progress_frame.grid_columnconfigure(0, weight=1)
    
  # Function to change download mode and disable resolution selection for audio
  def change_dw_mode(self, mode):
    if mode == "Audio":
      self.dw_res_select.configure(state="disabled")
    else:
      self.dw_res_select.configure(state="normal")

  # Function to build progress frame
  def progress_frame_build(self):
    progress_text = ctk.CTkLabel(self.progress_frame, text="Downloading...", font=ctk.CTkFont(size=20, weight="bold"))
    progress_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    self.progress_bar = ctk.CTkProgressBar(self.progress_frame, corner_radius=20)
    self.progress_bar.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    self.progress_bar.set(0)

    self.progress_percent = ctk.CTkLabel(self.progress_frame, text="0%", font=ctk.CTkFont(size=20, weight="bold"))
    self.progress_percent.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

  # Function to select destination folder
  def select_destination_folder(self):
    folder = filedialog.askdirectory(title="Select a folder")
    if folder:
      self.footer_destination.configure(text=folder, fg_color="transparent")

  # Function to update progress bar
  def on_progress(self, stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100
    self.progress_bar.set(float(percent/100))
    self.progress_percent.configure(text=f"{round(percent)}%")
    self.update()

  # Function to download video
  def download(self):
    # Check all the possible errors before downloading
    if self.finish_frame:
      self.finish_frame.destroy()
      self.progress_bar.set(0)
      self.progress_percent.configure(text="0%")
    self.progress_frame_build()
    error = False
    if self.content == []:
      self.scrollframe.configure(fg_color="red")
      error = True
    if self.footer_destination.cget("text") == "Destination folder":
      self.footer_destination.configure(fg_color="red")
      error = True
    if self.footer_name.get() == "":
      self.footer_name.configure(fg_color="red")
      error = True
    if error:
      return
    try:
      # Download video based on selected mode and resolution
      if self.dw_mode_select.get() == "Audio":
        self.video.streams.get_audio_only().download(self.footer_destination.cget("text"), self.footer_name.get(), mp3=True)
      else:
        self.video.streams.get_by_resolution(self.dw_res_select.get()).download(self.footer_destination.cget("text"), self.footer_name.get())
      
      # Build finish frame based on download success
      self.finish_frame = ctk.CTkFrame(self.content_frame, corner_radius=20, fg_color="green")
      self.finish_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
      self.finish_frame.grid_columnconfigure(0, weight=1)
      self.finish_frame.grid_rowconfigure(0, weight=1)
      finish_label = ctk.CTkLabel(self.finish_frame, text="Download finished", font=ctk.CTkFont(size=20, weight="bold"))
      finish_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    except Exception:
      # Build error frame based on download error
      error = ctk.CTkToplevel(self)
      error.title("Error")
      error.grid_columnconfigure(0, weight=1)
      error.grid_rowconfigure(0, weight=1)
      error_label = ctk.CTkLabel(error, text="An error occured during the download.", font=ctk.CTkFont(size=20, weight="bold"))
      error_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
      close_button = ctk.CTkButton(error, text="Close", command=lambda:(error.destroy(), self.clear_scfr()))
      close_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
      return

# Run the app
if __name__ == "__main__":
  app = App()
  app.mainloop()
    
