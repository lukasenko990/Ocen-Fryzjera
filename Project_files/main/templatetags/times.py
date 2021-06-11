#!/usr/bin/env python3

from django import template

register = template.Library()

@register.filter
def times(number):
    return range(number)

@register.filter
def distractfiveabs(number):
    return abs(number-5)
