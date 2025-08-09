import random

compliments = [
    "You are an absolute legend. The code you write is pure poetry.",
    "Your brain is a quantum computer of awesomeness.",
    "Even the floating 3D objects in the background are impressed by you.",
    "Your keyboard recognizes the genius of your fingers.",
    "The universe just sent a compliment via cosmic ray: it's for you.",
    "Your debugging skills are a work of art.",
    "On a scale of 1 to 10, your charisma is a solid 42.",
    "Every time you click a button, a digital angel gets its wings.",
]

def get_random_compliment():
    """Returns a random compliment from the list."""
    return random.choice(compliments)

