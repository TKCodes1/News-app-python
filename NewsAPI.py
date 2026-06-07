import requests
import tkinter as tk
import feedparser
import webbrowser
class NewsApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title("NewsApp")
        self.window_width = 1000
        self.window_height = 800
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.x = (self.screen_width // 2) - (self.window_width // 2)
        self.y = (self.screen_height // 2) - (self.window_height // 2)
        self.window.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        self.BG = "#0f172a"
        self.CARD = "#1e293b"
        self.TEXT = "#e2e8f0"
        self.articles = []

    def render_news(self, articles):
        for widget in self.scroll_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        for article in articles:
            label = tk.Label(
                self.scroll_frame,
                text="📰 " + article.title,
                font=("Arial", 14),
                fg=self.TEXT,
                bg=self.BG,
                wraplength=800,
                justify="left",
                cursor="hand2"
            )

            label.pack(fill="x", pady=10)

            label.bind(
                "<Button-1>",
                lambda e, url=article.link: self.open_link(url)
            )

    def filter_news(self):
        query = self.entry.get().lower().strip()

        if not self.articles:
            return  

        if query == "":
            self.render_news(self.articles)
            return

        filtered = [
            article for article in self.articles
            if query in article.title.lower()
        ]

        self.render_news(filtered)
        print("QUERY:", query)
        for a in self.articles:
            print(a.title)




    def open_link(self, url):
        webbrowser.open(url)


    def get_news(self):
        self.url = "https://feeds.bbci.co.uk/news/rss.xml"
        self.feed = feedparser.parse(self.url)

        self.articles = self.feed.entries[:500]

        self.render_news(self.articles)


    def setup_ui(self):

        self.top_frame = tk.Frame(self.window, bg=self.BG)
        self.top_frame.pack(fill="x")
        self.title = tk.Label(self.top_frame, text="News App", font=("Arial", 18, "bold"), fg=self.TEXT, bg=self.BG)
        self.title.pack(pady=10, anchor="center")

        self.entry = tk.Entry(self.top_frame,font=("Arial", 14), justify="center", bg=self.BG, fg=self.TEXT,insertbackground=self.TEXT)
        self.entry.pack(anchor="center", pady=20)

        self.search_button = tk.Button(self.top_frame, text="filter", command=self.filter_news)
        self.search_button.pack()

        self.button = tk.Button(self.top_frame, text="Continue", command=self.get_news, font=("Arial", 12),
                                fg=self.BG,
                                bg="lightblue")
        self.button.pack(pady=10, anchor="center")


        self.canvas = tk.Canvas(self.window, bg=self.BG, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = tk.Frame(self.canvas, bg=self.BG)

        self.center_frame = tk.Frame(self.scroll_frame, bg=self.BG)
        self.center_frame.pack(fill="x", pady=20)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="n")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scroll_frame.update_idletasks()

        self.canvas.itemconfig(self.canvas_window, width=self.window_width
        )





    def run(self):
        self.setup_ui()
        self.window.mainloop()


app = NewsApp()
app.run()