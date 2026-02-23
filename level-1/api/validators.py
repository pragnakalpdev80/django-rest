from rest_framework import serializers

def validate_titleletters(value):
    if len(value)<4:
        raise serializers.ValidationError("Title must be more than 5 letters.")
    return value