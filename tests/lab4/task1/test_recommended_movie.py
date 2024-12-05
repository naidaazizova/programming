import unittest
from src.lab4.task1.recommended_movie import RecommendedMovie

class MyTestCase(unittest.TestCase):
    movies_path = "movies.txt"
    history_path = "history.txt"
    recommendedMovie = RecommendedMovie(movies_path, history_path)

    def test_creating_people(self):
        self.assertEqual(self.recommendedMovie.people[0].history, ['2', '1', '3'])
        self.assertEqual(self.recommendedMovie.people[2].history, ['2', '2', '2', '2', '2', '3'])

    def test_creating_movies(self):
        self.assertEqual(self.recommendedMovie.movies["1"], "Мстители: Финал")
        self.assertEqual(self.recommendedMovie.movies["4"], "Унесенные призраками")

    def test_recommending_movies(self):
        user_input = "2,3"
        recommended_movie = self.recommendedMovie.recommended_movie(user_input)
        self.assertEqual(recommended_movie, "Мстители: Финал")

        user_input = "3,4"
        recommended_movie = self.recommendedMovie.recommended_movie(user_input)
        self.assertEqual(recommended_movie, "Хатико")

        user_input = "5,6"
        recommended_movie = self.recommendedMovie.recommended_movie(user_input)
        self.assertEqual(recommended_movie, "Для Вас нет рекомендованного фильма")

    def test_recommending_movies_value(self):
        user_input = "2,3"
        recommended_movie = self.recommendedMovie.recommended_movies_value(user_input)
        self.assertEqual(recommended_movie, "Мстители: Финал")

        user_input = "1,4"
        recommended_movie = self.recommendedMovie.recommended_movies_value(user_input)
        self.assertEqual(recommended_movie, "Дюна")

        user_input = "5,6"
        recommended_movie = self.recommendedMovie.recommended_movies_value(user_input)
        self.assertEqual(recommended_movie, "Для Вас нет рекомендованного фильма")


if __name__ == '__main__':
    unittest.main()
