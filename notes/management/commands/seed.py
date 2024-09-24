from django.core.management.base import BaseCommand
from notes.models import Exercise

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('--------seeding data--------')
        run_seed(self, options['mode'])
        self.stdout.write('--------done--------')


def clear_data():
    """Deletes all the table data"""
    Exercise.objects.all().delete()

def add_exercises():
    exercises = {}
    with open("exercises.csv") as file:
        for line in file:
            tmp = line.split(',')
            tmp = [x for x in tmp if x != '' and x != '\n']
            exercises[tmp[0]] = tmp[1:]
    exercises["Back"] = exercises["Back"][:-1]  #last entry of category back is wrong
    for category in exercises:
        for exercise in exercises[category]:
            exercise_obj = Exercise.objects.create(
            name = exercise,
            category = category
            )
            exercise_obj.save()
        
    return "exercise_obj"

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # creating exercises
    add_exercises()