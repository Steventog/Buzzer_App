import customtkinter as ctk
import serial
import threading
import time
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

class DisplayWindow:
    def __init__(self, parent_app):
        self.window = ctk.CTkToplevel()
        self.window.title("Tableau d'affichage")
        self.window.geometry("1024x768")  # Taille par défaut
        self.window.resizable(True, True)  # Redimensionnable
        self.parent_app = parent_app
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Frame des scores avec animation
        self.score_frame = ctk.CTkFrame(main_frame)
        self.score_frame.pack(expand=True, fill="x", padx=30, pady=10)
        
        # Frame équipe 1 (bleu) avec animation
        self.team1_frame = ctk.CTkFrame(self.score_frame, fg_color="#ADD8E6")
        self.team1_frame.pack(side="left", expand=True, fill="x", padx=20, pady=10, ipadx=30, ipady=10)
        
        self.team1_name = ctk.CTkLabel(self.team1_frame, text="EQUIPE 1", 
                                     font=("Arial", 48, "bold"))
        self.team1_name.pack(pady=10)
        
        self.team1_score = ctk.CTkLabel(self.team1_frame, text="0 POINTS", 
                                      font=("Arial", 72, "bold"))
        self.team1_score.pack(pady=10)
        
        # Frame équipe 2 (rouge) avec animation
        self.team2_frame = ctk.CTkFrame(self.score_frame, fg_color="#FFB6C1")
        self.team2_frame.pack(side="right", expand=True, fill="x", padx=20, pady=10, ipadx=30, ipady=10)
        
        self.team2_name = ctk.CTkLabel(self.team2_frame, text="EQUIPE 2", 
                                     font=("Arial", 48, "bold"))
        self.team2_name.pack(pady=10)
        
        self.team2_score = ctk.CTkLabel(self.team2_frame, text="0 POINTS", 
                                      font=("Arial", 72, "bold"))
        self.team2_score.pack(pady=10)
        
        # Frame pour l'équipe qui a buzzé
        self.buzz_frame = ctk.CTkFrame(main_frame, fg_color="#333333")
        self.buzz_frame.pack(fill="x", padx=20, pady=20)
        
        self.buzz_label = ctk.CTkLabel(self.buzz_frame, text="", 
                                     font=("Arial", 64, "bold"))
        self.buzz_label.pack(pady=30)
        
        self.update_display()
    
    def close_window(self):
        self.window.destroy()
    
    def flash_team(self, team_frame):
        """Crée un effet de flash pour l'équipe qui a buzzé"""
        original_color = team_frame.cget("fg_color")
        team_frame.configure(fg_color="#FFFF00")  # Jaune vif
        self.window.after(200, lambda: team_frame.configure(fg_color=original_color))
    
    def update_display(self):
        """Met à jour l'affichage des scores et du buzz"""
        # Mise à jour des scores
        self.team1_score.configure(text=f"{self.parent_app.team1_score} POINTS")
        self.team2_score.configure(text=f"{self.parent_app.team2_score} POINTS")
        
        # Mise à jour du buzz
        buzz_text = self.parent_app.buzz_label.cget("text")
        if buzz_text != self.buzz_label.cget("text"):
            self.buzz_label.configure(text=buzz_text)
            if "EQUIPE 1" in buzz_text:
                self.flash_team(self.team1_frame)
            elif "EQUIPE 2" in buzz_text:
                self.flash_team(self.team2_frame)
        
        # Mise à jour continue
        self.window.after(100, self.update_display)

class QuizApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Quiz Buzzer")
        self.window.geometry("800x600")
        
        # Scores des équipes
        self.team1_score = 0
        self.team2_score = 0
        
        # Configuration du port série
        self.serial_port = None
        self.is_running = True
        self.buzz_locked = False
        
        # Équipe actuellement sélectionnée (1 ou 2)
        self.current_team = None
        
        # Fenêtre d'affichage
        self.display_window = None
        
        self.setup_gui()
        self.connect_arduino()
    
    def setup_gui(self):
        # Frame des scores (en haut)
        score_frame = ctk.CTkFrame(self.window)
        score_frame.pack(pady=20, padx=20, fill="x")
        
        # Frame équipe 1 (bleu)
        self.team1_frame = ctk.CTkFrame(score_frame, fg_color="#ADD8E6")
        self.team1_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        
        ctk.CTkLabel(self.team1_frame, text="EQUIPE 1", 
                    font=("Arial", 24, "bold")).pack(pady=10)
        self.team1_score_label = ctk.CTkLabel(self.team1_frame, text="0 POINTS", 
                                            font=("Arial", 36, "bold"))
        self.team1_score_label.pack(pady=20)
        
        # Frame équipe 2 (rouge)
        self.team2_frame = ctk.CTkFrame(score_frame, fg_color="#FFB6C1")
        self.team2_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        ctk.CTkLabel(self.team2_frame, text="EQUIPE 2", 
                    font=("Arial", 24, "bold")).pack(pady=10)
        self.team2_score_label = ctk.CTkLabel(self.team2_frame, text="0 POINTS", 
                                            font=("Arial", 36, "bold"))
        self.team2_score_label.pack(pady=20)
        
        # Frame d'affichage de l'équipe qui a buzzé
        self.buzz_frame = ctk.CTkFrame(self.window)
        self.buzz_frame.pack(pady=20, padx=20, fill="x")
        
        self.buzz_label = ctk.CTkLabel(self.buzz_frame, text="", 
                                     font=("Arial", 32, "bold"))
        self.buzz_label.pack(pady=20)
        
        # Frame des boutons de points
        points_frame = ctk.CTkFrame(self.window)
        points_frame.pack(pady=20, padx=20, fill="x")
        
        # Première ligne de boutons de points
        points_buttons_frame1 = ctk.CTkFrame(points_frame)
        points_buttons_frame1.pack(pady=10)
        
        for points in range(5):
            btn = ctk.CTkButton(points_buttons_frame1,
                              text=f"+{points}",
                              width=100,
                              command=lambda p=points: self.add_points(p),
                              fg_color="green",
                              hover_color="darkgreen")
            btn.pack(side="left", padx=5)
        
        # Deuxième ligne avec Reset et Passer
        control_buttons_frame = ctk.CTkFrame(points_frame)
        control_buttons_frame.pack(pady=10)
        
        ctk.CTkButton(control_buttons_frame,
                     text="RESET",
                     width=150,
                     command=self.reset_buzz,
                     fg_color="green",
                     hover_color="darkgreen"
                     ).pack(side="left", padx=5)
        
        ctk.CTkButton(control_buttons_frame,
                     text="PASSER À L'ADVERSAIRE",
                     width=150,
                     command=self.switch_team,
                     fg_color="green",
                     hover_color="darkgreen"
                     ).pack(side="left", padx=5)
        
        # Bouton pour ouvrir la fenêtre d'affichage
        display_button = ctk.CTkButton(self.window,
                                     text="TABLEAU D'AFFICHAGE",
                                     width=200,
                                     height=50,
                                     command=self.open_display_window,
                                     fg_color="blue",
                                     hover_color="darkblue")
        display_button.pack(pady=20)
    
    def open_display_window(self):
        """Ouvre la fenêtre d'affichage"""
        if self.display_window is None or not self.display_window.window.winfo_exists():
            self.display_window = DisplayWindow(self)
    
    def flash_score(self, team):
        """Crée un effet de flash lors de l'ajout de points"""
        label = self.team1_score_label if team == 1 else self.team2_score_label
        label.configure(text_color="#FFFF00")  # Jaune vif
        self.window.after(200, lambda: label.configure(text_color="black"))
    
    def connect_arduino(self):
        """Tente de se connecter à l'Arduino"""
        try:
            self.serial_port = serial.Serial('COM4', 9600, timeout=0.1)
            threading.Thread(target=self.read_serial, daemon=True).start()
        except:
            messagebox.showerror("Erreur", "Impossible de se connecter à l'Arduino")
    
    def read_serial(self):
        """Lit les données du port série en continu"""
        while self.is_running:
            if self.serial_port and self.serial_port.is_open:
                try:
                    if self.serial_port.in_waiting and not self.buzz_locked:
                        line = self.serial_port.readline().decode('utf-8').strip()
                        if line in ["Equipe 1", "Equipe 2"]:
                            self.buzz_locked = True
                            self.current_team = 1 if line == "Equipe 1" else 2
                            self.serial_port.reset_input_buffer()
                            self.window.after(0, self.update_buzz_display)
                            time.sleep(0.5)
                except:
                    pass
            time.sleep(0.1)
    
    def update_buzz_display(self):
        """Met à jour l'affichage de l'équipe qui a buzzé"""
        self.buzz_label.configure(text=f"EQUIPE {self.current_team} A BUZZÉ")
    
    def add_points(self, points):
        """Ajoute des points à l'équipe actuelle"""
        if self.current_team is None:
            messagebox.showwarning("Attention", "Aucune équipe n'a buzzé!")
            return
            
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment continuer ?"):
            if self.current_team == 1:
                self.team1_score += points
                self.team1_score_label.configure(text=f"{self.team1_score} POINTS")
                self.flash_score(1)
            else:
                self.team2_score += points
                self.team2_score_label.configure(text=f"{self.team2_score} POINTS")
                self.flash_score(2)
            self.reset_buzz()
    
    def reset_buzz(self):
        """Réinitialise l'affichage du buzz"""
        self.buzz_label.configure(text="")
        self.current_team = None
        self.buzz_locked = False
        if self.serial_port:
            self.serial_port.reset_input_buffer()
    
    def switch_team(self):
        """Change l'équipe actuellement sélectionnée"""
        if self.current_team is None:
            messagebox.showwarning("Attention", "Aucune équipe n'a buzzé!")
            return
        
        self.current_team = 2 if self.current_team == 1 else 1
        self.update_buzz_display()
    
    def run(self):
        """Lance l'application"""
        self.window.mainloop()
        self.is_running = False
        if self.serial_port:
            self.serial_port.close()

if __name__ == "__main__":
    app = QuizApp()
    app.run()
