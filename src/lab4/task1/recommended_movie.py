class Person:
    #Это класс, в котором представлены id пользователя и фильмов, которые уже просмотрены им
    def __init__(self, person_id, history): #Инициализируем объект Human
        self.person_id = person_id
        self.history = history

class Movie:
    #Это класс, в котором представлены id и название фильма
    def __init__(self, movie_id, name): #Инициализируем объект Movie
        self.movie_id = movie_id
        self.name = name

class RecommendedMovie:
    #Это класс для поиска рекомендованного фильма по алгоритму
    def __init__(self, movies_path, history_path): #Инициализируем объект RecommendedMovie
        self.people =[]
        self.movies = {}
        self.creating_people(history_path)
        self.creating_movies(movies_path)

    def creating_people(self, filepath): #Читаем список историй просмотров пользователей из файла
        # и сохраняем их в листе people
        with open(filepath, 'r') as file:
            for i, movies in enumerate(file.readlines()):
                movies = movies.strip().split(",")
                if movies != [""]:
                    human_id = i + 1
                    self.people.append(Person(human_id, movies))

    def creating_movies(self, filepath): #Читаем список фильмов из файла
        # и сохраняем их в словаре movies
        with open(filepath, 'r') as file:
            movies = []
            for line in file.readlines():
                if line.strip():
                    movie_id, name = line.strip().split(",")
                    movies.append(Movie(movie_id, name))
        self.movies = {movie.movie_id: movie.name for movie in movies}

    def recommended_movie(self, user_history): #Находим рекомендованный фильм для пользователя
        # на основе его истории просмотров
        user_history = set(user_history.split(","))
        similar_people = []
        for person in self.people:
            same_history = set(person.history) & user_history
            if len(same_history) >= (len(user_history) / 2):
                similar_people.append(person)

        good_movies = set()
        for person in similar_people:
            good_movies = good_movies | (set(person.history) - user_history)

        recommended_movies = [0] * (len(self.movies) + 1)
        for movie in good_movies:
            for person in self.people:
                for viewed_movie in person.history:
                    if viewed_movie == movie:
                        recommended_movies[int(movie)] += 1

        recommended_movies_id = str(recommended_movies.index(max(recommended_movies)))
        if recommended_movies_id != "0":
            return self.movies[recommended_movies_id]
        return "Для Вас нет рекомендованного фильма"

    def recommended_movies_value(self, user_history): #Находим рекомендованный фильм среди всех пользователей,
        # которые посмотрели наибольшее количество фильмов из истории пользователя
        user_history = set(user_history.split(","))
        similar_people = []
        for person in self.people:
            same_history = set(person.history) & user_history
            if len(same_history) >= (len(user_history) / 2):
                value = len(same_history) / len(user_history)
                similar_people.append((person, value))
        similar_people.sort(key=lambda x: x[1], reverse=True)

        if similar_people:
            good_movies = [set(similar_people[0][0].history) - user_history]
            for i in range(1, len(similar_people)):
                if similar_people[i][1] == similar_people[i - 1][1]:
                    good_movies[-1] = good_movies[-1] | (set(similar_people[i][0].history) - user_history)
                else:
                    good_movies.append(set(similar_people[i][0].history) - user_history)

            recommended_movies = [0] * (len(self.movies) + 1)
            for movie_set in good_movies:
                if movie_set != set():
                    for movie in movie_set:
                        for person in self.people:
                            for viewed_movie in person.history:
                                if viewed_movie == movie:
                                    recommended_movies[int(movie)] += 1
                    recommended_movies_id = str(recommended_movies.index(max(recommended_movies)))
                    return self.movies[recommended_movies_id]
        return "Для Вас нет рекомендованного фильма"

if __name__ == "__main__":
    MOVIES_PATH = "txtf/movies.txt"
    HISTORY_PATH = "txtf/history.txt"

    while True:
        USER_HISTORY = str(input())
        if USER_HISTORY.replace(",", "").isdigit():
            break
    recommendedMovie = RecommendedMovie(MOVIES_PATH, HISTORY_PATH)

    movie = recommendedMovie.recommended_movie(USER_HISTORY)
    movie_value = recommendedMovie.recommended_movies_value(USER_HISTORY)
    print(f"Рекомендованный фильм - {movie}")
    print(f"Рекомендованный фильм по значению - {movie_value}")










