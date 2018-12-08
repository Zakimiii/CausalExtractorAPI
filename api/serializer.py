from rest_framework import serializers

from .models import Causal, Morph, Pos
# import CabochaParser.CabochaParser
# import CausalExtraction.CausalExtraction
from cabocha.analyzer import CaboChaAnalyzer

# 
# class CausalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Causal
#         # fields = ('name', 'mail')
#
# class MorphSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Morph
#         # fields = ('name', 'mail')
#
# class PosSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pos
#         # fields = ('name', 'mail')
