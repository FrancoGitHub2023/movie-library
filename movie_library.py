import json
import os.path

class MovieLibrary:
    # La classe serve per gestire i film contenuti nel file JSON

    class MovieNotFoundError(Exception): # Classe per l'errore personalizzato
        pass
    
    
    def __init__(self, json_file):
        # Controlliamo se il percorso è assoluto
        if not os.path.isabs(json_file):
            raise ValueError("Devi fornire l'intero percorso del file!")
            
        self.json_file = json_file
        
        # Proviamo ad aprire e leggere il file
        try:

            file = open(self.json_file, 'r')
            self.movies = json.load(file)
            file.close()
            
        except FileNotFoundError:
            # Se il file non esiste, lancia l'errore
            raise FileNotFoundError(f"File not found: {self.json_file}")
        
    def _save_to_json(self):
        # Salva il file JSON        
        try:
            # Scrive nel file e lo chiude
            file = open(self.json_file, 'w')
            json.dump(self.movies, file, indent=4)
            file.close()
        except:
            print("Ops! Si è verificato un errore nel salvare il file") 
            
    def get_movies(self):
        # Restituisce l'intera collezione di film
        return self.movies 
    
    def add_movie(self, title, director, year, genres):
        # Creiamo un nuovo film come dizionario con tutti i dati
        nuovo_film = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }
        
        # Aggiungiamo il film alla collezione
        self.movies.append(nuovo_film)
        
        # Salviamo per aggiornare il file JSON
        self._save_to_json() 
    
    def remove_movie(self, title):
        # Cerca il film nella lista
        for film in self.movies:
            # Se troviamo il titolo (NON case sensitive)
            if film["title"].lower() == title.lower():
                # Rimuoviamo il film
                self.movies.remove(film)
                # Salviamo i cambiamenti
                self._save_to_json()
                return film
        
        # Se il film non è stato trovato lanciamo l'errore        
        raise self.MovieNotFoundError("Movie was not found")
    
    def update_movie(self, title, director=None, year=None, genres=None):
        # Cerca il film nella lista
        for film in self.movies:
            # Se troviamo il titolo (NON case sensitive)
            if film["title"].lower() == title.lower():
                # Aggiorna solo i campi che non sono None
                if director is not None:
                    film["director"] = director
                    
                if year is not None:
                    film["year"] = year
                    
                if genres is not None:
                    film["genres"] = genres
                
                # Salviamo le modifiche
                self._save_to_json()
                
                # Restituisce il film modificato
                return film
                
        # il film non è stato trovato
        raise self.MovieNotFoundError("Movie was not found")
    
    def get_movie_titles(self):
        # Creiamo una lista vuota per aggiungere i titoli
        titoli = []
        
        # Per ogni film nella collezione
        for film in self.movies:
            # Aggiunge il titolo alla lista
            titoli.append(film["title"])
            
        # Restituisce la lista dei titoli
        return titoli
    
    def count_movies(self):
        # Restituisce il numero di film presenti nella lista
        return len(self.movies) 
    
    def get_movie_by_title(self, title):
        # Cerchiamo il film nella lista
        for film in self.movies:
            # Confrontiamo i titoli ignorando maiuscole e minuscole
            if film["title"].lower() == title.lower():
                # Se il film è nella lista lo restituiamo
                return film
                
        # Se non troviamo nulla, stampiamo un messaggio di avviso
        print(f"Film '{title}' non è stato trovato!")
        return None
    
    def get_movies_by_title_substring(self, substring):
        # Lista vuota per inserire i film trovati
        film_trovati = []
        
        # Controlliamo ogni film della lista
        for film in self.movies:
            # Se la sottostringa è nel titolo
            if substring in film["title"]:
                # Aggiunge il film alla lista film_trovati
                film_trovati.append(film)
                
        # Restituisce tutti i film trovati
        return film_trovati 
    
    def get_movies_by_year(self, year):
        # Lista vuota per i film trovati
        film_trovati = []
        
        # Controlla ogni film nella lista
        for film in self.movies:
            # Se l'anno corrisponde
            if film["year"] == year:
                # Aggiungiamo il film alla lista
                film_trovati.append(film)
                
        # Restituisce tutti i film trovati
        return film_trovati
    
    def count_movies_by_director(self, director):
        # Contiamo i film del regista
        numero_film = 0
        
        # Controlliamo ogni singolo film
        for film in self.movies:
            # Se il regista corrisponde a quelo richiesto (si ignorano maiuscole e minuscole)
            if film["director"].lower() == director.lower():
                # Incrementa il numero di film
                numero_film = numero_film + 1
                
        # Restituisce il numero totale
        return numero_film
    
    def get_movies_by_genre(self, genre):
        # Inizia con una Lista vuota per i film trovati
        film_trovati = []
        
        # Controlla ogni singolo film
        for film in self.movies:
            # Per ogni genere del film
            for genere_film in film["genres"]:
                # Se il genere corrisponde (non consideriamo maiuscol e minuscole)
                if genere_film.lower() == genre.lower():
                    # Aggiungiamo il film e passiamo al prossimo film
                    film_trovati.append(film)
                    break # usciamo da if 
                    
        # Restituiamo tutti i film trovati
        return film_trovati 
    
    def get_oldest_movie_title(self):
        # Controlliamo se la lista è vuota
        if len(self.movies) == 0:
            print("Non ci sono film!")
            return None
        
        # Prendiamo a riferimento l'anno del primo film
        anno_piu_antico = self.movies[0]["year"]
        titolo_piu_antico = self.movies[0]["title"]
        
        # Confrontiamo tutti i film uno per uno
        for film in self.movies:
            # Se troviamo un anno più anticoo
            if film["year"] < anno_piu_antico:
                # Salviamo l'anno più antico rispetto al riferimento
                anno_piu_antico = film["year"]
                # Prendiamo il titolo di questo film
                titolo_piu_antico = film["title"]
        
        # Alla fine restituiamo il titolo del film più antico
        return titolo_piu_antico
    
    def get_average_release_year(self):
        # Se non ci sono film in lista, non possiamo fare la media
        if len(self.movies) == 0:
            print("Non ci sono film!")
            return 0.0
        
        # somma di tutti gli anni
        totale_anni = 0            
        # Conto il numero di film e sommo gli anni
        for film in self.movies:
            totale_anni = totale_anni + film["year"]
                    
        # Calcolo la media
        media = totale_anni / len(self.movies)
        
        # Arrotondiamo a due decimali
        return round(media, 2) 
    
    def get_longest_title(self):
        # Controllo se ci sono film nella collezione
        if len(self.movies) == 0:
            print("Nella collezione non ci sono film!")
            return None
            
        # Partiamo dal primo titolo a riferimento
        titolo_piu_lungo = self.movies[0]["title"]
        
        # Confronta ogni film
        for film in self.movies:
            # Se trovo un titolo più lungo
            if len(film["title"]) > len(titolo_piu_lungo):
                # Questo diventa il nuovo titolo più lungo
                titolo_piu_lungo = film["title"]
                
        # Ritorna il titolo più lungo trovato
        return titolo_piu_lungo
    
    def get_titles_between_years(self, start_year, end_year):
        # Lista vuota per inserire i titoli che trovo
        titoli_trovati = []
        
        # Controlliamo ogni film
        for film in self.movies:
            # Se l'anno del film è nel range indicato
            if film["year"] >= start_year and film["year"] <= end_year:
                # Aggiunge il titolo ai titoli trovati
                titoli_trovati.append(film["title"])
                
        # Restituiamo tutti i titoli trovati
        return titoli_trovati 
    
    def get_most_common_year(self):
        # Controllo se ci sono film
        if len(self.movies) == 0:
            print("Non ci sono film!")
            return None
            
        # Lista di tutti gli anni
        tutti_gli_anni = []
        for film in self.movies:
            tutti_gli_anni.append(film["year"])
            
        # Trovio l'anno più ripetuto
        anno_piu_ripetuto = tutti_gli_anni[0]  
        max_ripetizioni = 0  # quante volte è ripetuto
        
        # Controllo e confronto di un anno con il successivo
        for anno in tutti_gli_anni:
            # Conteggio di quante volte si ripete l'anno
            ripetizioni = 0
            for altro_anno in tutti_gli_anni:
                if anno == altro_anno:
                    ripetizioni = ripetizioni + 1
            
            # Se questo anno si ripete più volte del precedente
            if ripetizioni > max_ripetizioni:
                anno_piu_ripetuto = anno
                max_ripetizioni = ripetizioni
        
        return anno_piu_ripetuto 