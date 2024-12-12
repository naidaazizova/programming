import unittest
from src.lab5.solution import *

class TestOrders(unittest.TestCase):
    def test_order_valid(self): #Тест валидного заказа
        order_data = ['12345', 'Product1, Product2', 'Sarah Shaket', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        order.validate()
        self.assertTrue(order.is_valid())
        self.assertEqual(order.errors, [])

    def test_invalid_phone_format(self): #Тест с неверным форматом номера телефона
        order_data = ['12345', 'Banana, Bread', 'Sarah Shaket', 'Russia. Moscow region. Moscow. Lenin street', '+1-123-4567-890', 'MAX']
        order = Order(order_data)
        order.validate()
        self.assertFalse(order.is_valid())
        self.assertIn(('2', '+1-123-4567-890'), order.errors)

    def test_order_format_address(self): #Тест форматирования адреса
        order_data = ['12345', 'Banana, Bread', 'Sarah Shaket', 'Russia. Moscow region. Moscow. Lenin street', '+1-123-4567-890', 'MAX']
        order = Order(order_data)
        formatted_address = order.format_address()
        expected = 'Moscow region. Moscow. Lenin street'
        self.assertEqual(formatted_address, expected)

    def test_order_format_products(self): #Тест форматирования продуктов
        order_data = ['12345', 'Cookie, Coffee, Cookie, Bread, Coffee', 'Sarah Shaket', 'Russia. Moscow region. Moscow. Lenin street', '+1-123-456-78-90', 'MAX']
        order = Order(order_data)
        formatted_products = order.format_products()
        expected = 'Cookie x2, Coffee x2, Bread'
        self.assertEqual(formatted_products, expected)

    def test_order_process_with_data(self): #Тест OrderProcess с данными напрямую
            orders_data = [
                ['12345', 'Product1, Product2', 'Sarah Shaket', 'CountryA. Region. City. Street', '+1-123-456-78-90', 'MAX'],
                ['12346', 'Product3, Product4', 'Mira Shaket', '', '+1-123-456-78-90', 'LOW']
            ]
            processor = OrderProcess(orders_data=orders_data)
            processor.validate_orders()
            self.assertEqual(len(processor.errors), 1)
            valid_orders = processor.get_valid_orders()
            self.assertEqual(len(valid_orders), 1)
            self.assertEqual(valid_orders[0].order_number, '12345')

    def test_order_process_sort(self): #Тест сортировки заказов
            orders_data = [
                ['12345', '', '', 'CountryA. Region. City. Street', '', 'MAX'],
                ['12346', '', '', 'CountryB. Region. City. Street', '', 'LOW'],
                ['12347', '', '', 'CountryA. Region. City. Street', '', 'MIDDLE']
            ]
            processor = OrderProcess(orders_data=orders_data)
            for order in processor.orders:
                order.validate()
            sorted_orders = processor.sort_orders(processor.orders)
            self.assertEqual(sorted_orders[0].order_number, '12345')  # MAX - приоритет в CountryA
            self.assertEqual(sorted_orders[1].order_number, '12347')  # MIDDLE - приоритет в CountryA
            self.assertEqual(sorted_orders[2].order_number, '12346')  # LOW - приоритет в CountryB

    def test_order_process_full_process(self): #Тест полного процесса обработки без записи в файлы
            orders_data = [
                ['12345', 'Product1, Product2, Product1', 'Sarah Shaket', 'CountryA. Region. City. Street', '+1-123-456-78-90', 'MAX'],
                ['12346', 'Product3, Product4', 'Mira Shaket', '', '', 'LOW']
            ]
            processor = OrderProcess(orders_data=orders_data)
            processor.process()
            self.assertEqual(len(processor.errors), 2)
            valid_orders = processor.get_valid_orders()
            self.assertEqual(len(valid_orders), 1)
            formatted_products = valid_orders[0].format_products()
            self.assertEqual(formatted_products, 'Product1 x2, Product2')

if __name__ == '__main__':
    unittest.main()










