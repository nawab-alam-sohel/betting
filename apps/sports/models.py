from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class League(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='leagues')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='leagues/', null=True, blank=True)
    country = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    external_id = models.CharField(max_length=100, null=True, blank=True, help_text='ID from external API')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-priority', 'name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Team(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='teams/', null=True, blank=True)
    leagues = models.ManyToManyField(League, related_name='teams')
    external_id = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Game(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('closed', 'Closed for Betting'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='games')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time', 'league__name']
        indexes = [
            models.Index(fields=['status', 'start_time']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.start_time})"


class Market(models.Model):
    MARKET_TYPES = [
        ('1x2', '1X2'),
        ('ou', 'Over/Under'),
        ('gg', 'Both Teams to Score'),
        ('cs', 'Correct Score'),
        ('ht', 'Half Time'),
        ('dc', 'Double Chance'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='markets')
    market_type = models.CharField(max_length=20, choices=MARKET_TYPES)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    external_id = models.CharField(max_length=100, null=True, blank=True)
    specifier = models.JSONField(null=True, blank=True, help_text='Additional parameters like handicap/total')
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['priority', 'market_type']
        indexes = [
            models.Index(fields=['status', 'market_type']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.game} - {self.name}"


class Selection(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
        ('cashout', 'Cash Out'),
    ]

    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='selections')
    name = models.CharField(max_length=100)
    odds = models.DecimalField(max_digits=10, decimal_places=3)
    american_odds = models.IntegerField(null=True, blank=True)
    probability = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    result = models.CharField(max_length=20, null=True, blank=True)
    external_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['market', 'name']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.market} - {self.name} @ {self.odds}"

    def save(self, *args, **kwargs):
        # Convert decimal odds to American odds
        if self.odds and not self.american_odds:
            if self.odds >= 2.0:
                self.american_odds = int((self.odds - 1) * 100)
            else:
                self.american_odds = int(-100 / (self.odds - 1))
        super().save(*args, **kwargs)


class SportsProvider(models.Model):
    """External sports data provider configuration (demo vs real)."""
    key = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    base_url = models.URLField(blank=True)
    config = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name