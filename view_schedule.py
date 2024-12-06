import tabulate
from utils import get_full_schedule




def view_pilot_schedule(con):
    cur = con.cursor()
    get_full_schedule(cur)
    return