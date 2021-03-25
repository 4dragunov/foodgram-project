from time import time

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from multiselectfield import MultiSelectField

User = get_user_model()

BREAKFAST = 'breakfast'
LUNCH = 'lunch'
DINNER = 'dinner'

TAGS = ((BREAKFAST, 'breakfast'),
        (LUNCH, 'lunch'),
        (DINNER, 'dinner'))


def gen_slug(s):
    ''' Генерация slug для рецепта'''
    new_slug = (slugify(s, allow_unicode=True))
    return f'{new_slug}-{str(int(time()))}'


class Ingredients(models.Model):
    '''Модель ингридиентов (без привязки к рецепту)'''
    title = models.CharField(max_length=100, verbose_name='Название')
    dimension = models.CharField(max_length=50,
                                 verbose_name='Единица измерения')

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.title} {self.dimension}'


class Recipe(models.Model):
    '''Модель рецепта'''
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    prep_time = models.PositiveIntegerField(verbose_name='Время приготовления',
                                            help_text='в минутах',
                                            validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='recipes/images/',
                              verbose_name='Изображение',
                              help_text='поле для рисунка')
    date_pub = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата создания')
    tags = MultiSelectField(choices=TAGS,
                            default=BREAKFAST,
                            verbose_name='Теги')

    slug = models.SlugField(max_length=150, blank=True, unique=True)

    ingredients = models.ManyToManyField(Ingredients,
                                         blank=False,
                                         through='IngredientsForRecipe',
                                         verbose_name='Ингредиенты'
                                         )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipe_detail_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ("-date_pub",)


class IngredientsForRecipe(models.Model):
    '''
    Таблица связи между рецептом и количеством ингридиента
    '''
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                   verbose_name='Ингридиент',
                                   related_name='ingredient_recipe')
    amount = models.PositiveIntegerField(default=1,
                                         help_text='в граммах',
                                         validators=[MinValueValidator(1)],
                                         null=False,
                                         blank=False)
    date_pub = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата создания')

    def __str__(self):
        return f'{self.ingredient} для рецепта {self.recipe}'

    class Meta:
        verbose_name_plural = "Ингредиенты для рецепта"
        verbose_name = "Ингредиент для рецепта"


class Subscription(models.Model):
    '''Подписка на автора'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name='Пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following",
                               verbose_name='Автор')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ['user', 'author']
        ordering = ['user', 'author']


class Favorite(models.Model):
    '''Избранные рецепты'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name="favorites",
                             )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorites')

    date_pub = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата создания')

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ("-date_pub",)


class Purchase(models.Model):
    '''Список покупок'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name="purchases",
                             )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='purchases')

    date_pub = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата создания')

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ("-date_pub",)

    def __str__(self):
        return self.recipe.title

