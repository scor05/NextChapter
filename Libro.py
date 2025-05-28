class Libro:    
    def __init__(self, name, length, author, year, genres):  # length = n páginas; genres -> array[String] de géneros del libro
        self.name = name;
        self.length = length;
        self.author = author;
        self.year = year;
        self.genres = genres;