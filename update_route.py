

def addnwrt_from_exis_flight(con):
    cur =  con.cursor()
    print("Fetching unassigned Flights names")
    cur.execute("""SELECT p.pilot_name, p.pilot_id FROM pilot p LEFT JOIN 
                schedule s ON p.pilot_id = s.pilot_id WHERE s.schedule_id IS NULL;""")
    res = cur.fetchall()
    
    return 0