# Importowanie modułu PIL, który umożliwia manipulowanie obrazami
from PIL import Image

# Importowanie modułów do GUI
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


# Definiowanie funkcji, która szyfruje tekst w obrazie
def szyfruj_tekst_w_obrazie(sciezka_do_obrazu, tekst):
    # Dodaj znak końca tekstu do tekstu, aby zaznaczyć koniec tekstu
    tekst += "\0"

    # Otwórz obraz
    obraz = Image.open(sciezka_do_obrazu)
    # Pobieranie szerokości oraz wysokości obrazu
    szerokosc, wysokosc = obraz.size

    # Przekształć tekst na listę wartości ASCII
    tekst_ascii = [ord(c) for c in tekst]

    # Sprawdź, czy tekst mieści się w obrazie
    # Czy długość tekstu w ASCII nie przekracza liczby pikseli
    if len(tekst_ascii) > szerokosc * wysokosc:
        raise ValueError("Tekst jest za długi do zakodowania w tym obrazie.")

    # Szyfruj tekst w obrazie
    for i, wartosc in enumerate(tekst_ascii):
        x = (
            i % szerokosc
        )  # Ustalamy x, gdy x i>szerokość, wtedy bierzemy kolejną linię pikseli
        y = i // szerokosc  # Ustalamy y piksela gdzie zostaje zapisana informacja
        # Pobranie akturalnych składowych RGB piksela
        r, g, b = obraz.getpixel((x, y))
        # Zastąpienie składowej piksela wartością ASCII bieżącego zanku
        obraz.putpixel((x, y), (r, g, wartosc))

    # Zapisz szyfrowany obraz
    obraz.save("szyfrowany_obraz.png")


# Definiowanie funkcji do odszyfrowywania tekstu z obrazu
def odszyfruj_tekst_z_obrazu(sciezka_do_obrazu):
    # Otwórz obraz
    obraz = Image.open(sciezka_do_obrazu)
    # Pobranie szerokości oraz wysokości obrazu
    szerokosc, wysokosc = obraz.size

    # Odszyfruj tekst z obrazie
    tekst = ""
    for y in range(wysokosc):
        for x in range(szerokosc):
            r, g, b = obraz.getpixel((x, y))
            if chr(b) == "\0":  # Zakończ odczytywanie, gdy napotkasz znak końca tekstu
                return tekst
            else:
                tekst += chr(b)

    return tekst


# Definiowanie funkcji, która odpowiada za współdziałanie szyfrowania wraz z GUI
def szyfruj_gui():
    # Użytkownik wybiera obraz
    sciezka_do_obrazu = filedialog.askopenfilename()
    # Okno do wprowadzania tekstu do zaszyfrowania
    tekst = tk.simpledialog.askstring("Input", "Podaj tekst do zaszyfrowania:")
    # Szyfrowanie tekstu w obrazie
    szyfruj_tekst_w_obrazie(sciezka_do_obrazu, tekst)
    # Wyświetlanie okienka z informacją o poprawnym zaszyfrowaniu wiadomości
    messagebox.showinfo("Sukces", "Tekst został zaszyfrowany w obrazie.")


# Definiowanie funkcji odpowiedzialnej za współdziałanie deszyfrowania wraz z GUI
def odszyfruj_gui():
    # Wybieranie obrazu, z którego użytkownik chce odszyfrować wiadomość
    sciezka_do_obrazu = filedialog.askopenfilename()
    # Wykonanie funkcji deszyfrującej
    tekst = odszyfruj_tekst_z_obrazu(sciezka_do_obrazu)
    # Wyświetlenie wiadomości odszyfrowanej z obrazu
    messagebox.showinfo("Odszyfrowany tekst", tekst)


# Tworzenie okna apliacji o wymiarach 400x250
root = tk.Tk()
root.geometry("400x250")
root.resizable(True, True)

# Ustaw kolor tła okna
root.configure(bg="lightblue")

# Tworzymy puste miejsce, pole pomiędzy nazwą programu a górną granicą
puste_miejsce = tk.Frame(width=40, height=30, bg="lightblue")
puste_miejsce.pack()


# Ustawiamy tytuł okna programu
root.title("TextCrypt")

# Dodajemy etykietę z nazwą programu
etykieta_nazwa = tk.Label(
    root, text="TextCrypt", font=("Helvetica", 30), bg="lightblue", fg="black"
)
etykieta_nazwa.pack()

# Tworzymy ramkę, w której będą znajdować się przyciski aby jeden był obok drugiego
ramka_przyciskow = tk.Frame(root)
ramka_przyciskow.pack(pady=40)

# Tworzymy przycik, który odpowiada za szyfrowanie
button_szyfruj = tk.Button(
    ramka_przyciskow,
    text="Szyfruj tekst w obrazie",
    command=szyfruj_gui,
    bg="green",
    fg="black",
)
# Umieszczenie po lewej stronie ramki
button_szyfruj.pack(side=tk.LEFT)

# Dodaj pusty widget między przyciskami
puste_miejsce = tk.Frame(ramka_przyciskow, width=40, height=27, bg="lightblue")
puste_miejsce.pack(side=tk.LEFT)

# Tworzymy drugi przycik, któory odpowiada za deszyfrowanie
button_odszyfruj = tk.Button(
    ramka_przyciskow,
    text="Odszyfruj tekst z obrazu",
    command=odszyfruj_gui,
    bg="red",
    fg="white",
)
# Umieszczenie po prawej stronie ramki
button_odszyfruj.pack(side=tk.RIGHT)

# Dodaj etykietę na dole okna
etykieta_stay_safe = tk.Label(
    root,
    text="Pamiętaj, że bezpieczeństwo zaczyna się od \nzaszyfrowanych komunikatów.",
    bg="lightblue",
    fg="black",
)
etykieta_stay_safe.pack(side=tk.BOTTOM)

root.mainloop()
