\
# -*- coding: utf-8 -*-
"""
This module contains the food data extracted from the COMIDAS.markdown file.
It provides a list of dictionaries, each representing a food item with its
nutritional information.
"""

FOOD_DATA = [
    # Platos Principales - Carne
    {'category': 'Platos Principales - Carne', 'name': 'Asado (carne a la parrilla)', 'calories': '250 por 100 g', 'proteins': '25'},
    {'category': 'Platos Principales - Carne', 'name': 'Milanesa de carne', 'calories': '280 por 100 g', 'proteins': '20'},
    {'category': 'Platos Principales - Carne', 'name': 'Costillar (costillas asadas)', 'calories': '300 por 100 g', 'proteins': '25'},
    {'category': 'Platos Principales - Carne', 'name': 'Vacío (bife de flanco)', 'calories': '200 por 100 g', 'proteins': '25'},
    {'category': 'Platos Principales - Carne', 'name': 'Bondiola (cerdo asado)', 'calories': '250 por 100 g', 'proteins': '20'},
    {'category': 'Platos Principales - Carne', 'name': 'Carne al horno', 'calories': '250 por 100 g', 'proteins': '25'},
    {'category': 'Platos Principales - Carne', 'name': 'Choripán', 'calories': '400 por unidad', 'proteins': '15'},
    {'category': 'Platos Principales - Carne', 'name': 'Bife de lomo', 'calories': '220 por 100 g', 'proteins': '26'},
    {'category': 'Platos Principales - Carne', 'name': 'Matambre arrollado', 'calories': '300 por porción', 'proteins': '22'},
    {'category': 'Platos Principales - Carne', 'name': 'Morcilla', 'calories': '350 por 100 g', 'proteins': '14'},
    {'category': 'Platos Principales - Carne', 'name': 'Pollo asado', 'calories': '200 por 100 g', 'proteins': '22'},
    {'category': 'Platos Principales - Carne', 'name': 'Carne a la criolla', 'calories': '350 por porción', 'proteins': '20'},

    # Platos Principales - Empanadas
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de carne', 'calories': '300 por empanada', 'proteins': '12'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de pollo', 'calories': '280 por empanada', 'proteins': '10'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de jamón y queso', 'calories': '270 por empanada', 'proteins': '8'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de humita', 'calories': '250 por empanada', 'proteins': '6'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de verdura', 'calories': '240 por empanada', 'proteins': '5'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de queso y cebolla', 'calories': '260 por empanada', 'proteins': '7'},
    {'category': 'Platos Principales - Empanadas', 'name': 'Empanada de atún', 'calories': '280 por empanada', 'proteins': '12'},

    # Platos Principales - Pastas
    {'category': 'Platos Principales - Pastas', 'name': 'Ñoquis de papa', 'calories': '150 por 100 g', 'proteins': '4'},
    {'category': 'Platos Principales - Pastas', 'name': 'Ravioles de ricotta', 'calories': '200 por 100 g', 'proteins': '8'},
    {'category': 'Platos Principales - Pastas', 'name': 'Fideos con salsa tuco', 'calories': '350 por porción', 'proteins': '12'},
    {'category': 'Platos Principales - Pastas', 'name': 'Sorrentinos de jamón y queso', 'calories': '220 por 100 g', 'proteins': '9'},
    {'category': 'Platos Principales - Pastas', 'name': 'Tallarines con pesto', 'calories': '400 por porción', 'proteins': '10'},
    {'category': 'Platos Principales - Pastas', 'name': 'Fideos con estofado', 'calories': '380 por porción', 'proteins': '15'},

    # Platos Principales - Guisos
    {'category': 'Platos Principales - Guisos', 'name': 'Guiso de lentejas', 'calories': '300 por porción', 'proteins': '18'},
    {'category': 'Platos Principales - Guisos', 'name': 'Locro', 'calories': '400 por porción', 'proteins': '20'},
    {'category': 'Platos Principales - Guisos', 'name': 'Estofado de carne', 'calories': '350 por porción', 'proteins': '20'},
    {'category': 'Platos Principales - Guisos', 'name': 'Carbonada', 'calories': '380 por porción', 'proteins': '18'},
    {'category': 'Platos Principales - Guisos', 'name': 'Guiso de mondongo', 'calories': '320 por porción', 'proteins': '22'},
    {'category': 'Platos Principales - Guisos', 'name': 'Guiso de arroz', 'calories': '300 por porción', 'proteins': '10'},

    # Platos Principales - Otros
    {'category': 'Platos Principales - Otros', 'name': 'Pastel de papas', 'calories': '400 por porción', 'proteins': '20'},
    {'category': 'Platos Principales - Otros', 'name': 'Tortilla de papas', 'calories': '200 por porción', 'proteins': '10'},
    {'category': 'Platos Principales - Otros', 'name': 'Pizza (porción mozzarella)', 'calories': '250 por porción', 'proteins': '10'},
    {'category': 'Platos Principales - Otros', 'name': 'Fainá', 'calories': '200 por porción', 'proteins': '5'},
    {'category': 'Platos Principales - Otros', 'name': 'Provoleta', 'calories': '300 por 100 g', 'proteins': '20'},
    {'category': 'Platos Principales - Otros', 'name': 'Tarta de zapallitos', 'calories': '300 por porción', 'proteins': '8'},

    # Acompañamientos
    {'category': 'Acompañamientos', 'name': 'Ensalada mixta (lechuga, tomate, cebolla)', 'calories': '100 por porción', 'proteins': '2'},
    {'category': 'Acompañamientos', 'name': 'Papas fritas', 'calories': '300 por 100 g', 'proteins': '3'},
    {'category': 'Acompañamientos', 'name': 'Puré de papas', 'calories': '150 por 100 g', 'proteins': '2'},
    {'category': 'Acompañamientos', 'name': 'Puré de calabaza', 'calories': '100 por 100 g', 'proteins': '2'},
    {'category': 'Acompañamientos', 'name': 'Choclo asado', 'calories': '120 por mazorca', 'proteins': '4'},
    {'category': 'Acompañamientos', 'name': 'Berenjenas al escabeche', 'calories': '150 por porción', 'proteins': '1'},
    {'category': 'Acompañamientos', 'name': 'Zapallitos rellenos', 'calories': '200 por porción', 'proteins': '8'},
    {'category': 'Acompañamientos', 'name': 'Arroz con queso', 'calories': '200 por 100 g', 'proteins': '6'},
    {'category': 'Acompañamientos', 'name': 'Batatas asadas', 'calories': '100 por 100 g', 'proteins': '2'},
    {'category': 'Acompañamientos', 'name': 'Ensalada rusa', 'calories': '250 por porción', 'proteins': '5'},
    {'category': 'Acompañamientos', 'name': 'Papas a la crema', 'calories': '250 por porción', 'proteins': '4'},
    {'category': 'Acompañamientos', 'name': 'Tomates rellenos', 'calories': '150 por porción', 'proteins': '6'},

    # Sándwiches
    {'category': 'Sándwiches', 'name': 'Sánguche de miga (jamón y queso)', 'calories': '250 por unidad', 'proteins': '10'},
    {'category': 'Sándwiches', 'name': 'Sánguche de milanesa', 'calories': '600 por unidad', 'proteins': '25'},
    {'category': 'Sándwiches', 'name': 'Tostado (jamón y queso)', 'calories': '300 por unidad', 'proteins': '12'},
    {'category': 'Sándwiches', 'name': 'Sánguche de bondiola', 'calories': '500 por unidad', 'proteins': '20'},
    {'category': 'Sándwiches', 'name': 'Sánguche de lomo', 'calories': '450 por unidad', 'proteins': '22'},
    {'category': 'Sándwiches', 'name': 'Sánguche de matambre', 'calories': '400 por unidad', 'proteins': '20'},
    {'category': 'Sándwiches', 'name': 'Sánguche de vacío', 'calories': '450 por unidad', 'proteins': '24'},

    # Panificados y Facturas
    {'category': 'Panificados y Facturas', 'name': 'Medialunas', 'calories': '200 por unidad', 'proteins': '5'},
    {'category': 'Panificados y Facturas', 'name': 'Facturas (variedad)', 'calories': '250 por unidad', 'proteins': '4'},
    {'category': 'Panificados y Facturas', 'name': 'Tortitas negras', 'calories': '300 por unidad', 'proteins': '5'},
    {'category': 'Panificados y Facturas', 'name': 'Churros', 'calories': '200 por unidad', 'proteins': '3'},
    {'category': 'Panificados y Facturas', 'name': 'Chipá', 'calories': '150 por unidad', 'proteins': '4'},
    {'category': 'Panificados y Facturas', 'name': 'Cañoncitos', 'calories': '300 por unidad', 'proteins': '5'},
    {'category': 'Panificados y Facturas', 'name': 'Palmeritas', 'calories': '250 por unidad', 'proteins': '3'},

    # Postres
    {'category': 'Postres', 'name': 'Dulce de leche (porción)', 'calories': '300 por 100 g', 'proteins': '7'},
    {'category': 'Postres', 'name': 'Alfajor', 'calories': '400 por unidad', 'proteins': '5'},
    {'category': 'Postres', 'name': 'Flan casero', 'calories': '250 por porción', 'proteins': '6'},
    {'category': 'Postres', 'name': 'Panqueque con dulce de leche', 'calories': '350 por unidad', 'proteins': '6'},
    {'category': 'Postres', 'name': 'Torta rogel', 'calories': '500 por porción', 'proteins': '8'},
    {'category': 'Postres', 'name': 'Vigilante (queso y dulce)', 'calories': '400 por porción', 'proteins': '10'},
    {'category': 'Postres', 'name': 'Pastafrola', 'calories': '350 por porción', 'proteins': '5'},
    {'category': 'Postres', 'name': 'Tarta de manzana', 'calories': '300 por porción', 'proteins': '4'},
    {'category': 'Postres', 'name': 'Arroz con leche', 'calories': '200 por porción', 'proteins': '5'},
    {'category': 'Postres', 'name': 'Helado de dulce de leche', 'calories': '250 por 100 g', 'proteins': '4'},
    {'category': 'Postres', 'name': 'Tarta de coco', 'calories': '400 por porción', 'proteins': '6'},
    {'category': 'Postres', 'name': 'Mousse de chocolate', 'calories': '300 por porción', 'proteins': '5'},

    # Bebidas
    {'category': 'Bebidas', 'name': 'Café con leche', 'calories': '100 por taza', 'proteins': '5'},
    {'category': 'Bebidas', 'name': 'Mate (sin azúcar)', 'calories': '10 por taza', 'proteins': '0'},
    {'category': 'Bebidas', 'name': 'Licuado de banana', 'calories': '200 por vaso', 'proteins': '4'},
    {'category': 'Bebidas', 'name': 'Capuchino', 'calories': '150 por taza', 'proteins': '6'},
    {'category': 'Bebidas', 'name': 'Té con leche', 'calories': '100 por taza', 'proteins': '4'},
    {'category': 'Bebidas', 'name': 'Submarino (chocolate caliente)', 'calories': '300 por taza', 'proteins': '8'},
    {'category': 'Bebidas', 'name': 'Licuado de durazno', 'calories': '180 por vaso', 'proteins': '3'},

    # Snacks
    {'category': 'Snacks', 'name': 'Torta frita', 'calories': '300 por unidad', 'proteins': '4'},
    {'category': 'Snacks', 'name': 'Criollitos', 'calories': '200 por unidad', 'proteins': '3'},
    {'category': 'Snacks', 'name': 'Sopaipillas', 'calories': '250 por unidad', 'proteins': '3'},
    {'category': 'Snacks', 'name': 'Bolitas de fraile', 'calories': '280 por unidad', 'proteins': '4'},
    {'category': 'Snacks', 'name': 'Pionono', 'calories': '350 por porción', 'proteins': '6'},
    {'category': 'Snacks', 'name': 'Manzanas acarameladas', 'calories': '200 por unidad', 'proteins': '1'},

    # Desayuno
    {'category': 'Desayuno', 'name': 'Tostadas con manteca', 'calories': '200 por porción', 'proteins': '3'},
    {'category': 'Desayuno', 'name': 'Tostadas con dulce de leche', 'calories': '250 por porción', 'proteins': '4'},
    {'category': 'Desayuno', 'name': 'Yogur con frutas', 'calories': '150 por porción', 'proteins': '6'},
    {'category': 'Desayuno', 'name': 'Huevos revueltos', 'calories': '150 por porción', 'proteins': '12'},
    {'category': 'Desayuno', 'name': 'Mermelada (porción)', 'calories': '100 por 20 g', 'proteins': '0'},
    {'category': 'Desayuno', 'name': 'Fruta fresca (naranja)', 'calories': '60 por unidad', 'proteins': '1'},

    # Sopas
    {'category': 'Sopas', 'name': 'Sopa de zapallo', 'calories': '150 por porción', 'proteins': '3'},
    {'category': 'Sopas', 'name': 'Sopa de verduras', 'calories': '100 por porción', 'proteins': '2'},
    {'category': 'Sopas', 'name': 'Puchero', 'calories': '400 por porción', 'proteins': '20'},
    {'category': 'Sopas', 'name': 'Sopa de lentejas', 'calories': '250 por porción', 'proteins': '15'},
    {'category': 'Sopas', 'name': 'Sopa de pollo', 'calories': '200 por porción', 'proteins': '10'},

    # Platos Regionales
    {'category': 'Platos Regionales', 'name': 'Humita en chala', 'calories': '200 por porción', 'proteins': '5'},
    {'category': 'Platos Regionales', 'name': 'Tamales', 'calories': '300 por unidad', 'proteins': '8'},
    {'category': 'Platos Regionales', 'name': 'Milanesa napolitana', 'calories': '400 por 100 g', 'proteins': '22'},
    {'category': 'Platos Regionales', 'name': 'Pollo al disco', 'calories': '350 por porción', 'proteins': '25'},
    {'category': 'Platos Regionales', 'name': 'Lomo a la pizza', 'calories': '450 por porción', 'proteins': '28'},
    {'category': 'Platos Regionales', 'name': 'Empanada salteña', 'calories': '290 por empanada', 'proteins': '11'},

    # Comida Rápida
    {'category': 'Comida Rápida', 'name': 'Hamburguesa casera', 'calories': '500 por unidad', 'proteins': '20'},
    {'category': 'Comida Rápida', 'name': 'Lomito completo', 'calories': '600 por unidad', 'proteins': '25'},
    {'category': 'Comida Rápida', 'name': 'Papas al horno', 'calories': '150 por 100 g', 'proteins': '2'},
    {'category': 'Comida Rápida', 'name': 'Calzone de jamón y queso', 'calories': '350 por unidad', 'proteins': '15'},
    {'category': 'Comida Rápida', 'name': 'Pizza fugazzeta', 'calories': '300 por porción', 'proteins': '12'},

    # Bebidas (Alcohólicas)
    {'category': 'Bebidas (Alcohólicas)', 'name': 'Fernet con Coca', 'calories': '200 por vaso', 'proteins': '0'},
    {'category': 'Bebidas (Alcohólicas)', 'name': 'Vino tinto (copa)', 'calories': '125 por 150 ml', 'proteins': '0'},
    {'category': 'Bebidas (Alcohólicas)', 'name': 'Cerveza artesanal', 'calories': '150 por 330 ml', 'proteins': '1'},

    # Misceláneos
    {'category': 'Misceláneos', 'name': 'Revuelto Gramajo', 'calories': '400 por porción', 'proteins': '15'},
    {'category': 'Misceláneos', 'name': 'Tarta de jamón y queso', 'calories': '350 por porción', 'proteins': '12'},
    {'category': 'Misceláneos', 'name': 'Matambre a la pizza', 'calories': '350 por 100 g', 'proteins': '20'},
]

# Example usage: Print the name and calories of the first food item
# if __name__ == "__main__":
#     print(f"Food: {FOOD_DATA[0]['name']}, Calories: {FOOD_DATA[0]['calories']}")
#     # You can iterate through the list or access items by index
#     for food in FOOD_DATA:
#         if food['category'] == 'Postres':
#             print(f"Dessert: {food['name']}")
