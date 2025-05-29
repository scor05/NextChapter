class Libro:    
    def __init__(self, name, length, authors, year, genres):  # length = n páginas; genres -> array[String] de géneros del libro
        self.name = name;
        self.authors = authors;
        self.year = year;
        self.genres = genres;