from django.db import models
from django.core.exceptions import ValidationError


CELL_VALUES = {".", "b", "w"}


# class Players(models.Model):
#     name = models.CharField(max_length=24)


class Games(models.Model):
    class BoardSize(models.IntegerChoices):
        SMALL = 9, "9x9"
        MEDIUM = 13, "13x13"
        LARGE = 19, "19x19"

    class Player(models.TextChoices):
        WHITE = 'white'
        BLACK = 'black'

    title = models.CharField(max_length=128, default='Новая игра')
    board_size = models.PositiveSmallIntegerField(
        choices=BoardSize.choices,
        default=BoardSize.LARGE,
    )
    current_position = models.ForeignKey(
        'Positions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_games',
    )
    current_player = models.CharField(
        max_length=5, choices=Player.choices, default=Player.BLACK)


class Positions(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    previous = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next')
    board = models.JSONField(default=dict, blank=True)

    def clean(self):
        super().clean()
        if self.game_id is None:
            raise ValidationError(
                {"game": "Game must be set for position validation."})
        if self.board == {}:
            return

        board_size = self.game.board_size
        if not isinstance(self.board, list) or len(self.board) != board_size:
            raise ValidationError(
                {"board": f"Board must be a list with {board_size} rows."}
            )

        for row in self.board:
            if not isinstance(row, str) or len(row) != board_size:
                raise ValidationError(
                    {"board": f"Each row must be a string with {board_size} cells."}
                )
            if any(cell not in CELL_VALUES for cell in row):
                raise ValidationError(
                    {"board": "Board cells must be '.', 'b' or 'w'."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
