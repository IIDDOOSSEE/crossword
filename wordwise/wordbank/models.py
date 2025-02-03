from django.db import models

class wordBank(models.Model):
    WORD_TYPES = [
        ('noun', 'Noun'),
        ('pronoun', 'Pronoun'),
        ('verb', 'Verb'),
        ('adjective', 'Adjective'),
        ('adverb', 'Adverb'),
        ('preposition', 'Preposition'),
        ('conjunction', 'Conjunction'),
        ('interjection', 'Interjection'),
        ('determiner', 'Determiner'),
        ('phrase', 'Phrase'),
        ('modal verb', 'Modal Verb'),
        ('article', 'Article'),
        ('quantifier', 'Quantifier'),
        ('exclamatory word', 'Exclamatory Word'),
        ('gerund', 'Gerund'),
        ('infinitive', 'Infinitive'),
        ('relative pronoun', 'Relative Pronoun'),
        ('relative adverb', 'Relative Adverb'),
        ('prepositional phrase', 'Prepositional Phrase'),
        ('conjunction adverb', 'Conjunction Adverb'),
        ('correlative conjunction', 'Correlative Conjunction'),
        ('conditional', 'Conditional'),
        ('subjunctive mood', 'Subjunctive Mood'),
        ('indefinite pronoun', 'Indefinite Pronoun'),
        ('causative verb', 'Causative Verb'),
        ('intensifier', 'Intensifier')
    ]

    word = models.CharField(max_length=100, null=False)
    word_type = models.CharField(max_length=50, null=False, choices=WORD_TYPES)
    meaning = models.TextField()
    translates = models.CharField(max_length=100, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['word', 'word_type'], name='unique_word')
        ]

    def __str__(self):
        return self.word
